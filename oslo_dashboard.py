#!/usr/bin/env python3
"""
Oslo Planning Dashboard
Dedikert dashboard kun for Oslo kommune data og planlegging
"""

import json
import os
from datetime import datetime
from pathlib import Path
import webbrowser

class OsloPlanningDashboard:
    def __init__(self, oslo_data_file: str = None):
        self.oslo_data_file = oslo_data_file or self.find_latest_oslo_data()
        self.oslo_data = self.load_oslo_data()
        
        # Oslo-spesifikke områder og bydeler
        self.oslo_areas = [
            'Sentrum', 'Grünerløkka', 'Frogner', 'Gamle Oslo',
            'St. Hanshaugen', 'Sagene', 'Ullern', 'Vestre Aker',
            'Nordre Aker', 'Bjerke', 'Grorud', 'Stovner',
            'Alna', 'Østensjø', 'Nordstrand', 'Søndre Nordstrand'
        ]
        
    def find_latest_oslo_data(self) -> str:
        """Finn siste Oslo data fil"""
        oslo_files = list(Path('.').glob('oslo_planning_data_*.json'))
        if oslo_files:
            latest = max(oslo_files, key=os.path.getctime)
            print(f"Using Oslo data file: {latest}")
            return str(latest)
        return None
    
    def load_oslo_data(self) -> dict:
        """Last inn Oslo plandata"""
        if not self.oslo_data_file or not os.path.exists(self.oslo_data_file):
            print("No Oslo data file found. Run oslo_planning_system.py first.")
            return {'oslo_data': {'origo_datasets': [], 'reguleringsplaner': [], 'pdf_documents': []}}
        
        with open(self.oslo_data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_oslo_data(self) -> dict:
        """Analyser Oslo-data for dashboard"""
        oslo_data = self.oslo_data.get('oslo_data', {})
        
        origo_datasets = oslo_data.get('origo_datasets', [])
        reguleringsplaner = oslo_data.get('reguleringsplaner', [])
        pdf_documents = oslo_data.get('pdf_documents', [])
        
        # Analyser Oslo-spesifikke metrics
        stats = {
            'total_oslo_data': len(origo_datasets) + len(reguleringsplaner) + len(pdf_documents),
            'origo_datasets': len(origo_datasets),
            'reguleringsplaner': len(reguleringsplaner),
            'pdf_documents': len(pdf_documents),
            'data_sources': {
                'oslo_origo': len(origo_datasets),
                'geonorge_oslo': len(reguleringsplaner),
                'oslo_pdfs': len(pdf_documents)
            }
        }
        
        # Analyser bydelsdekning
        covered_areas = set()
        for plan in reguleringsplaner:
            title = plan.get('title', '').lower()
            for area in self.oslo_areas:
                if area.lower() in title:
                    covered_areas.add(area)
        
        stats['bydels_dekning'] = {
            'covered': len(covered_areas),
            'total': len(self.oslo_areas),
            'percentage': (len(covered_areas) / len(self.oslo_areas)) * 100,
            'covered_areas': list(covered_areas),
            'missing_areas': [area for area in self.oslo_areas if area not in covered_areas]
        }
        
        return stats
    
    def generate_oslo_dashboard_html(self) -> str:
        """Generer Oslo-spesifikk HTML dashboard"""
        
        stats = self.analyze_oslo_data()
        
        html_content = f"""
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oslo Planning Dashboard</title>
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
            font-size: 3em;
            margin-bottom: 10px;
        }}
        
        .oslo-title {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .oslo-subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .dashboard-container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .oslo-stats-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            padding: 30px;
        }}
        
        .oslo-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            border-left: 5px solid #1e3c72;
            transition: transform 0.3s ease;
        }}
        
        .oslo-card:hover {{
            transform: translateY(-5px);
        }}
        
        .oslo-card h3 {{
            color: #1e3c72;
            margin-bottom: 15px;
            font-size: 1.4em;
            display: flex;
            align-items: center;
        }}
        
        .oslo-icon {{
            font-size: 1.5em;
            margin-right: 10px;
        }}
        
        .oslo-stat-number {{
            font-size: 3em;
            font-weight: bold;
            color: #2a5298;
            margin-bottom: 10px;
        }}
        
        .oslo-stat-label {{
            color: #666;
            font-size: 1.1em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .oslo-progress-bar {{
            background: #f0f0f0;
            border-radius: 15px;
            height: 25px;
            margin: 15px 0;
            overflow: hidden;
            position: relative;
        }}
        
        .oslo-progress-fill {{
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            height: 100%;
            border-radius: 15px;
            transition: width 1s ease;
            position: relative;
        }}
        
        .oslo-progress-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-weight: bold;
            font-size: 0.9em;
        }}
        
        .bydel-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }}
        
        .bydel-item {{
            padding: 8px 12px;
            border-radius: 20px;
            text-align: center;
            font-size: 0.9em;
            font-weight: 500;
        }}
        
        .bydel-covered {{
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
        }}
        
        .bydel-missing {{
            background: #f5f5f5;
            color: #666;
            border: 2px dashed #ddd;
        }}
        
        .oslo-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        .oslo-table th,
        .oslo-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        
        .oslo-table th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #1e3c72;
        }}
        
        .oslo-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .source-tag {{
            display: inline-block;
            background: #1e3c72;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin: 2px;
        }}
        
        .oslo-footer {{
            background: #1e3c72;
            color: white;
            text-align: center;
            padding: 20px;
        }}
        
        .oslo-contact {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }}
        
        .oslo-contact strong {{
            color: #856404;
        }}
        
        .full-width {{
            grid-column: 1 / -1;
        }}
        
        .refresh-btn {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1.1em;
            margin: 20px;
            transition: transform 0.2s;
            box-shadow: 0 4px 15px rgba(30, 60, 114, 0.3);
        }}
        
        .refresh-btn:hover {{
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="oslo-header">
        <div class="oslo-logo">🏛️</div>
        <div class="oslo-title">Oslo Planning Dashboard</div>
        <div class="oslo-subtitle">Plandata og regulering for Oslo kommune</div>
        <div style="font-size: 0.9em; opacity: 0.7; margin-top: 10px;">
            Sist oppdatert: {datetime.now().strftime('%d.%m.%Y %H:%M')}
        </div>
    </div>
    
    <div class="dashboard-container">
        <div class="oslo-stats-header">
            <h2>📊 Oslo Plandata Oversikt</h2>
            <p>Komplett oversikt over tilgjengelige plandata for Oslo kommune</p>
        </div>
        
        <div class="dashboard-grid">
            <!-- Hovedstatistikk -->
            <div class="oslo-card">
                <h3><span class="oslo-icon">📋</span>Totalt plandata</h3>
                <div class="oslo-stat-number">{stats['total_oslo_data']}</div>
                <div class="oslo-stat-label">Oslo datasett</div>
            </div>
            
            <div class="oslo-card">
                <h3><span class="oslo-icon">🏢</span>Origo datasett</h3>
                <div class="oslo-stat-number">{stats['origo_datasets']}</div>
                <div class="oslo-stat-label">Fra Oslo Origo</div>
            </div>
            
            <div class="oslo-card">
                <h3><span class="oslo-icon">📄</span>Reguleringsplaner</h3>
                <div class="oslo-stat-number">{stats['reguleringsplaner']}</div>
                <div class="oslo-stat-label">Fra Geonorge</div>
            </div>
            
            <!-- Bydelsdekning -->
            <div class="oslo-card full-width">
                <h3><span class="oslo-icon">🗺️</span>Bydelsdekning</h3>
                <div style="display: flex; align-items: center; margin-bottom: 20px;">
                    <div class="oslo-stat-number" style="font-size: 2em; margin-right: 20px;">
                        {stats['bydels_dekning']['covered']}/{stats['bydels_dekning']['total']}
                    </div>
                    <div>
                        <div class="oslo-stat-label">Bydeler dekket</div>
                        <div class="oslo-progress-bar" style="width: 200px;">
                            <div class="oslo-progress-fill" style="width: {stats['bydels_dekning']['percentage']}%;">
                                <div class="oslo-progress-text">{stats['bydels_dekning']['percentage']:.1f}%</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <h4 style="margin-bottom: 15px; color: #1e3c72;">Oslo Bydeler:</h4>
                <div class="bydel-grid">
                    {self.generate_bydel_grid(stats['bydels_dekning'])}
                </div>
            </div>
            
            <!-- Datakilder -->
            <div class="oslo-card">
                <h3><span class="oslo-icon">📡</span>Datakilder</h3>
                {self.generate_source_breakdown(stats['data_sources'])}
            </div>
            
            <!-- Oslo kontakt info -->
            <div class="oslo-card">
                <h3><span class="oslo-icon">📞</span>Oslo Kontakter</h3>
                <div class="oslo-contact">
                    <strong>Origo Dataplatform:</strong><br>
                    📧 dataplattform@oslo.kommune.no<br>
                    <small>For API-tilgang og datasett</small>
                </div>
                <div class="oslo-contact">
                    <strong>Plan- og bygningsetaten (PBE):</strong><br>
                    📧 postmottak.pbe@oslo.kommune.no<br>
                    ☎️ 02180<br>
                    <small>For byggesaker og reguleringsplaner</small>
                </div>
            </div>
            
            <!-- Siste Oslo planer -->
            <div class="oslo-card full-width">
                <h3><span class="oslo-icon">📋</span>Siste Oslo Planer</h3>
                {self.generate_oslo_plans_table()}
            </div>
        </div>
        
        <div class="oslo-footer">
            <p><strong>Oslo Planning Dashboard</strong> - Dedikert for Oslo kommune</p>
            <p>Integrerer Origo, PBE-systemer og Geonorge data</p>
            <button class="refresh-btn" onclick="location.reload()">
                🔄 Oppdater Oslo Data
            </button>
        </div>
    </div>
    
    <script>
        // Animasjoner for Oslo dashboard
        document.addEventListener('DOMContentLoaded', function() {{
            // Animer progress bars
            const progressBars = document.querySelectorAll('.oslo-progress-fill');
            progressBars.forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {{
                    bar.style.width = width;
                }}, 500);
            }});
            
            // Animer statistikk-tall
            const statNumbers = document.querySelectorAll('.oslo-stat-number');
            statNumbers.forEach(num => {{
                const finalValue = parseInt(num.textContent);
                if (!isNaN(finalValue)) {{
                    let currentValue = 0;
                    const increment = finalValue / 30;
                    const timer = setInterval(() => {{
                        currentValue += increment;
                        if (currentValue >= finalValue) {{
                            currentValue = finalValue;
                            clearInterval(timer);
                        }}
                        num.textContent = Math.floor(currentValue);
                    }}, 50);
                }}
            }});
        }});
        
        // Auto-refresh hver 10 minutter
        setTimeout(() => location.reload(), 600000);
    </script>
</body>
</html>
"""
        return html_content
    
    def generate_bydel_grid(self, bydels_data: dict) -> str:
        """Generer HTML for bydels-grid"""
        html = ""
        covered = set(bydels_data['covered_areas'])
        
        for area in self.oslo_areas:
            if area in covered:
                html += f'<div class="bydel-item bydel-covered">✓ {area}</div>'
            else:
                html += f'<div class="bydel-item bydel-missing">{area}</div>'
        
        return html
    
    def generate_source_breakdown(self, sources: dict) -> str:
        """Generer HTML for kilde-breakdown"""
        html = ""
        total = sum(sources.values())
        
        source_names = {
            'oslo_origo': 'Oslo Origo',
            'geonorge_oslo': 'Geonorge Oslo',
            'oslo_pdfs': 'Oslo PDFs'
        }
        
        for source, count in sources.items():
            percentage = (count / total * 100) if total > 0 else 0
            name = source_names.get(source, source)
            
            html += f"""
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span class="source-tag">{name}</span>
                    <span><strong>{count}</strong></span>
                </div>
                <div class="oslo-progress-bar">
                    <div class="oslo-progress-fill" style="width: {percentage}%;"></div>
                </div>
            </div>
            """
        
        return html
    
    def generate_oslo_plans_table(self) -> str:
        """Generer tabell for Oslo planer"""
        oslo_data = self.oslo_data.get('oslo_data', {})
        plans = oslo_data.get('reguleringsplaner', [])[:10]  # Første 10
        
        html = """
        <table class="oslo-table">
            <thead>
                <tr>
                    <th>Plan</th>
                    <th>Område</th>
                    <th>Organisasjon</th>
                    <th>Kilde</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for plan in plans:
            title = plan.get('title', 'Ukjent plan')[:60]
            if len(plan.get('title', '')) > 60:
                title += '...'
            
            # Prøv å identifisere Oslo-område
            oslo_area = 'Oslo'
            plan_title_lower = plan.get('title', '').lower()
            for area in self.oslo_areas:
                if area.lower() in plan_title_lower:
                    oslo_area = area
                    break
            
            organization = plan.get('organization', 'Ukjent')
            source = plan.get('source', 'unknown')
            
            html += f"""
            <tr>
                <td><strong>{title}</strong></td>
                <td>{oslo_area}</td>
                <td>{organization}</td>
                <td><span class="source-tag">{source}</span></td>
            </tr>
            """
        
        html += """
            </tbody>
        </table>
        """
        
        return html
    
    def save_oslo_dashboard(self, filename: str = None) -> str:
        """Lagre Oslo dashboard som HTML"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'oslo_planning_dashboard_{timestamp}.html'
        
        html_content = self.generate_oslo_dashboard_html()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Oslo dashboard saved as: {filename}")
        return filename
    
    def open_oslo_dashboard(self, filename: str = None):
        """Åpne Oslo dashboard i nettleser"""
        if not filename:
            filename = self.save_oslo_dashboard()
        
        file_path = os.path.abspath(filename)
        webbrowser.open(f'file://{file_path}')
        print(f"Opening Oslo dashboard in browser: {filename}")

def main():
    print("🏛️ OSLO PLANNING DASHBOARD GENERATOR")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Opprett Oslo dashboard
    oslo_dashboard = OsloPlanningDashboard()
    
    # Generer og lagre Oslo dashboard
    dashboard_file = oslo_dashboard.save_oslo_dashboard()
    
    # Åpne i nettleser
    oslo_dashboard.open_oslo_dashboard(dashboard_file)
    
    print(f"✅ Oslo dashboard generated successfully!")
    print(f"📄 File: {dashboard_file}")
    print(f"🏛️ Focused exclusively on Oslo kommune data")
    print(f"🌐 Opening in your default web browser...")

if __name__ == "__main__":
    main()