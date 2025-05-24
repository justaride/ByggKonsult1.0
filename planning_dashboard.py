#!/usr/bin/env python3
"""
Planning Data Dashboard
Web-basert dashboard for visualisering av integrerte plandata
"""

import json
import os
from datetime import datetime
from pathlib import Path
import webbrowser
from typing import Dict, List

class PlanningDashboard:
    def __init__(self, data_file: str = None):
        self.data_file = data_file or self.find_latest_data_file()
        self.data = self.load_data()
        
    def find_latest_data_file(self) -> str:
        """Find the latest integrated data file"""
        data_files = list(Path('.').glob('integrated_planning_data_*.json'))
        if data_files:
            latest = max(data_files, key=os.path.getctime)
            print(f"Using data file: {latest}")
            return str(latest)
        return None
    
    def load_data(self) -> Dict:
        """Load integrated planning data"""
        if not self.data_file or not os.path.exists(self.data_file):
            print("No data file found. Run integrated_planning_system.py first.")
            return {'data': {'regulatory_plans': [], 'pdf_analyses': []}}
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_html_dashboard(self) -> str:
        """Generate HTML dashboard"""
        
        # Analyze data for dashboard
        stats = self.analyze_data()
        
        html_content = f"""
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Integrert Plandata Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 30px;
        }}
        
        .card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border-left: 4px solid #667eea;
        }}
        
        .card h3 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .progress-bar {{
            background: #f0f0f0;
            border-radius: 10px;
            height: 20px;
            margin: 10px 0;
            overflow: hidden;
        }}
        
        .progress-fill {{
            background: linear-gradient(90deg, #667eea, #764ba2);
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }}
        
        .municipality-list {{
            max-height: 200px;
            overflow-y: auto;
        }}
        
        .municipality-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .source-badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin: 2px;
        }}
        
        .log-item {{
            background: #f8f9fa;
            border-radius: 5px;
            padding: 10px;
            margin: 5px 0;
            font-size: 0.9em;
        }}
        
        .log-timestamp {{
            color: #666;
            font-size: 0.8em;
        }}
        
        .recommendations {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
        }}
        
        .recommendations li {{
            margin: 5px 0;
            color: #856404;
        }}
        
        .refresh-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            margin: 20px;
            transition: transform 0.2s;
        }}
        
        .refresh-btn:hover {{
            transform: translateY(-2px);
        }}
        
        .full-width {{
            grid-column: 1 / -1;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        
        .data-table th,
        .data-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        .data-table th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }}
        
        .data-table tr:hover {{
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏗️ Integrert Plandata Dashboard</h1>
            <p>Oversikt over reguleringsplaner fra Geonorge, Oslo Origo og PDF-analyse</p>
            <p style="font-size: 0.9em; opacity: 0.7;">Sist oppdatert: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
        </div>
        
        <div class="dashboard-grid">
            <!-- Statistics Cards -->
            <div class="card">
                <h3>📊 Totalt antall planer</h3>
                <div class="stat-number">{stats['total_plans']}</div>
                <div class="stat-label">Reguleringsplaner</div>
            </div>
            
            <div class="card">
                <h3>🏘️ Kommuner dekket</h3>
                <div class="stat-number">{stats['municipalities_count']}</div>
                <div class="stat-label">Kommuner</div>
            </div>
            
            <div class="card">
                <h3>🔗 Kryss-referanser</h3>
                <div class="stat-number">{stats['cross_references']}</div>
                <div class="stat-label">Sammenkoblede planer</div>
            </div>
            
            <!-- Data Sources -->
            <div class="card">
                <h3>📡 Datakilder</h3>
                {self.generate_source_breakdown(stats)}
            </div>
            
            <!-- Quality Metrics -->
            <div class="card">
                <h3>📈 Kvalitetsmetrikker</h3>
                {self.generate_quality_metrics(stats)}
            </div>
            
            <!-- Municipalities -->
            <div class="card">
                <h3>🗺️ Kommuner</h3>
                <div class="municipality-list">
                    {self.generate_municipality_list(stats)}
                </div>
            </div>
            
            <!-- Latest Plans -->
            <div class="card full-width">
                <h3>📋 Siste planer</h3>
                {self.generate_latest_plans_table()}
            </div>
            
            <!-- Processing Log -->
            <div class="card">
                <h3>📝 Prosesseringslogg</h3>
                {self.generate_processing_log()}
            </div>
            
            <!-- Recommendations -->
            <div class="card">
                <h3>💡 Anbefalinger</h3>
                <div class="recommendations">
                    <ul>
                        {self.generate_recommendations()}
                    </ul>
                </div>
            </div>
        </div>
        
        <center>
            <button class="refresh-btn" onclick="location.reload()">
                🔄 Oppdater Dashboard
            </button>
        </center>
    </div>
    
    <script>
        // Auto-refresh every 5 minutes
        setTimeout(() => location.reload(), 300000);
        
        // Progress bar animations
        document.addEventListener('DOMContentLoaded', function() {{
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {{
                    bar.style.width = width;
                }}, 500);
            }});
        }});
    </script>
</body>
</html>
"""
        return html_content
    
    def analyze_data(self) -> Dict:
        """Analyze loaded data for dashboard statistics"""
        plans = self.data.get('data', {}).get('regulatory_plans', [])
        pdf_analyses = self.data.get('data', {}).get('pdf_analyses', [])
        
        # Basic statistics
        total_plans = len(plans)
        
        # Municipality analysis
        municipalities = set()
        for plan in plans:
            municipality = plan.get('municipality', 'Unknown')
            if municipality and municipality != 'Unknown':
                municipalities.add(municipality)
        
        # Source breakdown
        source_counts = {}
        for plan in plans:
            source = plan.get('source', 'unknown')
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Quality metrics
        plans_with_coordinates = len([p for p in plans if p.get('bbox') or p.get('coordinates')])
        plans_with_descriptions = len([p for p in plans if p.get('description')])
        
        return {
            'total_plans': total_plans,
            'municipalities_count': len(municipalities),
            'municipalities': list(municipalities),
            'cross_references': 0,  # Will be calculated in integration
            'source_counts': source_counts,
            'plans_with_coordinates': plans_with_coordinates,
            'plans_with_descriptions': plans_with_descriptions,
            'pdf_analyses_count': len(pdf_analyses)
        }
    
    def generate_source_breakdown(self, stats: Dict) -> str:
        """Generate HTML for source breakdown"""
        html = ""
        total = stats['total_plans']
        
        for source, count in stats['source_counts'].items():
            percentage = (count / total * 100) if total > 0 else 0
            
            html += f"""
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span class="source-badge">{source}</span>
                    <span>{count} planer</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {percentage}%;"></div>
                </div>
            </div>
            """
        
        return html
    
    def generate_quality_metrics(self, stats: Dict) -> str:
        """Generate HTML for quality metrics"""
        total = stats['total_plans']
        
        metrics = [
            ('Med koordinater', stats['plans_with_coordinates']),
            ('Med beskrivelser', stats['plans_with_descriptions']),
            ('PDF-analyser', stats['pdf_analyses_count'])
        ]
        
        html = ""
        for label, count in metrics:
            percentage = (count / total * 100) if total > 0 else 0
            
            html += f"""
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>{label}</span>
                    <span>{count}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {percentage}%;"></div>
                </div>
            </div>
            """
        
        return html
    
    def generate_municipality_list(self, stats: Dict) -> str:
        """Generate HTML for municipality list"""
        html = ""
        
        for municipality in sorted(stats['municipalities']):
            # Count plans per municipality
            plans_count = len([
                p for p in self.data.get('data', {}).get('regulatory_plans', [])
                if p.get('municipality') == municipality
            ])
            
            html += f"""
            <div class="municipality-item">
                <span>{municipality}</span>
                <span style="color: #667eea; font-weight: bold;">{plans_count}</span>
            </div>
            """
        
        return html
    
    def generate_latest_plans_table(self) -> str:
        """Generate HTML table for latest plans"""
        plans = self.data.get('data', {}).get('regulatory_plans', [])
        
        # Sort by last updated (if available) or take first 10
        latest_plans = plans[:10]
        
        html = """
        <table class="data-table">
            <thead>
                <tr>
                    <th>Plan</th>
                    <th>Kommune</th>
                    <th>Kilde</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for plan in latest_plans:
            title = plan.get('title', 'Ukjent plan')[:50]
            if len(plan.get('title', '')) > 50:
                title += '...'
            
            municipality = plan.get('municipality', 'Ukjent')
            source = plan.get('source', 'ukjent')
            plan_id = plan.get('plan_id', 'N/A')
            
            html += f"""
            <tr>
                <td><strong>{title}</strong><br><small>ID: {plan_id}</small></td>
                <td>{municipality}</td>
                <td><span class="source-badge">{source}</span></td>
                <td>Aktiv</td>
            </tr>
            """
        
        html += """
            </tbody>
        </table>
        """
        
        return html
    
    def generate_processing_log(self) -> str:
        """Generate HTML for processing log"""
        log_entries = self.data.get('data', {}).get('processing_log', [])
        
        html = ""
        for entry in log_entries[-5:]:  # Last 5 entries
            timestamp = entry.get('timestamp', '')
            operation = entry.get('operation', 'Unknown')
            summary = entry.get('details', {}).get('summary', 'No details')
            
            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%H:%M:%S')
            except:
                formatted_time = timestamp[:8] if timestamp else 'Unknown'
            
            html += f"""
            <div class="log-item">
                <div class="log-timestamp">{formatted_time}</div>
                <div><strong>{operation}</strong></div>
                <div style="font-size: 0.8em; color: #666;">{summary}</div>
            </div>
            """
        
        return html
    
    def generate_recommendations(self) -> str:
        """Generate HTML for recommendations"""
        stats = self.analyze_data()
        recommendations = []
        
        if stats['total_plans'] == 0:
            recommendations.append("Ingen plandata funnet - sjekk datakilder")
        
        if stats['plans_with_coordinates'] / stats['total_plans'] < 0.5 if stats['total_plans'] > 0 else False:
            recommendations.append("Lav andel planer med koordinater - vurder å forbedre geografisk datainnsamling")
        
        if 'oslo_origo' not in stats['source_counts']:
            recommendations.append("Mangler Oslo Origo data - kontakt dataplattform@oslo.kommune.no")
        
        if stats['municipalities_count'] < 5:
            recommendations.append("Vurder å utvide til flere kommuner")
        
        recommendations.append("Implementer automatisk overvåking av nye planpublikasjoner")
        
        html = ""
        for rec in recommendations:
            html += f"<li>{rec}</li>"
        
        return html
    
    def save_dashboard(self, filename: str = None) -> str:
        """Save dashboard as HTML file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'planning_dashboard_{timestamp}.html'
        
        html_content = self.generate_html_dashboard()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Dashboard saved as: {filename}")
        return filename
    
    def open_dashboard(self, filename: str = None):
        """Open dashboard in web browser"""
        if not filename:
            filename = self.save_dashboard()
        
        file_path = os.path.abspath(filename)
        webbrowser.open(f'file://{file_path}')
        print(f"Opening dashboard in browser: {filename}")

def main():
    print("🌐 PLANNING DATA DASHBOARD GENERATOR")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create dashboard
    dashboard = PlanningDashboard()
    
    # Generate and save dashboard
    dashboard_file = dashboard.save_dashboard()
    
    # Open in browser
    dashboard.open_dashboard(dashboard_file)
    
    print(f"✅ Dashboard generated successfully!")
    print(f"📄 File: {dashboard_file}")
    print(f"🌐 Opening in your default web browser...")

if __name__ == "__main__":
    main()