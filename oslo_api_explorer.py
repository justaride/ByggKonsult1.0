#!/usr/bin/env python3
"""
Oslo Kommune API Explorer
Utforske Oslo kommunes Origo dataplatform og søke etter reguleringsplandata
"""

import requests
import json
import os
from datetime import datetime
from urllib.parse import urljoin

class OsloAPIExplorer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Oslo-API-Explorer/1.0 (Educational Research)'
        })
        
        # Potensielle Oslo kommune API endpoints
        self.endpoints = {
            'statistics': 'https://statistikkbanken.oslo.kommune.no/',
            'planinnsyn': 'https://od2.pbe.oslo.kommune.no/',
            'github_okdata': 'https://api.github.com/repos/oslokommune/okdata-sdk-python',
            'data_norge': 'https://data.norge.no/api/dcat/datasets'
        }
        
        self.discovered_apis = []
    
    def search_data_norge_oslo(self):
        """Søk etter Oslo kommune datasett på data.norge.no"""
        print("Søker etter Oslo kommune datasett på data.norge.no...")
        
        try:
            params = {
                'q': 'Oslo kommune reguleringsplan',
                'size': 50
            }
            
            response = self.session.get(self.endpoints['data_norge'], params=params)
            response.raise_for_status()
            
            data = response.json()
            
            oslo_datasets = []
            if 'hits' in data and 'hits' in data['hits']:
                for hit in data['hits']['hits']:
                    source = hit['_source']
                    
                    # Sjekk om det er relatert til Oslo
                    title = source.get('title', {}).get('nb', '')
                    publisher = source.get('publisher', {}).get('name', '')
                    
                    if 'oslo' in title.lower() or 'oslo' in publisher.lower():
                        dataset_info = {
                            'title': title,
                            'publisher': publisher,
                            'description': source.get('description', {}).get('nb', '')[:200],
                            'id': source.get('id', ''),
                            'themes': source.get('theme', []),
                            'keywords': source.get('keyword', [])
                        }
                        
                        # Søk spesifikt etter plandata
                        text_content = f"{title} {dataset_info['description']}".lower()
                        if any(keyword in text_content for keyword in ['plan', 'regulering', 'areal', 'kart']):
                            dataset_info['relevant_for_planning'] = True
                        
                        oslo_datasets.append(dataset_info)
            
            print(f"Fant {len(oslo_datasets)} Oslo-relaterte datasett")
            
            # Vis planrelevante datasett
            plan_datasets = [d for d in oslo_datasets if d.get('relevant_for_planning')]
            print(f"Av disse er {len(plan_datasets)} potensielt relevante for plandata")
            
            return oslo_datasets
            
        except requests.RequestException as e:
            print(f"Feil ved søk på data.norge.no: {e}")
            return []
    
    def explore_github_okdata(self):
        """Utforsk Oslo kommunes okdata GitHub repo"""
        print("\nUtforsker Oslo kommunes okdata GitHub repository...")
        
        try:
            # Hent repo info
            response = self.session.get(self.endpoints['github_okdata'])
            response.raise_for_status()
            
            repo_data = response.json()
            
            print(f"Repository: {repo_data['name']}")
            print(f"Beskrivelse: {repo_data['description']}")
            print(f"Sist oppdatert: {repo_data['updated_at']}")
            
            # Hent README
            readme_url = f"https://api.github.com/repos/oslokommune/okdata-sdk-python/readme"
            readme_response = self.session.get(readme_url)
            
            if readme_response.status_code == 200:
                readme_data = readme_response.json()
                
                # README er base64-kodet
                import base64
                readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
                
                # Lagre README for analyse
                with open('oslo_okdata_readme.md', 'w', encoding='utf-8') as f:
                    f.write(readme_content)
                
                print("✓ README lastet ned og lagret som oslo_okdata_readme.md")
                
                # Søk etter API endpoints i README
                lines = readme_content.lower().split('\n')
                api_hints = []
                for line in lines:
                    if any(word in line for word in ['http', 'api', 'endpoint', 'url']):
                        api_hints.append(line.strip())
                
                if api_hints:
                    print(f"Funnet {len(api_hints)} potensielle API-referanser i README")
                
            return repo_data
            
        except requests.RequestException as e:
            print(f"Feil ved GitHub API kall: {e}")
            return None
    
    def test_planinnsyn_endpoints(self):
        """Test forskjellige endpoints på planinnsyn-systemet"""
        print("\nTester Oslo planinnsyn endpoints...")
        
        base_url = "https://od2.pbe.oslo.kommune.no/"
        
        test_paths = [
            "",
            "api/",
            "rest/",
            "services/",
            "kart/",
            "plan/",
            "data/",
            "geoserver/",
            "wfs/",
            "wms/"
        ]
        
        working_endpoints = []
        
        for path in test_paths:
            url = urljoin(base_url, path)
            try:
                response = self.session.get(url, timeout=10)
                
                status_info = {
                    'url': url,
                    'status_code': response.status_code,
                    'content_type': response.headers.get('content-type', ''),
                    'content_length': len(response.content)
                }
                
                if response.status_code == 200:
                    working_endpoints.append(status_info)
                    print(f"✓ {url} - {response.status_code}")
                    
                    # Sjekk for API-indikatorer
                    content_lower = response.text.lower()
                    if any(indicator in content_lower for indicator in ['api', 'json', 'xml', 'wfs', 'wms']):
                        status_info['potential_api'] = True
                        print(f"  → Potensielt API funnet!")
                
                else:
                    print(f"✗ {url} - {response.status_code}")
                    
            except requests.RequestException as e:
                print(f"✗ {url} - Error: {e}")
        
        return working_endpoints
    
    def search_for_origo_endpoints(self):
        """Søk etter Origo dataplatform endpoints"""
        print("\nSøker etter Origo dataplatform endpoints...")
        
        potential_origo_domains = [
            "https://data.oslo.no/",
            "https://origo.oslo.no/",
            "https://dataplatform.oslo.no/",
            "https://api.oslo.no/",
            "https://opendata.oslo.no/"
        ]
        
        for domain in potential_origo_domains:
            try:
                response = self.session.get(domain, timeout=10)
                print(f"{domain} - Status: {response.status_code}")
                
                if response.status_code == 200:
                    # Sjekk innhold for API-indikatorer
                    content = response.text.lower()
                    if any(indicator in content for indicator in ['origo', 'dataplatform', 'api']):
                        print(f"  → Potensielt Origo platform funnet!")
                        
            except requests.RequestException as e:
                print(f"{domain} - Error: {str(e)[:50]}...")
    
    def create_report(self, data_norge_results, github_data, planinnsyn_endpoints):
        """Lag en rapport over funne API-er"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'data_norge_datasets': len(data_norge_results),
                'plan_relevant_datasets': len([d for d in data_norge_results if d.get('relevant_for_planning')]),
                'working_planinnsyn_endpoints': len(planinnsyn_endpoints),
                'github_repo_analyzed': github_data is not None
            },
            'data_norge_results': data_norge_results,
            'github_analysis': github_data,
            'planinnsyn_endpoints': planinnsyn_endpoints
        }
        
        # Lagre rapport
        with open('oslo_api_exploration_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report

def main():
    print("=== OSLO KOMMUNE API EXPLORER ===")
    print(f"Startet: {datetime.now()}")
    
    explorer = OsloAPIExplorer()
    
    # 1. Søk på data.norge.no
    data_norge_results = explorer.search_data_norge_oslo()
    
    # 2. Utforsk GitHub okdata repo
    github_data = explorer.explore_github_okdata()
    
    # 3. Test planinnsyn endpoints
    planinnsyn_endpoints = explorer.test_planinnsyn_endpoints()
    
    # 4. Søk etter Origo endpoints
    explorer.search_for_origo_endpoints()
    
    # 5. Lag rapport
    report = explorer.create_report(data_norge_results, github_data, planinnsyn_endpoints)
    
    # Vis sammendrag
    print(f"\n=== SAMMENDRAG ===")
    print(f"📊 Data.norge.no: {report['summary']['data_norge_datasets']} Oslo-datasett funnet")
    print(f"🏗️ Planrelevante: {report['summary']['plan_relevant_datasets']} datasett")
    print(f"🌐 Planinnsyn endpoints: {report['summary']['working_planinnsyn_endpoints']} working")
    print(f"💻 GitHub repo: {'✓' if report['summary']['github_repo_analyzed'] else '✗'}")
    
    print(f"\n📄 Rapport lagret som: oslo_api_exploration_report.json")
    
    if report['summary']['plan_relevant_datasets'] > 0:
        print(f"\n🎯 Funnet planrelevante datasett! Se rapporten for detaljer.")

if __name__ == "__main__":
    main()