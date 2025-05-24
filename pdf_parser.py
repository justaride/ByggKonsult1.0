#!/usr/bin/env python3
"""
PDF Parser for Norwegian Regulatory Plans (Reguleringsplaner)
Første versjon av PDF-parser for å ekstraktere informasjon fra reguleringsplaner
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
import sys

# Try to import PDF libraries
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

class RegulatoryPlanPDFParser:
    def __init__(self):
        self.norwegian_keywords = {
            'plan_info': [
                'reguleringsplan', 'detaljplan', 'områderegulering',
                'planid', 'plan-id', 'saksnummer', 'plankart',
                'planbestemmelser', 'planbeskrivelse'
            ],
            'administrative': [
                'kommunenummer', 'kommune', 'fylke', 'plantype',
                'planstatus', 'vedtaksdato', 'kunngjøringsdato',
                'behandlende myndighet', 'plansaksbehandler'
            ],
            'areas': [
                'areal', 'kvadratmeter', 'dekar', 'hektar',
                'byggeområde', 'naturområde', 'landbruksområde',
                'friluftsområde', 'byggehøyde', 'utnyttingsgrad'
            ],
            'zoning': [
                'formål', 'bebyggelse og anlegg', 'samferdselsanlegg',
                'teknisk infrastruktur', 'grønnstruktur', 'bruk og vern',
                'boligbebyggelse', 'fritidsbebyggelse', 'sentrumsformål',
                'næringsbebyggelse', 'industri', 'råstoffutvinning'
            ],
            'restrictions': [
                'byggegrense', 'byggelinje', 'byggeforbud',
                'hensynssone', 'sikringssone', 'støysone',
                'faresone', 'bevaring', 'naturvernområde'
            ]
        }
        
        self.coordinate_patterns = [
            r'(\d+\.\d+)[,\s]+(\d+\.\d+)',  # Decimal coordinates
            r'UTM\s*[\d\s]*[,:\s]*(\d+)[,\s]+(\d+)',  # UTM coordinates
            r'N\s*(\d+)[,\s]+E\s*(\d+)',  # N/E coordinates
        ]
        
        self.date_patterns = [
            r'(\d{1,2})\.(\d{1,2})\.(\d{4})',  # DD.MM.YYYY
            r'(\d{4})-(\d{1,2})-(\d{1,2})',   # YYYY-MM-DD
        ]
    
    def check_dependencies(self):
        """Sjekk hvilke PDF-biblioteker som er tilgjengelige"""
        available = []
        missing = []
        
        if PYPDF2_AVAILABLE:
            available.append("PyPDF2")
        else:
            missing.append("PyPDF2")
            
        if PDFPLUMBER_AVAILABLE:
            available.append("pdfplumber")
        else:
            missing.append("pdfplumber")
        
        print(f"Available PDF libraries: {', '.join(available) if available else 'None'}")
        if missing:
            print(f"Missing PDF libraries: {', '.join(missing)}")
            print("Install with: pip install PyPDF2 pdfplumber")
        
        return len(available) > 0
    
    def extract_text_pypdf2(self, pdf_path):
        """Ekstrakta tekst med PyPDF2"""
        if not PYPDF2_AVAILABLE:
            return None
            
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error with PyPDF2: {e}")
            return None
    
    def extract_text_pdfplumber(self, pdf_path):
        """Ekstrakta tekst med pdfplumber (bedre for tabeller og layout)"""
        if not PDFPLUMBER_AVAILABLE:
            return None
            
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"Error with pdfplumber: {e}")
            return None
    
    def extract_text(self, pdf_path):
        """Ekstrakta tekst fra PDF med beste tilgjengelige metode"""
        text = None
        
        # Prøv pdfplumber først (bedre kvalitet)
        if PDFPLUMBER_AVAILABLE:
            text = self.extract_text_pdfplumber(pdf_path)
        
        # Fall back til PyPDF2
        if not text and PYPDF2_AVAILABLE:
            text = self.extract_text_pypdf2(pdf_path)
        
        return text
    
    def find_keywords(self, text, category):
        """Finn nøkkelord i tekst"""
        if category not in self.norwegian_keywords:
            return []
        
        found_keywords = []
        keywords = self.norwegian_keywords[category]
        
        text_lower = text.lower()
        
        for keyword in keywords:
            if keyword in text_lower:
                # Finn kontekst rundt nøkkelordet
                pattern = re.compile(f'(.{{0,50}}{re.escape(keyword)}.{{0,50}})', re.IGNORECASE)
                matches = pattern.findall(text)
                for match in matches[:3]:  # Maks 3 matches per nøkkelord
                    found_keywords.append({
                        'keyword': keyword,
                        'context': match.strip()
                    })
        
        return found_keywords
    
    def extract_coordinates(self, text):
        """Ekstrakta koordinater fra tekst"""
        coordinates = []
        
        for pattern in self.coordinate_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                coordinates.append({
                    'x': match[0],
                    'y': match[1],
                    'type': 'coordinate_pair'
                })
        
        return coordinates[:10]  # Maks 10 koordinater
    
    def extract_dates(self, text):
        """Ekstrakta datoer fra tekst"""
        dates = []
        
        for pattern in self.date_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                dates.append({
                    'raw': '.'.join(match) if len(match) == 3 else '-'.join(match),
                    'components': match
                })
        
        return dates[:10]  # Maks 10 datoer
    
    def extract_plan_id(self, text):
        """Ekstrakta plan-ID fra tekst"""
        plan_id_patterns = [
            r'plan[- ]?id[:\s]*([A-Za-z0-9\-\.]+)',
            r'saksnummer[:\s]*([A-Za-z0-9\-\.\/]+)',
            r'plannummer[:\s]*([A-Za-z0-9\-\.]+)',
        ]
        
        for pattern in plan_id_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def extract_municipality(self, text):
        """Ekstrakta kommune fra tekst"""
        municipality_patterns = [
            r'([A-Za-zÆØÅæøå\s]+)\s+kommune',
            r'kommune[:\s]+([A-Za-zÆØÅæøå\s]+)',
        ]
        
        for pattern in municipality_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def parse_pdf(self, pdf_path):
        """Parse en PDF-fil og ekstrakta informasjon"""
        if not os.path.exists(pdf_path):
            return {'error': f'File not found: {pdf_path}'}
        
        print(f"Parsing PDF: {os.path.basename(pdf_path)}")
        
        # Ekstrakta tekst
        text = self.extract_text(pdf_path)
        if not text:
            return {'error': 'Could not extract text from PDF'}
        
        # Analyse tekst
        analysis = {
            'file_info': {
                'path': pdf_path,
                'filename': os.path.basename(pdf_path),
                'size_bytes': os.path.getsize(pdf_path),
                'parsed_at': datetime.now().isoformat()
            },
            'content_analysis': {
                'total_chars': len(text),
                'total_words': len(text.split()),
                'total_lines': len(text.split('\n'))
            },
            'extracted_info': {
                'plan_id': self.extract_plan_id(text),
                'municipality': self.extract_municipality(text),
                'coordinates': self.extract_coordinates(text),
                'dates': self.extract_dates(text)
            },
            'keywords': {}
        }
        
        # Finn nøkkelord i forskjellige kategorier
        for category in self.norwegian_keywords:
            keywords_found = self.find_keywords(text, category)
            if keywords_found:
                analysis['keywords'][category] = keywords_found
        
        # Legg til rå tekst (begrenset)
        analysis['sample_text'] = text[:1000] + "..." if len(text) > 1000 else text
        
        return analysis
    
    def create_sample_pdf(self, output_path="sample_regulatory_plan.pdf"):
        """Lag en enkel eksempel-PDF for testing"""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            
            c = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4
            
            # Tittel
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "REGULERINGSPLAN")
            c.drawString(50, height - 70, "Eksempel kommune")
            
            # Plan informasjon
            c.setFont("Helvetica", 12)
            y = height - 120
            lines = [
                "Plan-ID: 2024-001",
                "Saksnummer: 24/00123",
                "Kommune: Eksempel kommune",
                "Plantype: Detaljregulering",
                "Vedtaksdato: 15.03.2024",
                "",
                "FORMÅL:",
                "- Boligbebyggelse (§12-5 nr. 1)",
                "- Grønnstruktur (§12-5 nr. 3)",
                "",
                "AREAL:",
                "Totalt planareal: 2,5 hektar",
                "Byggeområde: 1,8 hektar",
                "",
                "KOORDINATER (UTM 33):",
                "Nord: 6643210, Øst: 598765",
                "Nord: 6643185, Øst: 598820"
            ]
            
            for line in lines:
                c.drawString(50, y, line)
                y -= 20
            
            c.save()
            print(f"Sample PDF created: {output_path}")
            return output_path
            
        except ImportError:
            print("reportlab not available. Install with: pip install reportlab")
            return None

def main():
    print("=== PDF Parser for Regulatory Plans ===")
    
    parser = RegulatoryPlanPDFParser()
    
    # Sjekk avhengigheter
    if not parser.check_dependencies():
        print("\nNo PDF libraries available. Please install:")
        print("pip install PyPDF2 pdfplumber")
        return
    
    # Lag eksempel-PDF hvis ingen PDF-filer finnes
    pdf_files = list(Path('.').glob('*.pdf'))
    
    if not pdf_files:
        print("\nNo PDF files found. Creating sample PDF...")
        sample_path = parser.create_sample_pdf()
        if sample_path:
            pdf_files = [Path(sample_path)]
    
    # Parse PDFs
    results = []
    for pdf_file in pdf_files:
        result = parser.parse_pdf(str(pdf_file))
        results.append(result)
        
        # Vis resultat
        print(f"\n=== ANALYSIS: {pdf_file.name} ===")
        
        if 'error' in result:
            print(f"Error: {result['error']}")
            continue
            
        # Vis ekstraktert informasjon
        extracted = result['extracted_info']
        if extracted['plan_id']:
            print(f"Plan ID: {extracted['plan_id']}")
        if extracted['municipality']:
            print(f"Municipality: {extracted['municipality']}")
        if extracted['coordinates']:
            print(f"Coordinates found: {len(extracted['coordinates'])}")
        if extracted['dates']:
            print(f"Dates found: {len(extracted['dates'])}")
        
        # Vis nøkkelord
        for category, keywords in result['keywords'].items():
            if keywords:
                print(f"\n{category.upper()} keywords:")
                for kw in keywords[:3]:  # Vis første 3
                    print(f"  - {kw['keyword']}: {kw['context'][:60]}...")
    
    # Lagre resultater
    output_file = f"pdf_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()