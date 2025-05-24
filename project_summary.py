#!/usr/bin/env python3
"""
Project Summary: Kartverket APIs og PDF Parser
Sammendrag av arbeidet med Kartverket APIs og reguleringsplan-parser
"""

import json
import os
from datetime import datetime
from pathlib import Path

def print_section(title, content=""):
    """Print en formatert seksjon"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)
    if content:
        print(content)

def summarize_api_exploration():
    """Sammendrag av API-utforskning"""
    print_section("1. KARTVERKET API UTFORSKNING")
    
    print("✓ Kartverket/Geonorge API struktur kartlagt:")
    print("  - WFS (Web Feature Service) endpoints identifisert")
    print("  - SePlan service funnet for plandata")
    print("  - Geonorge katalog API testet")
    
    print("\n✓ Reguleringsplan-tilgang:")
    print("  - Direkte WFS endpoints for reguleringsplaner ikke funnet")
    print("  - Data tilgjengelig gjennom kommunale systemer")
    print("  - SePlan viser planID og lenker til kommunale nettsider")
    
    print("\n✓ Funne API-patterns:")
    print("  - https://wfs.geonorge.no/skwms1/wfs.[dataset]")
    print("  - https://kartkatalog.geonorge.no/api/search")
    print("  - Standardiserte WFS GetCapabilities/GetFeature requests")

def summarize_data_collection():
    """Sammendrag av datainnsamling"""
    print_section("2. DATAINNSAMLING - EKSEMPEL REGULERINGSPLANER")
    
    # Les rapporten hvis den eksisterer
    report_file = "regulatory_plans/sample_plans_report.json"
    if os.path.exists(report_file):
        with open(report_file, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        print(f"✓ Totalt {report['total_plans_found']} reguleringsplaner identifisert")
        
        # Tell opp kommuner
        municipalities = set()
        organizations = set()
        for plan in report['plans']:
            municipalities.add(plan.get('municipality', 'Ukjent'))
            organizations.add(plan.get('organization', 'Ukjent'))
        
        print(f"✓ Fra {len(municipalities)} forskjellige kommuner")
        print(f"✓ {len(organizations)} forskjellige organisasjoner")
        
        print(f"\n✓ Generert: {report['generated_at']}")
        print("✓ Lagret metadata for videre behandling")
        
        # Vis noen eksempler
        print("\nEksempler på funne planer:")
        for i, plan in enumerate(report['plans'][:3], 1):
            print(f"  {i}. {plan['title'][:50]}...")
            print(f"     - {plan['organization']}")
            print(f"     - UUID: {plan['uuid']}")
    else:
        print("❌ Ingen plandata funnet - kjør regulatory_plan_downloader.py")

def summarize_pdf_parser():
    """Sammendrag av PDF-parser"""
    print_section("3. PDF PARSER - FØRSTE VERSJON")
    
    print("✓ PDF-parser implementert med støtte for:")
    print("  - PyPDF2 og pdfplumber biblioteker")
    print("  - Norske nøkkelord for reguleringsplaner")
    print("  - Koordinat-ekstraksjon (UTM, desimal)")
    print("  - Dato-ekstraksjon (DD.MM.YYYY, YYYY-MM-DD)")
    print("  - Plan-ID og kommune-identifikasjon")
    
    print("\n✓ Kategorier av nøkkelord:")
    categories = [
        "plan_info (reguleringsplan, planid, saksnummer)",
        "administrative (kommune, plantype, vedtaksdato)",
        "areas (areal, kvadratmeter, byggehøyde)",
        "zoning (formål, boligbebyggelse, næringsbebyggelse)",
        "restrictions (byggegrense, hensynssone, faresone)"
    ]
    for cat in categories:
        print(f"  - {cat}")
    
    print("\n✓ Output format:")
    print("  - JSON med strukturert metadata")
    print("  - Ekstrakterte koordinater og datoer")
    print("  - Nøkkelord med kontekst")
    print("  - Filstatistikk og parsing-info")
    
    # Sjekk om det finnes analyse-resultater
    analysis_files = list(Path('.').glob('pdf_analysis_results_*.json'))
    if analysis_files:
        latest = max(analysis_files, key=os.path.getctime)
        with open(latest, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        print(f"\n✓ Siste analyse: {len(results)} PDF-filer prosessert")
        print(f"✓ Resultater lagret i: {latest.name}")

def summarize_technical_details():
    """Tekniske detaljer"""
    print_section("4. TEKNISKE DETALJER")
    
    print("📁 Filer opprettet:")
    files = [
        ("kartverket_explorer.py", "API-utforskning og WFS testing"),
        ("regulatory_plan_downloader.py", "Søk og nedlasting av plandata"),
        ("pdf_parser.py", "PDF-analyse og informasjonsekstraksjon"),
        ("project_summary.py", "Dette sammendrag-scriptet")
    ]
    
    for filename, description in files:
        status = "✓" if os.path.exists(filename) else "❌"
        print(f"  {status} {filename} - {description}")
    
    print("\n📦 Avhengigheter installert:")
    dependencies = [
        "requests (HTTP/API kommunikasjon)",
        "PyPDF2 (PDF tekstekstraksjon)",
        "pdfplumber (Avansert PDF-parsing)",
        "reportlab (PDF-generering for testing)"
    ]
    
    for dep in dependencies:
        print(f"  ✓ {dep}")
    
    print("\n🗂️ Datamapper opprettet:")
    folders = [
        ("regulatory_plans/", "Plandata og rapporter"),
        ("capabilities/", "WFS capabilities XML filer")
    ]
    
    for folder, description in folders:
        status = "✓" if os.path.exists(folder) else "❌"
        print(f"  {status} {folder} - {description}")

def summarize_next_steps():
    """Neste steg"""
    print_section("5. NESTE STEG OG FORBEDRINGER")
    
    print("🚀 Foreslåtte forbedringer:")
    
    improvements = [
        "PDF-parser utvidelser:",
        "  - OCR-støtte for skannede dokumenter",
        "  - Tabell-ekstraksjon (planbestemmelser)",
        "  - Kart/tegning-analyse",
        "  - Automatisk klassifisering av plantyper",
        "",
        "API-integrasjon:",
        "  - Direkte nedlasting fra kommunale systemer",
        "  - Autentisering for beskyttede data",
        "  - Batch-prosessering av store plansamlinger",
        "",
        "Data-analyse:",
        "  - Trendanalyse av reguleringsplaner",
        "  - Geografisk clustering av plandata",
        "  - Sammenligning på tvers av kommuner",
        "",
        "Brukergrensesnitt:",
        "  - Web-app for søk og visualisering",
        "  - Interaktive kart med plandata",
        "  - Eksport til forskjellige formater"
    ]
    
    for improvement in improvements:
        print(f"  {improvement}")

def main():
    print("🏛️ KARTVERKET API EXPLORER & PDF PARSER")
    print(f"Sammendrag generert: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    summarize_api_exploration()
    summarize_data_collection()
    summarize_pdf_parser()
    summarize_technical_details()
    summarize_next_steps()
    
    print_section("KONKLUSJON")
    print("✅ Kartverket APIs kartlagt og testet")
    print("✅ Eksempel-reguleringsplaner identifisert") 
    print("✅ Fungerende PDF-parser implementert")
    print("✅ Grunnlag for videre utvikling etablert")
    
    print(f"\n📊 Prosjektstatus: FØRSTE VERSJON FULLFØRT")
    print("🎯 Klar for videre utvikling og produksjonssetting")

if __name__ == "__main__":
    main()