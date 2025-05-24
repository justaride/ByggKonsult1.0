#!/usr/bin/env python3
"""
Kartverket API Explorer
Utforske Kartverkets APIs og hente ned eksempel-reguleringsplaner
"""

import requests
import json
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
import os
from datetime import datetime

class KartverketAPIExplorer:
    def __init__(self):
        self.base_wfs_url = "https://wfs.geonorge.no/skwms1"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Kartverket-API-Explorer/1.0'
        })
    
    def test_wfs_endpoints(self):
        """Test forskjellige WFS endpoints for å finne reguleringsplaner"""
        potential_endpoints = [
            "wfs.reguleringsplaner",
            "wfs.arealplaner", 
            "wfs.plandata",
            "wfs.kommuneplaner",
            "wfs.plan"
        ]
        
        working_endpoints = []
        
        for endpoint in potential_endpoints:
            url = f"{self.base_wfs_url}/{endpoint}"
            params = {
                'service': 'WFS',
                'request': 'GetCapabilities',
                'version': '2.0.0'
            }
            
            try:
                print(f"Testing endpoint: {endpoint}")
                response = self.session.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    # Sjekk om responsen inneholder WFS capabilities
                    if 'WFS_Capabilities' in response.text or 'FeatureTypeList' in response.text:
                        working_endpoints.append({
                            'endpoint': endpoint,
                            'url': url,
                            'status': 'SUCCESS'
                        })
                        print(f"✓ {endpoint} - Working!")
                        
                        # Lagre capabilities for analyse
                        self.save_capabilities(endpoint, response.text)
                    else:
                        print(f"✗ {endpoint} - Not a valid WFS service")
                else:
                    print(f"✗ {endpoint} - HTTP {response.status_code}")
                    
            except requests.RequestException as e:
                print(f"✗ {endpoint} - Error: {e}")
        
        return working_endpoints
    
    def save_capabilities(self, endpoint_name, capabilities_xml):
        """Lagre WFS capabilities for senere analyse"""
        if not os.path.exists('capabilities'):
            os.makedirs('capabilities')
            
        filename = f"capabilities/{endpoint_name}_capabilities.xml"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(capabilities_xml)
        print(f"  Saved capabilities to {filename}")
    
    def parse_capabilities(self, capabilities_xml):
        """Parse WFS capabilities for å finne tilgjengelige feature types"""
        try:
            root = ET.fromstring(capabilities_xml)
            
            # Find all feature types
            feature_types = []
            
            # Handle different namespace patterns
            for ft in root.iter():
                if 'FeatureType' in ft.tag:
                    name_elem = ft.find('.//{*}Name')
                    title_elem = ft.find('.//{*}Title')
                    
                    if name_elem is not None:
                        feature_types.append({
                            'name': name_elem.text,
                            'title': title_elem.text if title_elem is not None else 'No title'
                        })
            
            return feature_types
            
        except ET.ParseError as e:
            print(f"Error parsing capabilities XML: {e}")
            return []
    
    def get_features(self, endpoint, feature_type, max_features=10):
        """Hent features fra en WFS endpoint"""
        url = f"{self.base_wfs_url}/{endpoint}"
        params = {
            'service': 'WFS',
            'request': 'GetFeature',
            'version': '2.0.0',
            'typeNames': feature_type,
            'count': max_features,
            'outputFormat': 'application/json'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                # Try JSON first
                try:
                    return response.json()
                except json.JSONDecodeError:
                    # Fall back to XML/GML
                    return response.text
            else:
                print(f"Error getting features: HTTP {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"Error getting features: {e}")
            return None
    
    def explore_known_endpoints(self):
        """Utforsk kjente working WFS endpoints fra Geonorge"""
        known_endpoints = [
            "wfs.elf-gn",
            "wfs.akvakulturlokaliteter", 
            "wfs.grunnskoler_vgs",
            "wfs.verneplanvassdrag",
            "wfs.sefrak"
        ]
        
        print("\n=== Exploring Known Working Endpoints ===")
        
        for endpoint in known_endpoints:
            print(f"\nExploring: {endpoint}")
            url = f"{self.base_wfs_url}/{endpoint}"
            params = {
                'service': 'WFS',
                'request': 'GetCapabilities',
                'version': '2.0.0'
            }
            
            try:
                response = self.session.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    feature_types = self.parse_capabilities(response.text)
                    print(f"  Found {len(feature_types)} feature types:")
                    for ft in feature_types[:3]:  # Show first 3
                        print(f"    - {ft['name']}: {ft['title']}")
                    if len(feature_types) > 3:
                        print(f"    ... and {len(feature_types) - 3} more")
                        
            except requests.RequestException as e:
                print(f"  Error: {e}")

def main():
    print("=== Kartverket API Explorer ===")
    print(f"Started at: {datetime.now()}")
    
    explorer = KartverketAPIExplorer()
    
    # Test potential regulatory plan endpoints
    print("\n1. Testing potential reguleringsplan endpoints...")
    working_endpoints = explorer.test_wfs_endpoints()
    
    # Explore known working endpoints to understand patterns
    explorer.explore_known_endpoints()
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Found {len(working_endpoints)} working endpoints for regulatory plans")
    for endpoint in working_endpoints:
        print(f"  - {endpoint['endpoint']}")
    
    if not working_endpoints:
        print("\nNo direct regulatory plan endpoints found.")
        print("This suggests that regulatory plans might be:")
        print("1. Part of a broader planning dataset")
        print("2. Available through municipality-specific endpoints")
        print("3. Require special authentication")
        print("4. Use different service patterns")

if __name__ == "__main__":
    main()