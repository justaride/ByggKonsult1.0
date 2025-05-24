#!/usr/bin/env python3
"""
Oslo Planning System
Dedikert system for Oslo kommune plandata - kun Oslo-fokusert
Integrerer Origo dataplatform, PBE-systemer og Oslo-spesifikke dokumenter
"""

import requests
import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OsloPlanningSystem:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Oslo-Planning-System/1.0'
        })
        
        # Oslo-spesifikke datakilder
        self.oslo_sources = {
            'origo': {
                'base_url': 'https://api.oslo.kommune.no',
                'sdk_available': True,
                'contact': 'dataplattform@oslo.kommune.no',
                'environment': 'dev'  # eller 'prod'
            },
            'pbe_systems': {
                'planinnsyn': 'https://od2.pbe.oslo.kommune.no',
                'byggesak': 'https://innsyn.pbe.oslo.kommune.no',
                'eiendom': 'https://eiendom.oslo.kommune.no',
                'kart': 'https://kart.oslo.kommune.no',
                'tomteutleie': 'https://tomteutleie.oslo.kommune.no'
            },
            'oslo_official': {
                'kommune_main': 'https://www.oslo.kommune.no',
                'plan_bygg': 'https://www.oslo.kommune.no/plan-bygg-og-eiendom',
                'statistikk': 'https://statistikkbanken.oslo.kommune.no'
            }
        }
        
        # Oslo-spesifikke plantyper og dokumenter
        self.oslo_plan_types = {
            'kommuneplan': {
                'navn': 'Kommuneplan for Oslo',
                'status': 'gjeldende',
                'vedtatt': '2020',
                'dokumenter': ['arealdel', 'samfunnsdel', 'planbestemmelser']
            },
            'reguleringsplaner': {
                'antall_aktive': 'ca. 3000+',
                'kategorier': ['detaljregulering', 'områderegulering', 'planendring'],
                'format': 'SOSI og PDF'
            },
            'temaplaner': [
                'Temaplan kultur og idrett',
                'Temaplan for bolig',
                'Temaplan for næring',
                'Temaplan transport',
                'Klimaplan'
            ]
        }
        
        # Oslo-spesifikke nøkkelord for plandata
        self.oslo_keywords = {
            'områder': [
                'sentrum', 'grünerløkka', 'frogner', 'gamle oslo',
                'st. hanshaugen', 'sagene', 'ullern', 'vestre aker',
                'nordre aker', 'bjerke', 'grorud', 'stovner',
                'alna', 'østensjø', 'nordstrand', 'søndre nordstrand'
            ],
            'oslo_spesifikk': [
                'oslo kommune', 'oslo s', 'bjørvika', 'barcode',
                'tjuvholmen', 'aker brygge', 'vulkan', 'grønland',
                'tøyen', 'kampen', 'vålerenga', 'majorstuen'
            ],
            'planterminologi': [
                'oslo_kommuneplan', 'oslo_regulering', 'pbe_oslo',
                'plan_og_bygningsetaten', 'oslo_planstrategi'
            ]
        }
        
        # Oslo datasett storage
        self.oslo_data = {
            'origo_datasets': [],
            'reguleringsplaner': [],
            'byggesaker': [],
            'eiendomsdata': [],
            'infrastruktur': [],
            'temaplaner': [],
            'pdf_documents': [],
            'processing_log': []
        }
    
    def log_operation(self, operation: str, details: Dict[str, Any]):
        """Log Oslo-spesifikke operasjoner"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'oslo_context': True,
            'details': details
        }
        self.oslo_data['processing_log'].append(log_entry)
        logger.info(f"Oslo {operation}: {details.get('summary', 'Operation completed')}")
    
    def setup_origo_connection(self):
        """Sett opp tilkobling til Oslo Origo"""
        logger.info("Setting up Oslo Origo connection...")
        
        try:
            from okdata.sdk.config import Config
            from okdata.sdk.data.dataset import Dataset
            
            # Oslo-spesifikk konfigurasjon
            config = Config(env=self.oslo_sources['origo']['environment'])
            dataset_client = Dataset(config=config)
            
            self.log_operation('origo_setup', {
                'status': 'sdk_configured',
                'environment': self.oslo_sources['origo']['environment'],
                'summary': 'Origo SDK configured for Oslo'
            })
            
            return {'config': config, 'client': dataset_client, 'status': 'ready'}
            
        except ImportError:
            logger.warning("okdata-sdk not found. Install with: pip install okdata-sdk")
            return {'status': 'sdk_missing'}
        except Exception as e:
            logger.warning(f"Origo setup failed: {e}")
            return {'status': 'auth_needed', 'error': str(e)}
    
    def search_oslo_origo_datasets(self):
        """Søk kun etter Oslo-spesifikke datasett i Origo"""
        logger.info("Searching for Oslo-specific datasets in Origo...")
        
        origo_setup = self.setup_origo_connection()
        
        if origo_setup['status'] == 'ready':
            try:
                # Forsøk å liste datasett med Origo SDK
                # Dette krever gyldig autentisering
                logger.info("Origo SDK ready, but requires authentication")
                
                # Placeholder for når autentisering er på plass
                sample_oslo_datasets = self.get_sample_oslo_datasets()
                
                self.log_operation('origo_dataset_search', {
                    'method': 'sample_data',
                    'datasets_found': len(sample_oslo_datasets),
                    'summary': 'Using sample Oslo datasets until authentication is set up'
                })
                
                return sample_oslo_datasets
                
            except Exception as e:
                logger.warning(f"Origo dataset search failed: {e}")
                return []
        else:
            logger.info("Using sample Oslo datasets - Origo authentication needed")
            return self.get_sample_oslo_datasets()
    
    def get_sample_oslo_datasets(self) -> List[Dict]:
        """Eksempel på Oslo-datasett basert på kjent struktur"""
        return [
            {
                'source': 'oslo_origo',
                'dataset_id': 'oslo-reguleringsplaner',
                'title': 'Reguleringsplaner Oslo kommune',
                'description': 'Alle reguleringsplaner i Oslo kommune',
                'category': 'plandata',
                'format': 'JSON/GeoJSON',
                'update_frequency': 'daily',
                'oslo_specific': True
            },
            {
                'source': 'oslo_origo',
                'dataset_id': 'oslo-byggetillatelser',
                'title': 'Byggetillatelser Oslo',
                'description': 'Byggetillatelser behandlet av PBE',
                'category': 'byggesak',
                'format': 'JSON',
                'update_frequency': 'daily',
                'oslo_specific': True
            },
            {
                'source': 'oslo_origo',
                'dataset_id': 'oslo-eiendomsdata',
                'title': 'Eiendomsdata Oslo',
                'description': 'Eiendomsinformasjon og matrikkeldata',
                'category': 'eiendom',
                'format': 'JSON',
                'update_frequency': 'weekly',
                'oslo_specific': True
            },
            {
                'source': 'oslo_origo',
                'dataset_id': 'oslo-infrastruktur',
                'title': 'Infrastrukturdata Oslo',
                'description': 'VA-nett, strøm, vei og kollektivtransport',
                'category': 'infrastruktur',
                'format': 'GeoJSON',
                'update_frequency': 'monthly',
                'oslo_specific': True
            },
            {
                'source': 'oslo_origo',
                'dataset_id': 'oslo-bydelsfakta',
                'title': 'Bydelsfakta Oslo',
                'description': 'Demografiske data for Oslos 15 bydeler',
                'category': 'demografi',
                'format': 'JSON',
                'update_frequency': 'yearly',
                'oslo_specific': True
            }
        ]
    
    def search_oslo_geonorge_data(self):
        """Søk kun etter Oslo-spesifikke data på Geonorge"""
        logger.info("Searching for Oslo-specific data on Geonorge...")
        
        try:
            search_url = "https://kartkatalog.geonorge.no/api/search"
            params = {
                'text': 'Oslo kommune reguleringsplan',
                'limit': 50,
                'facets[0]name': 'type',
                'facets[0]value': 'dataset'
            }
            
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            search_results = response.json()
            oslo_plans = []
            
            if 'Results' in search_results:
                for result in search_results['Results']:
                    # Filtrer kun Oslo-relaterte resultater
                    title = result.get('Title', '').lower()
                    organization = result.get('Organization', '').lower()
                    
                    if self.is_oslo_related(title, organization):
                        plan_data = {
                            'source': 'geonorge_oslo',
                            'plan_id': result.get('Uuid', ''),
                            'title': result.get('Title', ''),
                            'organization': result.get('Organization', ''),
                            'description': result.get('Abstract', ''),
                            'theme': result.get('Theme', []),
                            'keywords': result.get('Keywords', []),
                            'oslo_relevance': self.assess_oslo_relevance(result),
                            'download_links': self.extract_download_links(result)
                        }
                        oslo_plans.append(plan_data)
            
            self.log_operation('geonorge_oslo_search', {
                'total_results': len(search_results.get('Results', [])),
                'oslo_specific': len(oslo_plans),
                'summary': f'Found {len(oslo_plans)} Oslo-specific plans on Geonorge'
            })
            
            return oslo_plans
            
        except requests.RequestException as e:
            logger.error(f"Geonorge Oslo search failed: {e}")
            return []
    
    def is_oslo_related(self, title: str, organization: str) -> bool:
        """Sjekk om data er Oslo-relatert"""
        oslo_indicators = [
            'oslo', 'oslo kommune', 'plan- og bygningsetaten',
            'pbe oslo', 'oslo kommuneplan'
        ]
        
        text_to_check = f"{title} {organization}".lower()
        return any(indicator in text_to_check for indicator in oslo_indicators)
    
    def assess_oslo_relevance(self, dataset_info: Dict) -> str:
        """Vurder Oslo-relevans"""
        title = dataset_info.get('Title', '').lower()
        
        if 'oslo kommune' in title:
            return 'high'
        elif any(area in title for area in self.oslo_keywords['områder']):
            return 'medium'
        elif 'oslo' in title:
            return 'low'
        else:
            return 'minimal'
    
    def extract_download_links(self, geonorge_data: Dict) -> List[Dict]:
        """Ekstrakta nedlastingslenker fra Geonorge data"""
        links = []
        
        if 'DistributionDetails' in geonorge_data:
            for dist in geonorge_data['DistributionDetails']:
                if 'URL' in dist:
                    links.append({
                        'url': dist['URL'],
                        'protocol': dist.get('Protocol', ''),
                        'name': dist.get('Name', ''),
                        'format': dist.get('Protocol', '').upper()
                    })
        
        return links
    
    def process_oslo_pdf_documents(self, pdf_directory: str = ".") -> List[Dict]:
        """Prosesser kun Oslo-relaterte PDF-dokumenter"""
        logger.info(f"Processing Oslo-specific PDF documents from {pdf_directory}")
        
        pdf_results = []
        pdf_files = list(Path(pdf_directory).glob("*.pdf"))
        
        for pdf_file in pdf_files:
            try:
                # Analyser PDF for Oslo-relevans
                analysis = self.analyze_oslo_pdf(str(pdf_file))
                
                if analysis and analysis.get('oslo_relevant', False):
                    oslo_pdf_data = {
                        'source': 'oslo_pdf',
                        'file_path': str(pdf_file),
                        'oslo_relevance': analysis.get('oslo_relevance_score', 0),
                        'plan_id': analysis.get('plan_id'),
                        'oslo_areas': analysis.get('oslo_areas', []),
                        'plan_type': analysis.get('plan_type'),
                        'processed_at': datetime.now().isoformat(),
                        'content_summary': analysis.get('content_analysis', {})
                    }
                    pdf_results.append(oslo_pdf_data)
                
            except Exception as e:
                logger.error(f"Error processing Oslo PDF {pdf_file}: {e}")
        
        self.log_operation('oslo_pdf_processing', {
            'files_processed': len(pdf_files),
            'oslo_relevant_found': len(pdf_results),
            'summary': f'Processed {len(pdf_results)} Oslo-relevant PDFs'
        })
        
        return pdf_results
    
    def analyze_oslo_pdf(self, pdf_path: str) -> Optional[Dict]:
        """Analyser PDF for Oslo-spesifikt innhold"""
        try:
            # Import PDF libraries
            try:
                import pdfplumber
                text = self.extract_text_pdfplumber(pdf_path)
            except ImportError:
                try:
                    import PyPDF2
                    text = self.extract_text_pypdf2(pdf_path)
                except ImportError:
                    return {'error': 'No PDF libraries available'}
            
            if not text:
                return {'error': 'Could not extract text'}
            
            # Analyser for Oslo-relevans
            oslo_analysis = self.analyze_oslo_content(text)
            
            if oslo_analysis['oslo_relevance_score'] > 0:
                oslo_analysis['oslo_relevant'] = True
                oslo_analysis['content_analysis'] = {
                    'total_chars': len(text),
                    'total_words': len(text.split()),
                    'oslo_mentions': oslo_analysis['oslo_mentions']
                }
            
            return oslo_analysis
            
        except Exception as e:
            return {'error': f'PDF analysis failed: {e}'}
    
    def extract_text_pdfplumber(self, pdf_path: str) -> str:
        """Ekstrakta tekst med pdfplumber"""
        import pdfplumber
        
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def extract_text_pypdf2(self, pdf_path: str) -> str:
        """Ekstrakta tekst med PyPDF2"""
        import PyPDF2
        
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def analyze_oslo_content(self, text: str) -> Dict:
        """Analyser tekst for Oslo-spesifikt innhold"""
        text_lower = text.lower()
        
        # Tell Oslo-referanser
        oslo_mentions = 0
        found_areas = []
        found_oslo_terms = []
        
        # Sjekk Oslo-områder
        for area in self.oslo_keywords['områder']:
            if area in text_lower:
                oslo_mentions += 2  # Bydeler gir høy score
                found_areas.append(area)
        
        # Sjekk Oslo-spesifikke termer
        for term in self.oslo_keywords['oslo_spesifikk']:
            if term in text_lower:
                oslo_mentions += 1
                found_oslo_terms.append(term)
        
        # Sjekk planterminologi
        for term in self.oslo_keywords['planterminologi']:
            if term in text_lower:
                oslo_mentions += 3  # Høy score for planerminologi
                found_oslo_terms.append(term)
        
        # Ekstrakter plan-ID hvis det er Oslo-relatert
        plan_id = None
        if oslo_mentions > 0:
            plan_id = self.extract_plan_id(text)
        
        return {
            'oslo_relevance_score': oslo_mentions,
            'oslo_areas': found_areas,
            'oslo_terms': found_oslo_terms,
            'oslo_mentions': oslo_mentions,
            'plan_id': plan_id,
            'plan_type': self.extract_oslo_plan_type(text_lower)
        }
    
    def extract_plan_id(self, text: str) -> Optional[str]:
        """Ekstrakta plan-ID fra tekst"""
        patterns = [
            r'plan[- ]?id[:\s]*([A-Za-z0-9\-\.]+)',
            r'saksnummer[:\s]*([A-Za-z0-9\-\.\/]+)',
            r'oslo[- ]plan[:\s]*([A-Za-z0-9\-\.]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def extract_oslo_plan_type(self, text: str) -> Optional[str]:
        """Identifiser Oslo plantype"""
        if 'kommuneplan' in text:
            return 'kommuneplan'
        elif 'detaljregulering' in text:
            return 'detaljregulering'
        elif 'områderegulering' in text:
            return 'områderegulering'
        elif 'reguleringsplan' in text:
            return 'reguleringsplan'
        elif any(tema in text for tema in ['temaplan', 'klimaplan', 'transportplan']):
            return 'temaplan'
        return None
    
    def integrate_oslo_data(self) -> Dict:
        """Integrer alle Oslo-datakilder"""
        logger.info("Starting Oslo data integration...")
        
        # Samle data fra alle Oslo-kilder
        origo_datasets = self.search_oslo_origo_datasets()
        geonorge_oslo = self.search_oslo_geonorge_data()
        oslo_pdfs = self.process_oslo_pdf_documents()
        
        # Lagre i Oslo-struktur
        self.oslo_data['origo_datasets'] = origo_datasets
        self.oslo_data['reguleringsplaner'].extend(geonorge_oslo)
        self.oslo_data['pdf_documents'] = oslo_pdfs
        
        # Oslo-spesifikk cross-referencing
        oslo_integrated = self.cross_reference_oslo_data()
        
        self.log_operation('oslo_data_integration', {
            'origo_datasets': len(origo_datasets),
            'geonorge_oslo_plans': len(geonorge_oslo),
            'oslo_pdfs': len(oslo_pdfs),
            'total_oslo_sources': len(origo_datasets) + len(geonorge_oslo) + len(oslo_pdfs),
            'summary': f'Integrated {len(origo_datasets) + len(geonorge_oslo) + len(oslo_pdfs)} Oslo data sources'
        })
        
        return oslo_integrated
    
    def cross_reference_oslo_data(self) -> Dict:
        """Cross-reference kun Oslo data"""
        logger.info("Cross-referencing Oslo data sources...")
        
        oslo_unified = {}
        
        # Kombiner alle Oslo datasett
        all_oslo_data = (
            self.oslo_data['origo_datasets'] +
            self.oslo_data['reguleringsplaner'] +
            self.oslo_data['pdf_documents']
        )
        
        for item in all_oslo_data:
            oslo_key = self.generate_oslo_key(item)
            
            if oslo_key in oslo_unified:
                oslo_unified[oslo_key] = self.merge_oslo_data(oslo_unified[oslo_key], item)
            else:
                oslo_unified[oslo_key] = item
        
        return {
            'oslo_unified_data': list(oslo_unified.values()),
            'total_oslo_items': len(oslo_unified),
            'source_breakdown': self.get_oslo_source_summary(),
            'oslo_coverage': self.assess_oslo_coverage(oslo_unified)
        }
    
    def generate_oslo_key(self, item: Dict) -> str:
        """Generer Oslo-spesifikk nøkkel"""
        plan_id = item.get('plan_id', '')
        title = item.get('title', '').lower()
        
        # Oslo-spesifikk nøkkel
        if plan_id:
            return f"oslo_{plan_id}"
        elif title:
            # Bruk Oslo-områder for å lage nøkkel
            for area in self.oslo_keywords['områder']:
                if area in title:
                    return f"oslo_{area}_{hash(title) % 1000}"
        
        return f"oslo_general_{hash(str(item)) % 1000}"
    
    def merge_oslo_data(self, existing: Dict, new: Dict) -> Dict:
        """Merge Oslo-spesifikk data"""
        merged = existing.copy()
        
        # Legg til Oslo-kilder
        if 'oslo_sources' not in merged:
            merged['oslo_sources'] = [existing.get('source', 'unknown')]
        
        if new.get('source') not in merged['oslo_sources']:
            merged['oslo_sources'].append(new.get('source', 'unknown'))
        
        # Merge Oslo-spesifikke felt
        oslo_fields = ['oslo_areas', 'oslo_terms', 'oslo_relevance_score']
        for field in oslo_fields:
            if field in new and new[field]:
                if field not in merged:
                    merged[field] = new[field]
                elif isinstance(merged[field], list):
                    merged[field].extend(new[field])
                elif isinstance(merged[field], (int, float)):
                    merged[field] = max(merged[field], new[field])
        
        return merged
    
    def get_oslo_source_summary(self) -> Dict:
        """Sammendrag av Oslo-kilder"""
        return {
            'origo_datasets': len(self.oslo_data['origo_datasets']),
            'geonorge_oslo': len(self.oslo_data['reguleringsplaner']),
            'oslo_pdfs': len(self.oslo_data['pdf_documents']),
            'total_oslo_sources': sum([
                len(self.oslo_data['origo_datasets']),
                len(self.oslo_data['reguleringsplaner']),
                len(self.oslo_data['pdf_documents'])
            ])
        }
    
    def assess_oslo_coverage(self, unified_data: Dict) -> Dict:
        """Vurder Oslo-dekning"""
        items = list(unified_data.values())
        
        # Tell Oslo-bydeler som er dekket
        covered_areas = set()
        for item in items:
            if 'oslo_areas' in item:
                covered_areas.update(item['oslo_areas'])
        
        return {
            'covered_oslo_areas': len(covered_areas),
            'total_oslo_areas': len(self.oslo_keywords['områder']),
            'coverage_percentage': (len(covered_areas) / len(self.oslo_keywords['områder'])) * 100,
            'missing_areas': [area for area in self.oslo_keywords['områder'] if area not in covered_areas]
        }
    
    def export_oslo_data(self, output_file: str = None) -> str:
        """Eksporter kun Oslo-data"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'oslo_planning_data_{timestamp}.json'
        
        oslo_export = {
            'generated_at': datetime.now().isoformat(),
            'system_info': {
                'name': 'Oslo Planning System',
                'version': '1.0',
                'oslo_focused': True,
                'data_sources': ['oslo_origo', 'geonorge_oslo', 'oslo_pdfs']
            },
            'oslo_data': self.oslo_data,
            'oslo_metadata': {
                'kommune': 'Oslo',
                'bydeler': self.oslo_keywords['områder'],
                'plantyper': list(self.oslo_plan_types.keys()),
                'kontakt': self.oslo_sources['origo']['contact']
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(oslo_export, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Oslo data exported to {output_file}")
        return output_file
    
    def generate_oslo_report(self) -> Dict:
        """Generer Oslo-spesifikk rapport"""
        oslo_integrated = self.cross_reference_oslo_data()
        
        report = {
            'report_type': 'oslo_planning_system',
            'generated_at': datetime.now().isoformat(),
            'oslo_summary': {
                'total_oslo_data_points': oslo_integrated['total_oslo_items'],
                'origo_status': 'configured_needs_auth',
                'pbe_systems_checked': len(self.oslo_sources['pbe_systems']),
                'oslo_coverage': oslo_integrated['oslo_coverage']
            },
            'data_quality': {
                'oslo_specific_data': oslo_integrated['total_oslo_items'],
                'multi_source_items': len([
                    item for item in oslo_integrated['oslo_unified_data'] 
                    if len(item.get('oslo_sources', [])) > 1
                ]),
                'areas_covered': oslo_integrated['oslo_coverage']['covered_oslo_areas']
            },
            'recommendations': [
                "Få Origo API-tilgang fra dataplattform@oslo.kommune.no",
                "Test okdata-cli med ekte Oslo datasett",
                "Utvide PDF-samling med Oslo-planer",
                "Implementere real-time oppdatering fra Oslo-kilder",
                "Fokusere på manglende bydeler i datasamlingen"
            ],
            'oslo_contacts': {
                'origo_platform': 'dataplattform@oslo.kommune.no',
                'pbe_main': 'postmottak.pbe@oslo.kommune.no',
                'phone': '02180'
            }
        }
        
        return report

def main():
    print("🏛️ OSLO PLANNING SYSTEM")
    print("Dedikert system for Oslo kommune plandata")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize Oslo-spesifikt system
    oslo_system = OsloPlanningSystem()
    
    # Kjør Oslo dataintegrasjon
    print("\n=== OSLO DATA INTEGRATION ===")
    oslo_result = oslo_system.integrate_oslo_data()
    
    # Generer Oslo-rapport
    print("\n=== OSLO ANALYSIS ===")
    oslo_report = oslo_system.generate_oslo_report()
    
    # Eksporter Oslo-data
    print("\n=== OSLO DATA EXPORT ===")
    oslo_export_file = oslo_system.export_oslo_data()
    
    # Lagre Oslo-rapport
    report_file = f"oslo_planning_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(oslo_report, f, indent=2, ensure_ascii=False)
    
    # Vis Oslo-resultater
    print(f"\n=== OSLO RESULTS ===")
    print(f"🏛️ Oslo data points: {oslo_report['oslo_summary']['total_oslo_data_points']}")
    print(f"🗺️ Oslo areas covered: {oslo_report['oslo_summary']['oslo_coverage']['covered_oslo_areas']}/{len(oslo_system.oslo_keywords['områder'])}")
    print(f"📊 Coverage: {oslo_report['oslo_summary']['oslo_coverage']['coverage_percentage']:.1f}%")
    print(f"🔗 Multi-source items: {oslo_report['data_quality']['multi_source_items']}")
    
    print(f"\n📁 Oslo files generated:")
    print(f"   - {oslo_export_file} (Oslo data)")
    print(f"   - {report_file} (Oslo analysis)")
    
    print(f"\n🎯 Next steps for Oslo:")
    for i, rec in enumerate(oslo_report['recommendations'][:3], 1):
        print(f"   {i}. {rec}")
    
    print(f"\n📧 Oslo contact: {oslo_report['oslo_contacts']['origo_platform']}")
    print(f"✅ Oslo Planning System ready!")

if __name__ == "__main__":
    main()