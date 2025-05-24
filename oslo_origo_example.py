#!/usr/bin/env python3
"""
Oslo Origo Dataplatform - Python Example
Eksempel på hvordan bruke Oslo's dataplatform
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
    
    print("\nNeste steg:")
    print("1. Sett environment variables (se oslo_origo_env_template.sh)")
    print("2. Kontakt dataplattform@oslo.kommune.no for tilgang")
    print("3. Test med okdata-cli: okdata datasets ls")
