#!/usr/bin/env python3
"""
Regulatory Plan Downloader
Henter ned eksempel-reguleringsplaner fra norske kommuner
"""

import requests
import json
import os
from datetime import datetime
from urllib.parse import urljoin, urlparse
import re

class RegulatoryPlanDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'RegulatoryPlanDownloader/1.0 (Educational Purpose)'
        })
        self.downloaded_plans = []
    
    def search_geonorge_api(self, query="reguleringsplan", limit=50):
        """Søk i Geonorge API etter reguleringsplaner"""
        api_url = "https://kartkatalog.geonorge.no/api/search"
        params = {
            'text': query,
            'limit': limit,
            'facets[0]name': 'type',
            'facets[0]value': 'dataset'
        }
        
        try:
            response = self.session.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error searching Geonorge API: {e}")
            return None
    
    def find_plan_documents(self, search_results):
        """Finn plan-dokumenter fra søkeresultater"""
        plan_documents = []
        
        if not search_results or 'Results' not in search_results:
            return plan_documents
            
        for result in search_results['Results']:
            title = result.get('Title', '')
            organization = result.get('Organization', '')
            uuid = result.get('Uuid', '')
            
            # Sjekk om dette er en reguleringsplan
            if any(keyword in title.lower() for keyword in ['reguleringsplan', 'detaljplan', 'områderegulering']):
                plan_info = {
                    'title': title,
                    'organization': organization,
                    'uuid': uuid,
                    'type': result.get('Type', ''),
                    'theme': result.get('Theme', []),
                    'purpose': result.get('Purpose', '')
                }
                
                # Prøv å finne lenker til dokumenter
                if 'DistributionDetails' in result:
                    distributions = result['DistributionDetails']
                    for dist in distributions:
                        if 'URL' in dist:
                            plan_info.setdefault('download_links', []).append({
                                'url': dist['URL'],
                                'protocol': dist.get('Protocol', ''),
                                'name': dist.get('Name', '')
                            })
                
                plan_documents.append(plan_info)
        
        return plan_documents
    
    def download_plan_metadata(self, uuid):
        """Last ned metadata for en spesifikk plan"""
        metadata_url = f"https://kartkatalog.geonorge.no/api/getdata/{uuid}"
        
        try:
            response = self.session.get(metadata_url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error downloading metadata for {uuid}: {e}")
            return None
    
    def find_sample_municipal_plans(self):
        """Finn eksempelplaner fra kjente kommuner"""
        sample_municipalities = [
            'Oslo',
            'Bergen', 
            'Stavanger',
            'Trondheim',
            'Kristiansand',
            'Drammen',
            'Tromsø'
        ]
        
        all_plans = []
        
        for municipality in sample_municipalities:
            print(f"\nSøker etter reguleringsplaner i {municipality}...")
            
            # Søk etter planer for denne kommunen
            search_query = f"reguleringsplan {municipality}"
            results = self.search_geonorge_api(search_query, limit=20)
            
            if results:
                plans = self.find_plan_documents(results)
                print(f"Fant {len(plans)} planer i {municipality}")
                
                for plan in plans:
                    plan['municipality'] = municipality
                    all_plans.append(plan)
                    print(f"  - {plan['title'][:80]}...")
            else:
                print(f"Ingen resultater for {municipality}")
        
        return all_plans
    
    def create_sample_plans_report(self, plans):
        """Lag en rapport over funne planer"""
        if not os.path.exists('regulatory_plans'):
            os.makedirs('regulatory_plans')
        
        report_file = 'regulatory_plans/sample_plans_report.json'
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_plans_found': len(plans),
            'plans': plans
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\nRapport lagret til: {report_file}")
        
        # Lag også en lesbar tekstrapport
        text_report_file = 'regulatory_plans/sample_plans_summary.txt'
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write("=== REGULERINGSPLANER - EKSEMPELSAMLING ===\n")
            f.write(f"Generert: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Totalt antall planer funnet: {len(plans)}\n\n")
            
            by_municipality = {}
            for plan in plans:
                municipality = plan.get('municipality', 'Ukjent')
                if municipality not in by_municipality:
                    by_municipality[municipality] = []
                by_municipality[municipality].append(plan)
            
            for municipality, muni_plans in by_municipality.items():
                f.write(f"\n--- {municipality} ({len(muni_plans)} planer) ---\n")
                for i, plan in enumerate(muni_plans, 1):
                    f.write(f"{i}. {plan['title']}\n")
                    f.write(f"   Organisasjon: {plan['organization']}\n")
                    f.write(f"   UUID: {plan['uuid']}\n")
                    if 'download_links' in plan:
                        f.write(f"   Nedlastingslenker: {len(plan['download_links'])}\n")
                    f.write("\n")
        
        print(f"Tekstrapport lagret til: {text_report_file}")
        return report_file, text_report_file

def main():
    print("=== Regulatory Plan Downloader ===")
    print(f"Started at: {datetime.now()}")
    
    downloader = RegulatoryPlanDownloader()
    
    # Søk etter eksempelplaner
    print("\n1. Søker etter eksempel-reguleringsplaner...")
    sample_plans = downloader.find_sample_municipal_plans()
    
    if sample_plans:
        print(f"\n=== RESULTATER ===")
        print(f"Totalt funnet {len(sample_plans)} reguleringsplaner")
        
        # Lag rapport
        report_file, text_file = downloader.create_sample_plans_report(sample_plans)
        
        # Vis noen eksempler
        print(f"\n=== EKSEMPLER ===")
        for i, plan in enumerate(sample_plans[:5], 1):
            print(f"{i}. {plan['title'][:60]}...")
            print(f"   Kommune: {plan.get('municipality', 'Ukjent')}")
            print(f"   Organisasjon: {plan['organization']}")
            if 'download_links' in plan:
                print(f"   Nedlastingslenker: {len(plan['download_links'])}")
        
        if len(sample_plans) > 5:
            print(f"   ... og {len(sample_plans) - 5} flere planer")
            
        print(f"\nSe full liste i: regulatory_plans/")
        
    else:
        print("Ingen reguleringsplaner funnet")

if __name__ == "__main__":
    main()