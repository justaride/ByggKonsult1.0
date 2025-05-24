#!/usr/bin/env python3
"""
Oslo Origo Dataplatform Setup Guide
Guide for å komme i gang med Oslo kommunes Origo dataplatform
"""

import os
import json
from datetime import datetime

class OsloOrigoSetup:
    def __init__(self):
        self.platform_info = {
            'name': 'Oslo Origo Dataplatform',
            'sdk': 'okdata-sdk',
            'cli': 'okdata-cli',
            'contact': 'dataplattform@oslo.kommune.no',
            'auth_methods': ['client_credentials', 'username_password', 'api_key'],
            'environments': ['dev', 'prod']
        }
    
    def check_sdk_installation(self):
        """Sjekk om Oslo SDK er installert"""
        print("=== SJEKKER OSLO SDK INSTALLASJON ===")
        
        try:
            import okdata
            print("✓ okdata-sdk er installert")
            return True
        except ImportError:
            print("✗ okdata-sdk er IKKE installert")
            print("Installer med: pip install okdata-sdk")
            return False
    
    def install_oslo_sdk(self):
        """Installer Oslo SDK"""
        print("\n=== INSTALLERER OSLO SDK ===")
        
        import subprocess
        import sys
        
        packages = ['okdata-sdk', 'okdata-cli']
        
        for package in packages:
            try:
                print(f"Installerer {package}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✓ {package} installert")
            except subprocess.CalledProcessError as e:
                print(f"✗ Feil ved installasjon av {package}: {e}")
    
    def create_config_template(self):
        """Lag konfigurasjonsmaler"""
        print("\n=== LAGER KONFIGURASJONSMALER ===")
        
        # Environment variables template
        env_template = """# Oslo Origo Dataplatform Environment Variables
# Legg disse i din .bashrc, .zshrc eller .env fil

# Metode 1: Client Credentials (for automatiserte systemer)
export OKDATA_CLIENT_ID=your-client-id
export OKDATA_CLIENT_SECRET=your-client-secret

# Metode 2: Username/Password (AD-brukere)
export OKDATA_USERNAME=your-oslo-ad-username
export OKDATA_PASSWORD=your-oslo-ad-password

# Metode 3: API Key (for events)
export OKDATA_API_KEY=your-api-key

# Environment (dev eller prod)
export OKDATA_ENVIRONMENT=dev

# For debugging
export OKDATA_CACHE_CREDENTIALS=false
"""
        
        with open('oslo_origo_env_template.sh', 'w') as f:
            f.write(env_template)
        
        print("✓ Environment template: oslo_origo_env_template.sh")
        
        # Python config template
        python_template = '''#!/usr/bin/env python3
"""
Oslo Origo Dataplatform - Python Example
Eksempel på hvordan bruke Oslo\'s dataplatform
"""

from okdata.sdk.config import Config
from okdata.sdk.data.dataset import Dataset
from okdata.sdk.data.download import Download

def setup_oslo_config():
    """Sett opp Oslo konfigurasjon"""
    # Automatisk konfigurasjon fra environment variables
    config = Config(env="dev")  # eller "prod"
    
    # Eventuelt override av instillinger
    config.config["cacheCredentials"] = False
    
    return config

def list_available_datasets():
    """List tilgjengelige datasett (krever autentisering)"""
    try:
        config = setup_oslo_config()
        dataset_client = Dataset(config=config)
        
        # Dette vil liste dine datasett
        # datasets = dataset_client.get_datasets()
        print("Datasett-listing krever gyldig autentisering")
        
    except Exception as e:
        print(f"Feil: {e}")
        print("Sjekk at OKDATA_* environment variables er satt")

def download_public_dataset_example():
    """Eksempel på nedlasting av offentlig datasett"""
    try:
        # For offentlige datasett trengs ikke autentisering
        config = Config(env="dev")
        downloader = Download(config=config)
        
        # Eksempel dataset (må finnes)
        dataset_id = "example-public-dataset"
        version = "1"
        edition = "latest"
        
        # result = downloader.download(dataset_id, version, edition, "./downloads/")
        print("Eksempel klar for nedlasting av offentlige datasett")
        
    except Exception as e:
        print(f"Feil: {e}")

def search_planning_datasets():
    """Søk etter planrelaterte datasett"""
    # Dette vil kreve tilgang til katalog-API
    planning_keywords = [
        "reguleringsplan",
        "detaljplan", 
        "områderegulering",
        "plandata",
        "arealplan"
    ]
    
    print("Søkebegreper for plandata:")
    for keyword in planning_keywords:
        print(f"  - {keyword}")

if __name__ == "__main__":
    print("=== OSLO ORIGO DATAPLATFORM EKSEMPEL ===")
    
    # Test konfigurasjon
    try:
        config = setup_oslo_config()
        print("✓ Konfigurasjon opprettet")
    except Exception as e:
        print(f"✗ Konfigurasjonsfeil: {e}")
    
    # Vis søkebegreper
    search_planning_datasets()
    
    print("\\nNeste steg:")
    print("1. Sett environment variables (se oslo_origo_env_template.sh)")
    print("2. Kontakt dataplattform@oslo.kommune.no for tilgang")
    print("3. Test med okdata-cli: okdata datasets ls")
'''
        
        with open('oslo_origo_example.py', 'w') as f:
            f.write(python_template)
        
        print("✓ Python example: oslo_origo_example.py")
    
    def create_access_guide(self):
        """Lag tilgangsguide"""
        print("\n=== LAGER TILGANGSGUIDE ===")
        
        guide = {
            'title': 'Oslo Origo Dataplatform - Tilgangsguide',
            'generated_at': datetime.now().isoformat(),
            'platform_info': self.platform_info,
            'steps': {
                '1_installation': {
                    'description': 'Installer Oslo SDK',
                    'commands': [
                        'pip install okdata-sdk',
                        'pip install okdata-cli'
                    ]
                },
                '2_authentication': {
                    'description': 'Sett opp autentisering',
                    'options': {
                        'client_credentials': {
                            'description': 'For automatiserte systemer',
                            'contact': 'dataplattform@oslo.kommune.no',
                            'env_vars': ['OKDATA_CLIENT_ID', 'OKDATA_CLIENT_SECRET']
                        },
                        'username_password': {
                            'description': 'For AD-brukere (Oslo ansatte)',
                            'env_vars': ['OKDATA_USERNAME', 'OKDATA_PASSWORD']
                        },
                        'api_key': {
                            'description': 'For events og spesifikke tjenester',
                            'env_vars': ['OKDATA_API_KEY']
                        }
                    }
                },
                '3_configuration': {
                    'description': 'Konfigurer environment',
                    'env_vars': {
                        'OKDATA_ENVIRONMENT': 'dev eller prod',
                        'OKDATA_CACHE_CREDENTIALS': 'true/false'
                    }
                },
                '4_testing': {
                    'description': 'Test tilkobling',
                    'commands': [
                        'okdata datasets ls',
                        'okdata --help'
                    ]
                }
            },
            'planning_data_strategy': {
                'description': 'Strategi for å finne reguleringsplandata',
                'approaches': [
                    'Søk i datasett-katalogen etter plan-nøkkelord',
                    'Kontakt dataplattform-teamet for planspesifikk veiledning',
                    'Utforsk offentlige datasett først',
                    'Kombiner med nasjonale tjenester (Geonorge)'
                ]
            },
            'next_steps': [
                'Installer okdata-sdk og okdata-cli',
                'Kontakt dataplattform@oslo.kommune.no for tilgang',
                'Test med dev-environment først',
                'Utforsk tilgjengelige datasett',
                'Dokumenter funne plandata-kilder'
            ]
        }
        
        with open('oslo_origo_access_guide.json', 'w', encoding='utf-8') as f:
            json.dump(guide, f, indent=2, ensure_ascii=False)
        
        print("✓ Tilgangsguide: oslo_origo_access_guide.json")
        
        return guide
    
    def summarize_findings(self):
        """Sammendrag av funn"""
        print("\n=== SAMMENDRAG: OSLO KOMMUNE API-ER ===")
        
        findings = {
            'origo_dataplatform': {
                'status': 'Identifisert og dokumentert',
                'access_method': 'SDK + CLI + Environment variables',
                'authentication': 'Multiple methods available',
                'contact': 'dataplattform@oslo.kommune.no'
            },
            'planinnsyn_system': {
                'status': 'Kartlagt - ikke standard API',
                'observation': 'Tradisjonell web-app uten eksponerte API-er',
                'recommendation': 'Bruk Origo eller nasjonale tjenester'
            },
            'recommended_approach': [
                '1. Start med Oslo Origo dataplatform',
                '2. Kombiner med nasjonale Geonorge API-er',
                '3. Kontakt Oslo kommune for planspesifikk veiledning'
            ]
        }
        
        for key, info in findings.items():
            print(f"\n{key.replace('_', ' ').title()}:")
            if isinstance(info, dict):
                for subkey, value in info.items():
                    print(f"  {subkey}: {value}")
            elif isinstance(info, list):
                for item in info:
                    print(f"  - {item}")

def main():
    print("🏛️ OSLO KOMMUNE - ORIGO DATAPLATFORM SETUP")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    setup = OsloOrigoSetup()
    
    # Sjekk installasjon
    sdk_installed = setup.check_sdk_installation()
    
    if not sdk_installed:
        print("\n→ Oslo SDK kan installeres med: pip install okdata-sdk okdata-cli")
        # setup.install_oslo_sdk()  # Uncomment to auto-install
    
    # Lag konfigurasjonstemplateer
    setup.create_config_template()
    
    # Lag tilgangsguide
    guide = setup.create_access_guide()
    
    # Sammendrag
    setup.summarize_findings()
    
    print(f"\n✅ Setup komplett!")
    print(f"📁 Filer opprettet:")
    print(f"  - oslo_origo_env_template.sh")
    print(f"  - oslo_origo_example.py") 
    print(f"  - oslo_origo_access_guide.json")
    
    print(f"\n🚀 Neste steg:")
    print(f"  1. Kontakt: dataplattform@oslo.kommune.no")
    print(f"  2. Sett environment variables")
    print(f"  3. Test: okdata datasets ls")

if __name__ == "__main__":
    main()