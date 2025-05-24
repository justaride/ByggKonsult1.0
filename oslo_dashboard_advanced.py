#!/usr/bin/env python3
"""
Oslo Dashboard Advanced Features
Demonstrasjon av spesifikke features og interaktiv funksjonalitet
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import webbrowser
import random

class OsloDashboardAdvanced:
    def __init__(self, oslo_data_file: str = None):
        self.oslo_data_file = oslo_data_file or self.find_latest_oslo_data()
        self.oslo_data = self.load_oslo_data()
        
        # Simulerte real-time data for demo
        self.demo_mode = True
        
        # Oslo-spesifikke områder med demo data
        self.oslo_areas_with_data = {
            'Sentrum': {'plans': 15, 'last_update': '2025-05-20', 'status': 'active'},
            'Grünerløkka': {'plans': 8, 'last_update': '2025-05-18', 'status': 'active'},
            'Frogner': {'plans': 12, 'last_update': '2025-05-22', 'status': 'active'},
            'Gamle Oslo': {'plans': 6, 'last_update': '2025-05-15', 'status': 'active'},
            'St. Hanshaugen': {'plans': 4, 'last_update': '2025-05-10', 'status': 'pending'},
            'Sagene': {'plans': 7, 'last_update': '2025-05-19', 'status': 'active'},
            'Ullern': {'plans': 3, 'last_update': '2025-05-12', 'status': 'pending'},
            'Vestre Aker': {'plans': 5, 'last_update': '2025-05-14', 'status': 'active'},
            'Nordre Aker': {'plans': 2, 'last_update': '2025-05-08', 'status': 'inactive'},
            'Bjerke': {'plans': 1, 'last_update': '2025-05-05', 'status': 'inactive'},
            'Grorud': {'plans': 3, 'last_update': '2025-05-16', 'status': 'pending'},
            'Stovner': {'plans': 2, 'last_update': '2025-05-11', 'status': 'inactive'},
            'Alna': {'plans': 4, 'last_update': '2025-05-17', 'status': 'active'},
            'Østensjø': {'plans': 6, 'last_update': '2025-05-21', 'status': 'active'},
            'Nordstrand': {'plans': 3, 'last_update': '2025-05-13', 'status': 'pending'},
            'Søndre Nordstrand': {'plans': 2, 'last_update': '2025-05-09', 'status': 'inactive'}
        }
        
    def find_latest_oslo_data(self) -> str:
        """Finn siste Oslo data fil"""
        oslo_files = list(Path('.').glob('oslo_planning_data_*.json'))
        if oslo_files:
            latest = max(oslo_files, key=os.path.getctime)
            return str(latest)
        return None
    
    def load_oslo_data(self) -> dict:
        """Last inn Oslo plandata"""
        if not self.oslo_data_file or not os.path.exists(self.oslo_data_file):
            return {'oslo_data': {'origo_datasets': [], 'reguleringsplaner': [], 'pdf_documents': []}}
        
        with open(self.oslo_data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_advanced_dashboard_html(self) -> str:
        """Generer avansert dashboard med interaktive features"""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oslo Planning Dashboard - Advanced Features</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .oslo-header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        
        .oslo-logo {{
            font-size: 4em;
            margin-bottom: 10px;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        .oslo-title {{
            font-size: 2.8em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .live-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #4CAF50;
            border-radius: 50%;
            margin-left: 10px;
            animation: blink 1s infinite;
        }}
        
        @keyframes blink {{
            0%, 50% {{ opacity: 1; }}
            51%, 100% {{ opacity: 0.3; }}
        }}
        
        .dashboard-container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .feature-tabs {{
            display: flex;
            background: #f8f9fa;
            border-bottom: 1px solid #ddd;
        }}
        
        .tab-button {{
            flex: 1;
            padding: 15px 20px;
            border: none;
            background: none;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            color: #666;
            transition: all 0.3s ease;
        }}
        
        .tab-button.active {{
            background: #1e3c72;
            color: white;
        }}
        
        .tab-button:hover {{
            background: #e9ecef;
        }}
        
        .tab-button.active:hover {{
            background: #2a5298;
        }}
        
        .tab-content {{
            padding: 30px;
            min-height: 600px;
        }}
        
        .tab-panel {{
            display: none;
        }}
        
        .tab-panel.active {{
            display: block;
        }}
        
        .interactive-map {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        
        .bydel-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: all 0.3s ease;
            border-left: 5px solid #ddd;
            position: relative;
            overflow: hidden;
        }}
        
        .bydel-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .bydel-card.active {{
            border-left-color: #4CAF50;
            background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);
        }}
        
        .bydel-card.pending {{
            border-left-color: #FF9800;
            background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
        }}
        
        .bydel-card.inactive {{
            border-left-color: #f44336;
            background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        }}
        
        .bydel-name {{
            font-weight: bold;
            color: #1e3c72;
            margin-bottom: 8px;
            font-size: 1.1em;
        }}
        
        .bydel-stats {{
            font-size: 0.9em;
            color: #666;
        }}
        
        .plan-count {{
            font-weight: bold;
            color: #2a5298;
            font-size: 1.2em;
        }}
        
        .status-indicator {{
            position: absolute;
            top: 10px;
            right: 10px;
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }}
        
        .status-active {{
            background: #4CAF50;
        }}
        
        .status-pending {{
            background: #FF9800;
        }}
        
        .status-inactive {{
            background: #f44336;
        }}
        
        .real-time-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #1e3c72, #2a5298);
        }}
        
        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            color: #1e3c72;
            margin-bottom: 10px;
            transition: all 0.5s ease;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 1.1em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .trend-indicator {{
            margin-top: 10px;
            font-size: 0.9em;
        }}
        
        .trend-up {{
            color: #4CAF50;
        }}
        
        .trend-down {{
            color: #f44336;
        }}
        
        .search-filter {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .search-input {{
            width: 100%;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1.1em;
            transition: border-color 0.3s ease;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: #1e3c72;
        }}
        
        .filter-buttons {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        
        .filter-btn {{
            padding: 8px 16px;
            border: 2px solid #1e3c72;
            border-radius: 20px;
            background: white;
            color: #1e3c72;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9em;
        }}
        
        .filter-btn.active {{
            background: #1e3c72;
            color: white;
        }}
        
        .notification-panel {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            max-height: 400px;
            overflow-y: auto;
        }}
        
        .notification {{
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #1e3c72;
            background: #f8f9fa;
            position: relative;
        }}
        
        .notification.new {{
            border-left-color: #4CAF50;
            background: #f8fff8;
            animation: slideIn 0.5s ease;
        }}
        
        @keyframes slideIn {{
            from {{ transform: translateX(-100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        .notification-time {{
            font-size: 0.8em;
            color: #666;
            position: absolute;
            top: 10px;
            right: 15px;
        }}
        
        .charts-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }}
        
        .chart-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .simple-chart {{
            height: 200px;
            background: linear-gradient(to top, #e3f2fd 0%, #bbdefb 100%);
            border-radius: 8px;
            position: relative;
            overflow: hidden;
        }}
        
        .chart-bars {{
            display: flex;
            align-items: end;
            height: 100%;
            padding: 20px;
            gap: 5px;
        }}
        
        .chart-bar {{
            flex: 1;
            background: linear-gradient(to top, #1e3c72, #2a5298);
            border-radius: 4px 4px 0 0;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .chart-bar:hover {{
            background: linear-gradient(to top, #2a5298, #4a90e2);
            transform: scaleY(1.1);
        }}
        
        .export-panel {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .export-buttons {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .export-btn {{
            padding: 15px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            transition: all 0.3s ease;
            text-align: center;
        }}
        
        .export-btn.primary {{
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
        }}
        
        .export-btn.secondary {{
            background: #f8f9fa;
            color: #1e3c72;
            border: 2px solid #1e3c72;
        }}
        
        .export-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
        }}
        
        .modal-content {{
            background: white;
            margin: 10% auto;
            padding: 30px;
            border-radius: 15px;
            width: 80%;
            max-width: 600px;
            position: relative;
            animation: modalSlideIn 0.3s ease;
        }}
        
        @keyframes modalSlideIn {{
            from {{ transform: translateY(-50px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
        .close {{
            position: absolute;
            right: 20px;
            top: 15px;
            font-size: 2em;
            cursor: pointer;
            color: #666;
        }}
        
        .close:hover {{
            color: #f44336;
        }}
        
        @media (max-width: 768px) {{
            .interactive-map {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .charts-container {{
                grid-template-columns: 1fr;
            }}
            
            .feature-tabs {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="oslo-header">
        <div class="oslo-logo">🏛️</div>
        <div class="oslo-title">
            Oslo Planning Dashboard
            <span class="live-indicator"></span>
        </div>
        <div style="font-size: 1.2em; opacity: 0.9;">
            Advanced Features Demo - Live Data
        </div>
        <div style="font-size: 0.9em; opacity: 0.7; margin-top: 10px;">
            Sist oppdatert: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
        </div>
    </div>
    
    <div class="dashboard-container">
        <div class="feature-tabs">
            <button class="tab-button active" onclick="showTab('overview')">📊 Oversikt</button>
            <button class="tab-button" onclick="showTab('map')">🗺️ Interaktivt Kart</button>
            <button class="tab-button" onclick="showTab('analytics')">📈 Analytics</button>
            <button class="tab-button" onclick="showTab('search')">🔍 Søk & Filter</button>
            <button class="tab-button" onclick="showTab('notifications')">🔔 Varsler</button>
            <button class="tab-button" onclick="showTab('export')">📤 Export</button>
        </div>
        
        <!-- Overview Tab -->
        <div id="overview" class="tab-content">
            <div class="tab-panel active">
                <h2 style="color: #1e3c72; margin-bottom: 20px;">📊 Real-time Oslo Oversikt</h2>
                
                <div class="real-time-stats">
                    <div class="stat-card">
                        <div class="stat-number" id="total-plans">49</div>
                        <div class="stat-label">Totale Planer</div>
                        <div class="trend-indicator trend-up">↗ +3 denne uken</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-number" id="active-areas">11</div>
                        <div class="stat-label">Aktive Bydeler</div>
                        <div class="trend-indicator trend-up">↗ +1 ny bydel</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-number" id="pending-plans">18</div>
                        <div class="stat-label">Ventende Planer</div>
                        <div class="trend-indicator trend-down">↘ -2 siden i går</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-number" id="completion-rate">69</div>
                        <div class="stat-label">% Fullført</div>
                        <div class="trend-indicator trend-up">↗ +5% denne måneden</div>
                    </div>
                </div>
                
                <div class="charts-container">
                    <div class="chart-card">
                        <h3 style="color: #1e3c72; margin-bottom: 15px;">Planer per Bydel</h3>
                        <div class="simple-chart">
                            <div class="chart-bars">
                                {self.generate_chart_bars()}
                            </div>
                        </div>
                    </div>
                    
                    <div class="chart-card">
                        <h3 style="color: #1e3c72; margin-bottom: 15px;">Trend Siste 7 Dager</h3>
                        <div class="simple-chart">
                            <div class="chart-bars">
                                {self.generate_trend_bars()}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Interactive Map Tab -->
        <div id="map" class="tab-content">
            <div class="tab-panel">
                <h2 style="color: #1e3c72; margin-bottom: 20px;">🗺️ Interaktivt Oslo Bydelskart</h2>
                <p style="margin-bottom: 20px;">Klikk på en bydel for å se detaljer. Farger indikerer status:</p>
                
                <div style="display: flex; gap: 20px; margin-bottom: 20px; flex-wrap: wrap;">
                    <div style="display: flex; align-items: center; gap: 5px;">
                        <div class="status-indicator status-active"></div>
                        <span>Aktiv (har plandata)</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 5px;">
                        <div class="status-indicator status-pending"></div>
                        <span>Venter (planlegging pågår)</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 5px;">
                        <div class="status-indicator status-inactive"></div>
                        <span>Inaktiv (mangler data)</span>
                    </div>
                </div>
                
                <div class="interactive-map">
                    {self.generate_interactive_bydel_cards()}
                </div>
            </div>
        </div>
        
        <!-- Analytics Tab -->
        <div id="analytics" class="tab-content">
            <div class="tab-panel">
                <h2 style="color: #1e3c72; margin-bottom: 20px;">📈 Oslo Planning Analytics</h2>
                
                <div class="search-filter">
                    <h3>📊 Dataanalyse Verktøy</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px;">
                        <div>
                            <h4>Plantyper</h4>
                            <ul style="margin-top: 10px;">
                                <li>Detaljregulering: 31 planer</li>
                                <li>Områderegulering: 12 planer</li>
                                <li>Planendring: 6 planer</li>
                            </ul>
                        </div>
                        <div>
                            <h4>Tidsperiode</h4>
                            <ul style="margin-top: 10px;">
                                <li>Siste 30 dager: 8 nye planer</li>
                                <li>Siste 90 dager: 23 nye planer</li>
                                <li>Siste år: 49 nye planer</li>
                            </ul>
                        </div>
                        <div>
                            <h4>Status Fordeling</h4>
                            <ul style="margin-top: 10px;">
                                <li>Vedtatte planer: 31 (63%)</li>
                                <li>Under behandling: 18 (37%)</li>
                                <li>Avslåtte: 0 (0%)</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Search & Filter Tab -->
        <div id="search" class="tab-content">
            <div class="tab-panel">
                <h2 style="color: #1e3c72; margin-bottom: 20px;">🔍 Søk & Filter Oslo Data</h2>
                
                <div class="search-filter">
                    <input type="text" class="search-input" placeholder="Søk i Oslo plandata... (f.eks. 'Grünerløkka', 'reguleringsplan', 'bolig')" 
                           oninput="searchOsloData(this.value)">
                    
                    <div class="filter-buttons">
                        <button class="filter-btn active" onclick="filterByType('all')">Alle</button>
                        <button class="filter-btn" onclick="filterByType('reguleringsplan')">Reguleringsplaner</button>
                        <button class="filter-btn" onclick="filterByType('origo')">Origo Data</button>
                        <button class="filter-btn" onclick="filterByType('pdf')">PDF Dokumenter</button>
                        <button class="filter-btn" onclick="filterByType('sentrum')">Sentrum</button>
                        <button class="filter-btn" onclick="filterByType('grünerløkka')">Grünerløkka</button>
                    </div>
                </div>
                
                <div id="search-results" style="margin-top: 20px;">
                    <div style="padding: 20px; text-align: center; color: #666;">
                        Skriv inn søkeord for å filtrere Oslo plandata...
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Notifications Tab -->
        <div id="notifications" class="tab-content">
            <div class="tab-panel">
                <h2 style="color: #1e3c72; margin-bottom: 20px;">🔔 Live Oslo Plandata Varsler</h2>
                
                <div class="notification-panel" id="notifications-list">
                    <div class="notification new">
                        <div class="notification-time">23.05.2025 15:30</div>
                        <strong>Ny reguleringsplan - Grünerløkka</strong><br>
                        Reguleringsplan for Thorvald Meyers gate 12-14 er publisert for offentlig ettersyn.
                    </div>
                    
                    <div class="notification">
                        <div class="notification-time">23.05.2025 14:15</div>
                        <strong>Origo Datasett Oppdatert</strong><br>
                        Oslo byggetillatelser datasett har fått 5 nye poster.
                    </div>
                    
                    <div class="notification">
                        <div class="notification-time">23.05.2025 12:45</div>
                        <strong>PBE System Status</strong><br>
                        Planinnsyn system er tilbake online etter vedlikehold.
                    </div>
                    
                    <div class="notification">
                        <div class="notification-time">23.05.2025 11:20</div>
                        <strong>Bydel Dekning Oppdatering</strong><br>
                        Nordre Aker bydel har nå 3 nye reguleringsplaner tilgjengelig.
                    </div>
                </div>
                
                <button onclick="addDemoNotification()" style="margin-top: 15px; padding: 10px 20px; background: #1e3c72; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    🔄 Simuler Nytt Varsel
                </button>
            </div>
        </div>
        
        <!-- Export Tab -->
        <div id="export" class="tab-content">
            <div class="tab-panel">
                <h2 style="color: #1e3c72; margin-bottom: 20px;">📤 Export Oslo Data</h2>
                
                <div class="export-panel">
                    <h3>Velg eksportformat:</h3>
                    
                    <div class="export-buttons">
                        <button class="export-btn primary" onclick="exportData('json')">
                            📄 JSON<br>
                            <small>Strukturerte data for API</small>
                        </button>
                        
                        <button class="export-btn primary" onclick="exportData('csv')">
                            📊 CSV<br>
                            <small>Excel-kompatibel tabell</small>
                        </button>
                        
                        <button class="export-btn secondary" onclick="exportData('pdf')">
                            📋 PDF Rapport<br>
                            <small>Formatert sammendrag</small>
                        </button>
                        
                        <button class="export-btn secondary" onclick="exportData('geojson')">
                            🗺️ GeoJSON<br>
                            <small>Geografiske data for GIS</small>
                        </button>
                    </div>
                    
                    <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
                        <h4>🔧 API Tilgang</h4>
                        <p>For live API tilgang til Oslo data:</p>
                        <code style="background: white; padding: 5px 10px; border-radius: 4px; display: block; margin: 10px 0;">
                            GET https://api.oslo-planning.no/v1/plans?format=json
                        </code>
                        <small>Krever API nøkkel fra Oslo kommune</small>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Modal for detaljer -->
    <div id="detail-modal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <div id="modal-content">
                <!-- Dynamisk innhold -->
            </div>
        </div>
    </div>
    
    <script>
        // Tab funksjonalitet
        function showTab(tabName) {{
            // Skjul alle tab panels
            document.querySelectorAll('.tab-panel').forEach(panel => {{
                panel.classList.remove('active');
            }});
            
            // Fjern active class fra alle buttons
            document.querySelectorAll('.tab-button').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            // Vis valgt tab
            document.getElementById(tabName).querySelector('.tab-panel').classList.add('active');
            event.target.classList.add('active');
        }}
        
        // Bydel kart interaksjon
        function showBydelDetails(bydelName, data) {{
            const modal = document.getElementById('detail-modal');
            const content = document.getElementById('modal-content');
            
            content.innerHTML = `
                <h2>🗺️ ${{bydelName}}</h2>
                <div style="margin: 20px 0;">
                    <p><strong>Antall planer:</strong> ${{data.plans}}</p>
                    <p><strong>Sist oppdatert:</strong> ${{data.last_update}}</p>
                    <p><strong>Status:</strong> ${{data.status}}</p>
                </div>
                <div style="margin-top: 30px;">
                    <h3>📋 Siste aktivitet:</h3>
                    <ul style="margin-top: 10px;">
                        <li>Reguleringsplan for ${{bydelName}} sentrum - Under behandling</li>
                        <li>Områderegulering boligområde - Vedtatt</li>
                        <li>Planendring for næringsområde - Høring</li>
                    </ul>
                </div>
                <button onclick="closeModal()" style="margin-top: 20px; padding: 10px 20px; background: #1e3c72; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    Lukk
                </button>
            `;
            
            modal.style.display = 'block';
        }}
        
        function closeModal() {{
            document.getElementById('detail-modal').style.display = 'none';
        }}
        
        // Søkefunksjonalitet
        function searchOsloData(query) {{
            const resultsDiv = document.getElementById('search-results');
            
            if (query.length < 2) {{
                resultsDiv.innerHTML = '<div style="padding: 20px; text-align: center; color: #666;">Skriv minst 2 tegn for å søke...</div>';
                return;
            }}
            
            // Simulerte søkeresultater
            const mockResults = [
                {{ title: 'Reguleringsplan Grünerløkka Nord', type: 'reguleringsplan', bydel: 'Grünerløkka' }},
                {{ title: 'Oslo Origo Byggetillatelser', type: 'origo', bydel: 'Alle' }},
                {{ title: 'Planbestemmelser Sentrum', type: 'pdf', bydel: 'Sentrum' }},
                {{ title: 'Områderegulering Frogner Park', type: 'reguleringsplan', bydel: 'Frogner' }}
            ];
            
            const filteredResults = mockResults.filter(result => 
                result.title.toLowerCase().includes(query.toLowerCase()) ||
                result.bydel.toLowerCase().includes(query.toLowerCase())
            );
            
            if (filteredResults.length === 0) {{
                resultsDiv.innerHTML = '<div style="padding: 20px; text-align: center; color: #666;">Ingen resultater funnet for "' + query + '"</div>';
                return;
            }}
            
            let html = '<h3>Søkeresultater (' + filteredResults.length + '):</h3>';
            filteredResults.forEach(result => {{
                html += `
                    <div style="padding: 15px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; background: white;">
                        <h4 style="color: #1e3c72;">${{result.title}}</h4>
                        <p><strong>Type:</strong> ${{result.type}} | <strong>Bydel:</strong> ${{result.bydel}}</p>
                    </div>
                `;
            }});
            
            resultsDiv.innerHTML = html;
        }}
        
        // Filter funksjonalitet
        function filterByType(type) {{
            // Oppdater active state
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Simuler filtrering
            const resultsDiv = document.getElementById('search-results');
            resultsDiv.innerHTML = `<div style="padding: 20px; color: #666;">Filtrert på: ${{type}}</div>`;
        }}
        
        // Export funksjonalitet
        function exportData(format) {{
            alert('🚀 Eksporterer Oslo data i ' + format.toUpperCase() + ' format...\\n\\nI en ekte implementering ville dette laste ned:\\n- Alle Oslo plandata\\n- Formatert som ' + format + '\\n- Med metadata og tidsstempel');
        }}
        
        // Simuler nye varsler
        function addDemoNotification() {{
            const notificationsList = document.getElementById('notifications-list');
            const newNotification = document.createElement('div');
            newNotification.className = 'notification new';
            newNotification.innerHTML = `
                <div class="notification-time">${{new Date().toLocaleString('no-NO')}}</div>
                <strong>Demo Varsel - Ny Aktivitet</strong><br>
                Simulert varsel: Ny plandata tilgjengelig i Oslo system.
            `;
            
            notificationsList.insertBefore(newNotification, notificationsList.firstChild);
        }}
        
        // Real-time data simulering
        function updateRealTimeStats() {{
            const stats = ['total-plans', 'active-areas', 'pending-plans', 'completion-rate'];
            
            stats.forEach(statId => {{
                const element = document.getElementById(statId);
                if (element) {{
                    const currentValue = parseInt(element.textContent);
                    const change = Math.floor(Math.random() * 3) - 1; // -1, 0, eller 1
                    const newValue = Math.max(0, currentValue + change);
                    
                    if (newValue !== currentValue) {{
                        element.style.transform = 'scale(1.1)';
                        element.style.color = '#4CAF50';
                        
                        setTimeout(() => {{
                            element.textContent = newValue;
                            element.style.transform = 'scale(1)';
                            element.style.color = '#1e3c72';
                        }}, 200);
                    }}
                }}
            }});
        }}
        
        // Modal lukking ved klikk utenfor
        window.onclick = function(event) {{
            const modal = document.getElementById('detail-modal');
            if (event.target === modal) {{
                modal.style.display = 'none';
            }}
        }}
        
        // Start real-time oppdateringer
        setInterval(updateRealTimeStats, 10000); // Hver 10 sekund
        
        // Auto-refresh hele siden
        setTimeout(() => {{
            location.reload();
        }}, 300000); // Hver 5 minutter
    </script>
</body>
</html>
"""
        return html_content
    
    def generate_interactive_bydel_cards(self) -> str:
        """Generer interaktive bydel kort"""
        html = ""
        
        for area, data in self.oslo_areas_with_data.items():
            status_class = data['status']
            
            html += f"""
            <div class="bydel-card {status_class}" onclick="showBydelDetails('{area}', {json.dumps(data)})">
                <div class="status-indicator status-{status_class}"></div>
                <div class="bydel-name">{area}</div>
                <div class="bydel-stats">
                    <div class="plan-count">{data['plans']}</div>
                    <div>planer tilgjengelig</div>
                    <div style="font-size: 0.8em; margin-top: 5px;">
                        Oppdatert: {data['last_update']}
                    </div>
                </div>
            </div>
            """
        
        return html
    
    def generate_chart_bars(self) -> str:
        """Generer chart bars for plandata"""
        html = ""
        
        # Simulerte data for de mest aktive bydelene
        top_areas = ['Sentrum', 'Frogner', 'Grünerløkka', 'Sagene', 'Østensjø']
        
        for i, area in enumerate(top_areas):
            height = random.randint(30, 90)
            html += f'<div class="chart-bar" style="height: {height}%" title="{area}: {self.oslo_areas_with_data[area]["plans"]} planer"></div>'
        
        return html
    
    def generate_trend_bars(self) -> str:
        """Generer trend bars for siste uke"""
        html = ""
        
        # Simulerte data for siste 7 dager
        for i in range(7):
            height = random.randint(20, 80)
            html += f'<div class="chart-bar" style="height: {height}%" title="Dag {i+1}: {random.randint(2, 8)} nye planer"></div>'
        
        return html
    
    def save_advanced_dashboard(self, filename: str = None) -> str:
        """Lagre avansert dashboard"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'oslo_advanced_dashboard_{timestamp}.html'
        
        html_content = self.generate_advanced_dashboard_html()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Advanced Oslo dashboard saved as: {filename}")
        return filename
    
    def open_advanced_dashboard(self, filename: str = None):
        """Åpne avansert dashboard i nettleser"""
        if not filename:
            filename = self.save_advanced_dashboard()
        
        file_path = os.path.abspath(filename)
        webbrowser.open(f'file://{file_path}')
        print(f"Opening advanced Oslo dashboard: {filename}")

def main():
    print("🚀 OSLO DASHBOARD ADVANCED FEATURES DEMO")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Opprett avansert Oslo dashboard
    advanced_dashboard = OsloDashboardAdvanced()
    
    # Generer og åpne avansert dashboard
    dashboard_file = advanced_dashboard.save_advanced_dashboard()
    advanced_dashboard.open_advanced_dashboard(dashboard_file)
    
    print(f"\n✨ SPESIFIKKE FEATURES DEMONSTRERT:")
    features = [
        "🔄 Real-time data oppdateringer (hver 10 sek)",
        "🗺️ Interaktivt bydelskart med klikk-detaljer",
        "📊 Animerte charts og grafer",
        "🔍 Live søk og filtrering",
        "🔔 Push notifications system",
        "📤 Export til JSON/CSV/PDF/GeoJSON",
        "📱 Tab-basert navigasjon",
        "🎨 Responsive design med animasjoner",
        "📈 Analytics med trenddata",
        "🎯 Modal vinduer for detaljer"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print(f"\n📄 File: {dashboard_file}")
    print(f"🌐 Opening in browser with advanced features...")
    print(f"💡 Prøv å klikke på bydeler, bruk søk, og test export!")

if __name__ == "__main__":
    main()