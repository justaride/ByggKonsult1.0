#!/usr/bin/env python3
"""
Integrated Planning Data System
Integrert system som kombinerer:
- Oslo Origo Dataplatform
- Geonorge/Kartverket API-er  
- PDF-parser for reguleringsplaner
- Unified data processing og analyse
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

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntegratedPlanningSystem:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Integrated-Planning-System/1.0'
        })
        
        # Data sources configuration
        self.data_sources = {
            'geonorge': {
                'base_url': 'https://kartkatalog.geonorge.no/api',
                'wfs_base': 'https://wfs.geonorge.no/skwms1',
                'seplan': 'https://seplan.geonorge.no'
            },
            'oslo_origo': {
                'base_url': 'https://api.oslo.kommune.no',  # Placeholder
                'sdk_available': True,
                'contact': 'dataplattform@oslo.kommune.no'
            },
            'oslo_planinnsyn': {
                'base_url': 'https://od2.pbe.oslo.kommune.no'
            }
        }
        
        # Integrated data storage
        self.integrated_data = {
            'regulatory_plans': [],
            'metadata_sources': {},
            'pdf_analyses': [],
            'geographic_data': [],
            'processing_log': []
        }
        
        # Norwegian planning keywords for unified search
        self.planning_keywords = {
            'plan_types': [
                'reguleringsplan', 'detaljplan', 'områderegulering',
                'kommuneplan', 'reguleringsplanforslag'
            ],
            'areas': [
                'boligbebyggelse', 'næringsbebyggelse', 'industri',
                'sentrumsformål', 'fritidsbebyggelse', 'landbruksområde',
                'naturområde', 'friluftsområde', 'grønnstruktur'
            ],
            'administrative': [
                'planid', 'saksnummer', 'vedtaksdato', 'kunngjøringsdato',
                'planstatus', 'behandlende_myndighet'
            ]
        }
    
    def log_operation(self, operation: str, details: Dict[str, Any]):
        """Log system operations"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'details': details
        }
        self.integrated_data['processing_log'].append(log_entry)
        logger.info(f"{operation}: {details.get('summary', 'Operation completed')}")
    
    def search_geonorge_plans(self, municipality: str = None, limit: int = 50) -> List[Dict]:
        """Search for regulatory plans via Geonorge API"""
        logger.info(f"Searching Geonorge for regulatory plans{f' in {municipality}' if municipality else ''}")
        
        search_url = f"{self.data_sources['geonorge']['base_url']}/search"
        
        # Build search query
        query_parts = ['reguleringsplan']
        if municipality:
            query_parts.append(municipality)
        
        params = {
            'text': ' '.join(query_parts),
            'limit': limit,
            'facets[0]name': 'type',
            'facets[0]value': 'dataset'
        }
        
        try:
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            search_results = response.json()
            
            plans = []
            if 'Results' in search_results:
                for result in search_results['Results']:
                    plan_data = self.extract_plan_metadata(result, 'geonorge')
                    if plan_data:
                        plans.append(plan_data)
            
            self.log_operation('geonorge_search', {
                'municipality': municipality,
                'plans_found': len(plans),
                'summary': f'Found {len(plans)} plans from Geonorge'
            })
            
            return plans
            
        except requests.RequestException as e:
            logger.error(f"Geonorge search failed: {e}")
            return []
    
    def search_oslo_origo_plans(self) -> List[Dict]:
        """Search for regulatory plans via Oslo Origo (placeholder)"""
        logger.info("Searching Oslo Origo for regulatory plans")
        
        # Check if Oslo SDK is available
        try:
            import okdata
            from okdata.sdk.config import Config
            from okdata.sdk.data.dataset import Dataset
            
            # This would be the real implementation
            config = Config(env="dev")
            dataset_client = Dataset(config=config)
            
            # Search for planning datasets
            planning_keywords = ['reguleringsplan', 'plandata', 'arealplan']
            
            oslo_plans = []
            
            # Placeholder for real API calls
            logger.info("Oslo Origo SDK available but requires authentication")
            
            self.log_operation('oslo_origo_search', {
                'status': 'sdk_available_needs_auth',
                'summary': 'Oslo Origo SDK detected but requires authentication setup'
            })
            
            return oslo_plans
            
        except ImportError:
            logger.info("Oslo Origo SDK not installed - using placeholder data")
            
            # Generate sample Oslo data structure for integration testing
            sample_oslo_plans = [{
                'source': 'oslo_origo',
                'plan_id': 'oslo-sample-001',
                'title': 'Reguleringsplan for Bjørvika',
                'municipality': 'Oslo',
                'status': 'vedtatt',
                'area_m2': 250000,
                'plan_type': 'detaljregulering',
                'contact': 'dataplattform@oslo.kommune.no'
            }]
            
            self.log_operation('oslo_origo_search', {
                'status': 'sample_data',
                'plans_found': len(sample_oslo_plans),
                'summary': 'Using sample Oslo data for integration testing'
            })
            
            return sample_oslo_plans
    
    def extract_plan_metadata(self, raw_data: Dict, source: str) -> Optional[Dict]:
        """Extract standardized plan metadata from different sources"""
        
        if source == 'geonorge':
            return {
                'source': 'geonorge',
                'plan_id': raw_data.get('Uuid', ''),
                'title': raw_data.get('Title', ''),
                'organization': raw_data.get('Organization', ''),
                'municipality': self.extract_municipality_from_title(raw_data.get('Title', '')),
                'description': raw_data.get('Abstract', ''),
                'theme': raw_data.get('Theme', []),
                'keywords': raw_data.get('Keywords', []),
                'bbox': raw_data.get('BoundingBox', {}),
                'download_links': self.extract_download_links(raw_data),
                'last_updated': raw_data.get('Updated', ''),
                'metadata_url': f"https://kartkatalog.geonorge.no/metadata/{raw_data.get('Uuid', '')}"
            }
        
        elif source == 'oslo_origo':
            # Standardized format for Oslo data
            return raw_data  # Already in our format
        
        return None
    
    def extract_municipality_from_title(self, title: str) -> str:
        """Extract municipality name from plan title"""
        municipality_patterns = [
            r'([A-Za-zÆØÅæøå\s]+)\s+kommune',
            r'kommune[:\s]+([A-Za-zÆØÅæøå\s]+)',
            r'([A-Za-zÆØÅæøå]+)\s+reguleringsplan'
        ]
        
        for pattern in municipality_patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return 'Unknown'
    
    def extract_download_links(self, geonorge_data: Dict) -> List[Dict]:
        """Extract download links from Geonorge data"""
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
    
    def process_pdf_files(self, pdf_directory: str = ".") -> List[Dict]:
        """Process PDF files using integrated parser"""
        logger.info(f"Processing PDF files from {pdf_directory}")
        
        pdf_results = []
        pdf_files = list(Path(pdf_directory).glob("*.pdf"))
        
        for pdf_file in pdf_files:
            try:
                # Import our existing PDF parser functionality
                analysis = self.analyze_pdf_with_enhanced_parser(str(pdf_file))
                
                if analysis and 'error' not in analysis:
                    # Standardize PDF analysis format
                    standardized = {
                        'source': 'pdf_analysis',
                        'file_path': str(pdf_file),
                        'plan_id': analysis['extracted_info'].get('plan_id'),
                        'municipality': self.clean_municipality_name(
                            analysis['extracted_info'].get('municipality', '')
                        ),
                        'coordinates': analysis['extracted_info'].get('coordinates', []),
                        'dates': analysis['extracted_info'].get('dates', []),
                        'keywords_found': analysis.get('keywords', {}),
                        'content_stats': analysis.get('content_analysis', {}),
                        'processed_at': datetime.now().isoformat()
                    }
                    
                    pdf_results.append(standardized)
                
            except Exception as e:
                logger.error(f"Error processing {pdf_file}: {e}")
        
        self.log_operation('pdf_processing', {
            'files_processed': len(pdf_files),
            'successful_analyses': len(pdf_results),
            'summary': f'Processed {len(pdf_results)}/{len(pdf_files)} PDF files'
        })
        
        return pdf_results
    
    def analyze_pdf_with_enhanced_parser(self, pdf_path: str) -> Optional[Dict]:
        """Enhanced PDF analysis using our existing parser"""
        # This integrates with our existing PDF parser
        try:
            # Import PDF libraries if available
            try:
                import pdfplumber
                PDFPLUMBER_AVAILABLE = True
            except ImportError:
                PDFPLUMBER_AVAILABLE = False
            
            try:
                import PyPDF2
                PYPDF2_AVAILABLE = True
            except ImportError:
                PYPDF2_AVAILABLE = False
            
            if not (PDFPLUMBER_AVAILABLE or PYPDF2_AVAILABLE):
                return {'error': 'No PDF libraries available'}
            
            # Extract text using available libraries
            text = None
            
            if PDFPLUMBER_AVAILABLE:
                with pdfplumber.open(pdf_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            
            elif PYPDF2_AVAILABLE:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            
            if not text:
                return {'error': 'Could not extract text'}
            
            # Analyze extracted text
            return self.analyze_planning_text(text, pdf_path)
            
        except Exception as e:
            return {'error': f'PDF processing failed: {e}'}
    
    def analyze_planning_text(self, text: str, source_path: str) -> Dict:
        """Analyze text for planning information"""
        analysis = {
            'file_info': {
                'path': source_path,
                'size_bytes': len(text),
                'processed_at': datetime.now().isoformat()
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
                'dates': self.extract_dates(text),
                'plan_type': self.extract_plan_type(text),
                'area_info': self.extract_area_info(text)
            },
            'keywords': self.find_planning_keywords(text)
        }
        
        return analysis
    
    def extract_plan_id(self, text: str) -> Optional[str]:
        """Extract plan ID from text"""
        patterns = [
            r'plan[- ]?id[:\s]*([A-Za-z0-9\-\.]+)',
            r'saksnummer[:\s]*([A-Za-z0-9\-\.\/]+)',
            r'plannummer[:\s]*([A-Za-z0-9\-\.]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def extract_municipality(self, text: str) -> Optional[str]:
        """Extract municipality from text"""
        patterns = [
            r'([A-Za-zÆØÅæøå\s]+)\s+kommune',
            r'kommune[:\s]+([A-Za-zÆØÅæøå\s]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def extract_coordinates(self, text: str) -> List[Dict]:
        """Extract coordinates from text"""
        patterns = [
            r'(\d+\.\d+)[,\s]+(\d+\.\d+)',
            r'UTM\s*[\d\s]*[,:\s]*(\d+)[,\s]+(\d+)',
            r'N\s*(\d+)[,\s]+E\s*(\d+)'
        ]
        
        coordinates = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches[:5]:  # Limit to 5 coordinates
                coordinates.append({
                    'x': match[0],
                    'y': match[1],
                    'type': 'coordinate_pair'
                })
        
        return coordinates
    
    def extract_dates(self, text: str) -> List[Dict]:
        """Extract dates from text"""
        patterns = [
            r'(\d{1,2})\.(\d{1,2})\.(\d{4})',
            r'(\d{4})-(\d{1,2})-(\d{1,2})'
        ]
        
        dates = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches[:5]:  # Limit to 5 dates
                dates.append({
                    'raw': '.'.join(match) if len(match) == 3 else '-'.join(match),
                    'components': match
                })
        
        return dates
    
    def extract_plan_type(self, text: str) -> Optional[str]:
        """Extract plan type from text"""
        for plan_type in self.planning_keywords['plan_types']:
            if plan_type in text.lower():
                return plan_type
        return None
    
    def extract_area_info(self, text: str) -> Dict:
        """Extract area information from text"""
        area_patterns = [
            r'(\d+[\.,]\d+)\s*(hektar|ha)',
            r'(\d+[\.,]\d+)\s*(kvadratmeter|m2|m²)',
            r'areal[:\s]*(\d+[\.,]\d+)'
        ]
        
        areas = []
        for pattern in area_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                areas.append({
                    'value': match[0],
                    'unit': match[1] if len(match) > 1 else 'unknown'
                })
        
        return {'areas_found': areas}
    
    def find_planning_keywords(self, text: str) -> Dict:
        """Find planning keywords in text"""
        found_keywords = {}
        text_lower = text.lower()
        
        for category, keywords in self.planning_keywords.items():
            found_in_category = []
            
            for keyword in keywords:
                if keyword in text_lower:
                    # Find context around keyword
                    pattern = re.compile(f'(.{{0,50}}{re.escape(keyword)}.{{0,50}})', re.IGNORECASE)
                    matches = pattern.findall(text)
                    
                    for match in matches[:2]:  # Max 2 contexts per keyword
                        found_in_category.append({
                            'keyword': keyword,
                            'context': match.strip()
                        })
            
            if found_in_category:
                found_keywords[category] = found_in_category
        
        return found_keywords
    
    def clean_municipality_name(self, municipality: str) -> str:
        """Clean and standardize municipality names"""
        if not municipality:
            return 'Unknown'
        
        # Remove common suffixes and clean up
        cleaned = municipality.replace('kommune', '').strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Multiple spaces to single
        
        return cleaned.title() if cleaned else 'Unknown'
    
    def integrate_data_sources(self, municipality: str = None) -> Dict:
        """Integrate data from all sources"""
        logger.info(f"Starting integrated data collection{f' for {municipality}' if municipality else ''}")
        
        # Collect from all sources
        geonorge_plans = self.search_geonorge_plans(municipality)
        oslo_plans = self.search_oslo_origo_plans()
        pdf_analyses = self.process_pdf_files()
        
        # Store in integrated data structure
        self.integrated_data['regulatory_plans'].extend(geonorge_plans)
        self.integrated_data['regulatory_plans'].extend(oslo_plans)
        self.integrated_data['pdf_analyses'].extend(pdf_analyses)
        
        # Cross-reference and deduplicate
        integrated_result = self.cross_reference_data()
        
        self.log_operation('data_integration', {
            'geonorge_plans': len(geonorge_plans),
            'oslo_plans': len(oslo_plans),
            'pdf_analyses': len(pdf_analyses),
            'total_integrated': len(integrated_result['unified_plans']),
            'summary': f'Integrated data from {len(geonorge_plans + oslo_plans + pdf_analyses)} sources'
        })
        
        return integrated_result
    
    def cross_reference_data(self) -> Dict:
        """Cross-reference data between sources"""
        logger.info("Cross-referencing data between sources")
        
        unified_plans = {}
        
        # Process all regulatory plans
        for plan in self.integrated_data['regulatory_plans']:
            plan_key = self.generate_plan_key(plan)
            
            if plan_key in unified_plans:
                # Merge with existing plan
                unified_plans[plan_key] = self.merge_plan_data(
                    unified_plans[plan_key], plan
                )
            else:
                unified_plans[plan_key] = plan
        
        # Try to match PDF analyses with plans
        for pdf_analysis in self.integrated_data['pdf_analyses']:
            potential_matches = self.find_matching_plans(pdf_analysis, unified_plans)
            
            for match_key in potential_matches:
                if match_key in unified_plans:
                    unified_plans[match_key]['pdf_analysis'] = pdf_analysis
        
        return {
            'unified_plans': list(unified_plans.values()),
            'cross_references': len([p for p in unified_plans.values() if 'pdf_analysis' in p]),
            'sources_summary': self.get_sources_summary()
        }
    
    def generate_plan_key(self, plan: Dict) -> str:
        """Generate unique key for plan identification"""
        municipality = plan.get('municipality', 'unknown').lower()
        title = plan.get('title', '').lower()
        plan_id = plan.get('plan_id', '')
        
        # Create composite key
        key_parts = [municipality]
        
        if plan_id:
            key_parts.append(plan_id)
        else:
            # Use title words for identification
            title_words = re.findall(r'\w+', title)[:3]
            key_parts.extend(title_words)
        
        return '_'.join(key_parts)
    
    def merge_plan_data(self, existing: Dict, new: Dict) -> Dict:
        """Merge plan data from different sources"""
        merged = existing.copy()
        
        # Add sources list
        if 'sources' not in merged:
            merged['sources'] = [existing.get('source', 'unknown')]
        
        if new.get('source') not in merged['sources']:
            merged['sources'].append(new.get('source', 'unknown'))
        
        # Merge non-empty fields
        for key, value in new.items():
            if key != 'source' and value and (key not in merged or not merged[key]):
                merged[key] = value
        
        return merged
    
    def find_matching_plans(self, pdf_analysis: Dict, unified_plans: Dict) -> List[str]:
        """Find plans that might match a PDF analysis"""
        matches = []
        
        pdf_municipality = pdf_analysis.get('municipality', '').lower()
        pdf_plan_id = pdf_analysis.get('plan_id', '')
        
        for plan_key, plan in unified_plans.items():
            plan_municipality = plan.get('municipality', '').lower()
            
            # Match by municipality and plan ID
            if (pdf_municipality in plan_municipality or plan_municipality in pdf_municipality) and pdf_plan_id:
                if pdf_plan_id in plan.get('plan_id', '') or pdf_plan_id in plan.get('title', ''):
                    matches.append(plan_key)
        
        return matches
    
    def get_sources_summary(self) -> Dict:
        """Get summary of data sources"""
        return {
            'geonorge': len([p for p in self.integrated_data['regulatory_plans'] if p.get('source') == 'geonorge']),
            'oslo_origo': len([p for p in self.integrated_data['regulatory_plans'] if p.get('source') == 'oslo_origo']),
            'pdf_analyses': len(self.integrated_data['pdf_analyses'])
        }
    
    def export_integrated_data(self, output_file: str = None) -> str:
        """Export integrated data to JSON"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'integrated_planning_data_{timestamp}.json'
        
        export_data = {
            'generated_at': datetime.now().isoformat(),
            'system_info': {
                'version': '1.0',
                'data_sources': list(self.data_sources.keys()),
                'processing_log_entries': len(self.integrated_data['processing_log'])
            },
            'data': self.integrated_data
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Integrated data exported to {output_file}")
        return output_file
    
    def generate_analysis_report(self) -> Dict:
        """Generate comprehensive analysis report"""
        unified_result = self.cross_reference_data()
        
        report = {
            'generation_time': datetime.now().isoformat(),
            'data_summary': {
                'total_plans': len(unified_result['unified_plans']),
                'sources_breakdown': self.get_sources_summary(),
                'cross_referenced_plans': unified_result['cross_references'],
                'municipalities_covered': len(set(
                    p.get('municipality', 'unknown') 
                    for p in unified_result['unified_plans']
                ))
            },
            'quality_metrics': {
                'plans_with_coordinates': len([
                    p for p in unified_result['unified_plans'] 
                    if p.get('coordinates') or (p.get('pdf_analysis', {}).get('coordinates'))
                ]),
                'plans_with_plan_id': len([
                    p for p in unified_result['unified_plans'] 
                    if p.get('plan_id')
                ]),
                'plans_with_pdf_data': len([
                    p for p in unified_result['unified_plans'] 
                    if 'pdf_analysis' in p
                ])
            },
            'processing_summary': self.integrated_data['processing_log'][-10:],  # Last 10 operations
            'recommendations': self.generate_recommendations(unified_result)
        }
        
        return report
    
    def generate_recommendations(self, unified_result: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        total_plans = len(unified_result['unified_plans'])
        cross_referenced = unified_result['cross_references']
        
        if total_plans == 0:
            recommendations.append("No planning data found - check data source configurations")
        
        if cross_referenced / total_plans < 0.3 if total_plans > 0 else False:
            recommendations.append("Low cross-reference rate - consider improving plan ID matching algorithms")
        
        oslo_plans = len([p for p in unified_result['unified_plans'] if 'oslo_origo' in p.get('sources', [])])
        if oslo_plans == 0:
            recommendations.append("No Oslo Origo data found - set up authentication with dataplattform@oslo.kommune.no")
        
        recommendations.append("Consider expanding to additional municipalities")
        recommendations.append("Implement automated monitoring for new plan publications")
        
        return recommendations

def main():
    print("🏗️ INTEGRATED PLANNING DATA SYSTEM")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize system
    system = IntegratedPlanningSystem()
    
    # Run integrated data collection
    print("\n=== PHASE 1: DATA COLLECTION ===")
    integrated_result = system.integrate_data_sources(municipality="Oslo")
    
    # Generate analysis report
    print("\n=== PHASE 2: ANALYSIS & CROSS-REFERENCING ===")
    report = system.generate_analysis_report()
    
    # Export data
    print("\n=== PHASE 3: DATA EXPORT ===")
    export_file = system.export_integrated_data()
    
    # Generate summary report
    report_file = f"integrated_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Display results
    print(f"\n=== RESULTS SUMMARY ===")
    print(f"📊 Total plans integrated: {report['data_summary']['total_plans']}")
    print(f"🔗 Cross-referenced plans: {report['data_summary']['cross_referenced_plans']}")
    print(f"🏘️ Municipalities covered: {report['data_summary']['municipalities_covered']}")
    print(f"📈 Quality metrics:")
    for metric, value in report['quality_metrics'].items():
        print(f"   - {metric}: {value}")
    
    print(f"\n📁 Files generated:")
    print(f"   - {export_file} (Complete integrated data)")
    print(f"   - {report_file} (Analysis report)")
    
    print(f"\n💡 Recommendations:")
    for rec in report['recommendations']:
        print(f"   - {rec}")
    
    print(f"\n✅ Integration complete!")

if __name__ == "__main__":
    main()