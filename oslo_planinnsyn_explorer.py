#!/usr/bin/env python3
"""
Oslo Kommune Planinnsyn Explorer
Dypere utforskning av Oslo's planinnsyn-system for reguleringsplaner
"""

import requests
import json
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

class OsloPlaninnsynExplorer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Oslo-Planinnsyn-Explorer/1.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8'
        })
        
        self.base_url = "https://od2.pbe.oslo.kommune.no/"
        self.findings = {
            'potential_apis': [],
            'data_endpoints': [],
            'planning_resources': [],
            'wfs_wms_services': []
        }
    
    def analyze_main_page(self):
        """Analyser hovedsiden for API-hint og lenker"""
        print("Analyserer Oslo planinnsyn hovedside...")
        
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            
            content = response.text
            
            # Søk etter JavaScript API-kall
            js_patterns = [
                r'ajax\s*:\s*["\']([^"\']+)["\']',
                r'url\s*:\s*["\']([^"\']+)["\']',
                r'service["\']?\s*:\s*["\']([^"\']+)["\']',
                r'endpoint["\']?\s*:\s*["\']([^"\']+)["\']'
            ]
            
            for pattern in js_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if match.startswith('/') or 'api' in match.lower():
                        self.findings['potential_apis'].append(match)
            
            # Søk etter WFS/WMS referanser
            geo_patterns = [
                r'wfs["\']?\s*:\s*["\']([^"\']+)["\']',
                r'wms["\']?\s*:\s*["\']([^"\']+)["\']',
                r'geoserver["\']?\s*:\s*["\']([^"\']+)["\']'
            ]
            
            for pattern in geo_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    self.findings['wfs_wms_services'].append(match)
            
            # Søk etter konfigurasjon objekter
            config_pattern = r'config\s*=\s*({[^}]+})'
            config_matches = re.findall(config_pattern, content, re.IGNORECASE)
            
            print(f"Funnet {len(self.findings['potential_apis'])} potensielle API-endpoints")
            print(f"Funnet {len(self.findings['wfs_wms_services'])} geo-service referanser")
            
            return content
            
        except requests.RequestException as e:
            print(f"Feil ved henting av hovedside: {e}")
            return None
    
    def test_common_gis_endpoints(self):
        """Test vanlige GIS API-endpoints"""
        print("\nTester vanlige GIS API-endpoints...")
        
        gis_endpoints = [
            "arcgis/rest/services",
            "arcgis/services",  
            "geoserver/wfs",
            "geoserver/wms",
            "geoserver/rest",
            "mapserver",
            "ows",
            "services/wfs",
            "services/wms",
            "rest/services",
            "api/v1",
            "api/v2",
            "webapi"
        ]
        
        working_gis_endpoints = []
        
        for endpoint in gis_endpoints:
            url = urljoin(self.base_url, endpoint)
            try:
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '').lower()
                    
                    endpoint_info = {
                        'url': url,
                        'status_code': response.status_code,
                        'content_type': content_type,
                        'content_length': len(response.content),
                        'potential_service_type': None
                    }
                    
                    # Analyser innhold
                    content = response.text.lower()
                    
                    if 'wfs' in content and ('getcapabilities' in content or 'getfeature' in content):
                        endpoint_info['potential_service_type'] = 'WFS'
                        print(f"✓ WFS service: {url}")
                        
                    elif 'wms' in content and ('getcapabilities' in content or 'getmap' in content):
                        endpoint_info['potential_service_type'] = 'WMS'
                        print(f"✓ WMS service: {url}")
                        
                    elif 'arcgis' in content or 'esri' in content:
                        endpoint_info['potential_service_type'] = 'ArcGIS REST'
                        print(f"✓ ArcGIS REST: {url}")
                        
                    elif any(indicator in content for indicator in ['json', 'api', 'rest']):
                        endpoint_info['potential_service_type'] = 'REST API'
                        print(f"✓ REST API: {url}")
                    
                    else:
                        print(f"✓ Unknown service: {url}")
                    
                    working_gis_endpoints.append(endpoint_info)
                
                elif response.status_code == 404:
                    print(f"✗ {url} - 404")
                else:
                    print(f"? {url} - {response.status_code}")
                    
            except requests.RequestException as e:
                print(f"✗ {url} - Error: {str(e)[:50]}...")
        
        self.findings['data_endpoints'] = working_gis_endpoints
        return working_gis_endpoints
    
    def test_wfs_getcapabilities(self):
        """Test WFS GetCapabilities på potensielle endpoints"""
        print("\nTester WFS GetCapabilities...")
        
        potential_wfs_bases = [
            self.base_url + "geoserver",
            self.base_url + "ows",
            self.base_url + "wfs",
            self.base_url + "services/wfs"
        ]
        
        for base_url in potential_wfs_bases:
            params = {
                'service': 'WFS',
                'request': 'GetCapabilities',
                'version': '2.0.0'
            }
            
            try:
                response = self.session.get(base_url, params=params, timeout=15)
                
                if response.status_code == 200:
                    content = response.text
                    
                    # Sjekk om det er gyldig WFS capabilities
                    if 'WFS_Capabilities' in content or 'FeatureTypeList' in content:
                        print(f"✓ Gyldig WFS capabilities: {base_url}")
                        
                        # Parse capabilities for feature types
                        try:
                            feature_types = self.parse_wfs_capabilities(content)
                            print(f"  Fant {len(feature_types)} feature types")
                            
                            # Søk etter planrelevante feature types
                            plan_features = [ft for ft in feature_types if 
                                           any(keyword in ft['name'].lower() 
                                               for keyword in ['plan', 'regulering', 'areal', 'bygge'])]
                            
                            if plan_features:
                                print(f"  🎯 {len(plan_features)} planrelevante feature types:")
                                for ft in plan_features[:3]:
                                    print(f"    - {ft['name']}: {ft['title']}")
                                
                                self.findings['planning_resources'].extend(plan_features)
                        
                        except Exception as e:
                            print(f"  Feil ved parsing av capabilities: {e}")
                    
                    else:
                        print(f"✗ Ikke gyldig WFS capabilities: {base_url}")
                
                else:
                    print(f"✗ {base_url} - {response.status_code}")
                    
            except requests.RequestException as e:
                print(f"✗ {base_url} - Error: {str(e)[:50]}...")
    
    def parse_wfs_capabilities(self, capabilities_xml):
        """Parse WFS capabilities XML"""
        try:
            root = ET.fromstring(capabilities_xml)
            feature_types = []
            
            # Handle different namespace patterns
            for ft in root.iter():
                if 'FeatureType' in ft.tag:
                    name_elem = ft.find('.//{*}Name')
                    title_elem = ft.find('.//{*}Title')
                    
                    if name_elem is not None:
                        feature_types.append({
                            'name': name_elem.text or 'Unknown',
                            'title': title_elem.text if title_elem is not None else 'No title'
                        })
            
            return feature_types
            
        except ET.ParseError as e:
            print(f"XML Parse error: {e}")
            return []
    
    def search_for_plan_apis(self):
        """Søk spesifikt etter plan-relaterte API-er"""
        print("\nSøker etter plan-spesifikke API-er...")
        
        plan_endpoints = [
            "api/plan",
            "api/planer",
            "api/regulering", 
            "api/reguleringsplan",
            "api/arealplan",
            "plan/api",
            "regulering/api",
            "rest/plan",
            "rest/planer",
            "plandata",
            "planregister"
        ]
        
        plan_apis_found = []
        
        for endpoint in plan_endpoints:
            url = urljoin(self.base_url, endpoint)
            
            try:
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    
                    api_info = {
                        'url': url,
                        'status_code': response.status_code,
                        'content_type': content_type,
                        'size': len(response.content)
                    }
                    
                    # Analyser for JSON API
                    if 'json' in content_type:
                        try:
                            json_data = response.json()
                            api_info['json_response'] = True
                            api_info['sample_data'] = str(json_data)[:200]
                            print(f"✓ JSON API funnet: {url}")
                        except:
                            pass
                    
                    plan_apis_found.append(api_info)
                    print(f"✓ Plan endpoint: {url} ({response.status_code})")
                
            except requests.RequestException:
                pass
        
        return plan_apis_found
    
    def create_comprehensive_report(self):
        """Lag en omfattende rapport"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'base_url': self.base_url,
            'summary': {
                'potential_apis': len(self.findings['potential_apis']),
                'data_endpoints': len(self.findings['data_endpoints']),
                'planning_resources': len(self.findings['planning_resources']),
                'wfs_wms_services': len(self.findings['wfs_wms_services'])
            },
            'findings': self.findings
        }
        
        # Lagre rapport
        with open('oslo_planinnsyn_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report

def main():
    print("=== OSLO PLANINNSYN EXPLORER ===")
    print(f"Startet: {datetime.now()}")
    
    explorer = OsloPlaninnsynExplorer()
    
    # 1. Analyser hovedside
    main_content = explorer.analyze_main_page()
    
    # 2. Test GIS endpoints
    gis_endpoints = explorer.test_common_gis_endpoints()
    
    # 3. Test WFS capabilities
    explorer.test_wfs_getcapabilities()
    
    # 4. Søk etter plan-spesifikke API-er
    plan_apis = explorer.search_for_plan_apis()
    
    # 5. Lag rapport
    report = explorer.create_comprehensive_report()
    
    # Vis sammendrag
    print(f"\n=== SAMMENDRAG ===")
    print(f"🔍 Potensielle API-er: {report['summary']['potential_apis']}")
    print(f"🌐 Data endpoints: {report['summary']['data_endpoints']}")
    print(f"🏗️ Planressurser: {report['summary']['planning_resources']}")
    print(f"🗺️ GIS services: {report['summary']['wfs_wms_services']}")
    
    if report['summary']['planning_resources'] > 0:
        print(f"\n🎯 Funnet plandata! Se oslo_planinnsyn_analysis.json")
    
    print(f"\n📄 Detaljert rapport: oslo_planinnsyn_analysis.json")

if __name__ == "__main__":
    main()