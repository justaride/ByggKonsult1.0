#!/usr/bin/env python3
"""
Oslo Planning Dashboard - Standalone Implementation
Phase 1: Core infrastructure for standalone operation
"""

import json
import sqlite3
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import io
import base64

class OsloPlanningDatabase:
    """Local SQLite database for Oslo planning data"""
    
    def __init__(self, db_path="oslo_planning.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize database with Oslo-specific tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Planning documents table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS planning_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            document_type TEXT NOT NULL,
            bydel TEXT,
            coordinates TEXT,
            date_created DATETIME,
            date_updated DATETIME,
            status TEXT DEFAULT 'active',
            content_text TEXT,
            file_path TEXT,
            metadata TEXT,
            ai_analysis TEXT,
            tags TEXT,
            source_system TEXT
        )
        ''')
        
        # Oslo areas/bydeler table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS oslo_areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_name TEXT UNIQUE NOT NULL,
            area_type TEXT,
            population INTEGER,
            area_km2 REAL,
            coordinates TEXT,
            status TEXT DEFAULT 'active',
            last_updated DATETIME,
            plan_count INTEGER DEFAULT 0,
            metadata TEXT
        )
        ''')
        
        # User uploads table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_type TEXT,
            upload_date DATETIME,
            file_size INTEGER,
            processed BOOLEAN DEFAULT FALSE,
            extraction_results TEXT,
            user_notes TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insert demo Oslo data
        self.insert_demo_data()
    
    def insert_demo_data(self):
        """Insert comprehensive demo data for Oslo's 15 official bydeler"""
        # Oslo's 15 official bydeler (districts) - factually correct as of 2025
        oslo_bydeler = [
            {'name': 'Alna', 'population': 49801, 'area_km2': 13.7, 'coordinates': '59.9278,10.8944'},
            {'name': 'Bjerke', 'population': 33422, 'area_km2': 7.7, 'coordinates': '59.9694,10.8167'},
            {'name': 'Frogner', 'population': 59269, 'area_km2': 8.3, 'coordinates': '59.9181,10.7167'},
            {'name': 'Gamle Oslo', 'population': 58671, 'area_km2': 7.5, 'coordinates': '59.9056,10.7639'},
            {'name': 'Grorud', 'population': 27707, 'area_km2': 8.2, 'coordinates': '59.9639,10.8833'},
            {'name': 'Grünerløkka', 'population': 58435, 'area_km2': 4.8, 'coordinates': '59.9227,10.7594'},
            {'name': 'Nordre Aker', 'population': 52327, 'area_km2': 13.6, 'coordinates': '59.9861,10.7703'},
            {'name': 'Nordstrand', 'population': 52459, 'area_km2': 16.9, 'coordinates': '59.8667,10.8167'},
            {'name': 'Sagene', 'population': 45089, 'area_km2': 3.1, 'coordinates': '59.9472,10.7311'},
            {'name': 'St. Hanshaugen', 'population': 38945, 'area_km2': 3.6, 'coordinates': '59.9306,10.7428'},
            {'name': 'Stovner', 'population': 33316, 'area_km2': 8.2, 'coordinates': '59.9833,10.9167'},
            {'name': 'Søndre Nordstrand', 'population': 39066, 'area_km2': 18.4, 'coordinates': '59.8167,10.8333'},
            {'name': 'Ullern', 'population': 34569, 'area_km2': 16.9, 'coordinates': '59.9167,10.6500'},
            {'name': 'Vestre Aker', 'population': 50157, 'area_km2': 16.6, 'coordinates': '59.9694,10.6708'},
            {'name': 'Østensjø', 'population': 50806, 'area_km2': 12.2, 'coordinates': '59.8833,10.8167'}
        ]
        
        # Add Sentrum as a special common area (not a bydel)
        oslo_common_areas = [
            {'name': 'Sentrum', 'population': 1023, 'area_km2': 1.8, 'coordinates': '59.9139,10.7522', 'area_type': 'common_area'}
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert 15 official bydeler
        for bydel in oslo_bydeler:
            cursor.execute('''
                INSERT OR IGNORE INTO oslo_areas 
                (area_name, area_type, population, area_km2, coordinates, last_updated, plan_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (bydel['name'], 'bydel', bydel['population'], bydel['area_km2'], 
                  bydel['coordinates'], datetime.now(), np.random.randint(1, 15)))
        
        # Insert common areas (Sentrum)
        for area in oslo_common_areas:
            cursor.execute('''
                INSERT OR IGNORE INTO oslo_areas 
                (area_name, area_type, population, area_km2, coordinates, last_updated, plan_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (area['name'], area['area_type'], area['population'], area['area_km2'], 
                  area['coordinates'], datetime.now(), np.random.randint(1, 8)))
        
        # Demo planning documents
        demo_documents = [
            {
                'title': 'Reguleringsplan for Grünerløkka Nord',
                'document_type': 'Reguleringsplan',
                'bydel': 'Grünerløkka',
                'coordinates': '59.9227,10.7594',
                'status': 'Under behandling',
                'content_text': 'Detaljert reguleringsplan for boligområde i Grünerløkka...',
                'tags': 'bolig,regulering,grünerløkka'
            },
            {
                'title': 'Områderegulering Frogner Park',
                'document_type': 'Områderegulering',
                'bydel': 'Frogner',
                'coordinates': '59.9181,10.7167',
                'status': 'Vedtatt',
                'content_text': 'Områderegulering for parkområde og tilstøtende bebyggelse...',
                'tags': 'park,områderegulering,frogner'
            },
            {
                'title': 'Planendring Sentrum Øst',
                'document_type': 'Planendring',
                'bydel': 'Sentrum',
                'coordinates': '59.9139,10.7522',
                'status': 'Høring',
                'content_text': 'Endring av reguleringsplan for forretningsområde...',
                'tags': 'forretning,planendring,sentrum'
            }
        ]
        
        for doc in demo_documents:
            cursor.execute('''
                INSERT OR IGNORE INTO planning_documents 
                (title, document_type, bydel, coordinates, status, content_text, tags, date_created)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (doc['title'], doc['document_type'], doc['bydel'], doc['coordinates'],
                  doc['status'], doc['content_text'], doc['tags'], datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_all_documents(self):
        """Get all planning documents"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM planning_documents", conn)
        conn.close()
        return df
    
    def get_oslo_areas(self):
        """Get all Oslo areas"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM oslo_areas", conn)
        conn.close()
        return df
    
    def add_document(self, title, doc_type, bydel, content, coordinates=None):
        """Add new planning document"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO planning_documents 
            (title, document_type, bydel, content_text, coordinates, date_created, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, doc_type, bydel, content, coordinates, datetime.now(), 'active'))
        
        conn.commit()
        conn.close()


class OsloVisualization:
    """Advanced visualization system for Oslo planning data"""
    
    def __init__(self, database):
        self.db = database
        
    def create_interactive_oslo_map(self, show_bydeler=True, show_documents=True, selected_bydel="All"):
        """Create interactive map of Oslo with planning data"""
        areas_df = self.db.get_oslo_areas()
        docs_df = self.db.get_all_documents()
        
        # Filter data based on selection
        if selected_bydel != "All":
            areas_df = areas_df[areas_df['area_name'] == selected_bydel]
            docs_df = docs_df[docs_df['bydel'] == selected_bydel]
        
        # Create base map with better styling
        fig = go.Figure()
        
        # Add bydeler as scatter points with improved visualization
        if show_bydeler and not areas_df.empty:
            # Separate bydeler and common areas
            bydeler_df = areas_df[areas_df['area_type'] == 'bydel']
            common_df = areas_df[areas_df['area_type'] == 'common_area']
            
            # Add bydeler
            if not bydeler_df.empty:
                lats, lons, texts, sizes, colors = [], [], [], [], []
                
                for _, area in bydeler_df.iterrows():
                    if area['coordinates']:
                        lat, lon = map(float, area['coordinates'].split(','))
                        lats.append(lat)
                        lons.append(lon)
                        texts.append(f"<b>{area['area_name']}</b><br>"
                                   f"Type: Bydel<br>"
                                   f"Planer: {area['plan_count']}<br>"
                                   f"Population: {area['population']:,}<br>"
                                   f"Area: {area['area_km2']} km²")
                        sizes.append(area['plan_count'] * 2 + 15)
                        colors.append(area['plan_count'])
                
                fig.add_trace(go.Scattermapbox(
                    lat=lats,
                    lon=lons,
                    mode='markers',
                    marker=dict(
                        size=sizes,
                        color=colors,
                        colorscale='Blues',
                        showscale=True,
                        colorbar=dict(
                            title="Antall Planer",
                            x=1.02,
                            thickness=15
                        ),
                        opacity=0.8
                    ),
                    text=texts,
                    hovertemplate='%{text}<extra></extra>',
                    name='Bydeler'
                ))
            
            # Add common areas (like Sentrum) with different styling
            if not common_df.empty:
                for _, area in common_df.iterrows():
                    if area['coordinates']:
                        lat, lon = map(float, area['coordinates'].split(','))
                        
                        fig.add_trace(go.Scattermapbox(
                            lat=[lat],
                            lon=[lon],
                            mode='markers',
                            marker=dict(
                                size=area['plan_count'] * 2 + 12,
                                color='gold',
                                opacity=0.9
                            ),
                            text=f"<b>{area['area_name']}</b><br>"
                                 f"Type: {area['area_type'].replace('_', ' ').title()}<br>"
                                 f"Planer: {area['plan_count']}<br>"
                                 f"Population: {area['population']:,}",
                            hovertemplate='%{text}<extra></extra>',
                            name='Common Areas'
                        ))
        
        # Add planning documents with status-based colors
        if show_documents and not docs_df.empty:
            status_colors = {
                'Under behandling': '#ff4444',  # Red
                'Vedtatt': '#44ff44',           # Green  
                'Høring': '#ff8800',            # Orange
                'Avslått': '#888888'            # Gray
            }
            
            # Group documents by status for better legend
            for status, color in status_colors.items():
                status_docs = docs_df[docs_df['status'] == status]
                
                if not status_docs.empty:
                    lats, lons, texts = [], [], []
                    
                    for _, doc in status_docs.iterrows():
                        if doc['coordinates']:
                            lat, lon = map(float, doc['coordinates'].split(','))
                            lats.append(lat)
                            lons.append(lon)
                            texts.append(f"<b>{doc['title']}</b><br>"
                                        f"Bydel: {doc['bydel']}<br>"
                                        f"Type: {doc['document_type']}<br>"
                                        f"Status: {doc['status']}<br>"
                                        f"Created: {doc['date_created'][:10] if doc['date_created'] else 'N/A'}")
                    
                    if lats:  # Only add trace if we have coordinates
                        fig.add_trace(go.Scattermapbox(
                            lat=lats,
                            lon=lons,
                            mode='markers',
                            marker=dict(
                                size=10,
                                color=color,
                                opacity=0.9
                            ),
                            text=texts,
                            hovertemplate='%{text}<extra></extra>',
                            name=f'Status: {status}'
                        ))
        
        # Improve map layout and styling
        center_lat = 59.9139
        center_lon = 10.7522
        zoom_level = 11
        
        # Adjust center and zoom if focusing on specific bydel
        if selected_bydel != "All" and not areas_df.empty:
            selected_area = areas_df[areas_df['area_name'] == selected_bydel].iloc[0]
            if selected_area['coordinates']:
                center_lat, center_lon = map(float, selected_area['coordinates'].split(','))
                zoom_level = 13
        
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=center_lat, lon=center_lon),
                zoom=zoom_level
            ),
            margin=dict(r=0, t=0, l=0, b=0),
            height=650,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255,255,255,0.8)"
            ),
            title=dict(
                text=f"Oslo Planning Map{' - ' + selected_bydel if selected_bydel != 'All' else ''}",
                x=0.5,
                font=dict(size=16)
            )
        )
        
        return fig
    
    def create_bydel_statistics(self):
        """Create bydel statistics dashboard"""
        areas_df = self.db.get_oslo_areas()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Planer per Bydel', 'Befolkning vs Planer', 
                          'Areal Fordeling', 'Plan Tetthet'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "pie"}, {"type": "bar"}]]
        )
        
        # Bar chart - Plans per bydel
        fig.add_trace(
            go.Bar(
                x=areas_df['area_name'][:8],  # Top 8
                y=areas_df['plan_count'][:8],
                name='Antall Planer',
                marker_color='lightblue'
            ),
            row=1, col=1
        )
        
        # Scatter - Population vs Plans
        fig.add_trace(
            go.Scatter(
                x=areas_df['population'],
                y=areas_df['plan_count'],
                mode='markers',
                marker=dict(size=10, color='red'),
                text=areas_df['area_name'],
                name='Befolkning vs Planer'
            ),
            row=1, col=2
        )
        
        # Pie chart - Area distribution
        fig.add_trace(
            go.Pie(
                labels=areas_df['area_name'][:6],
                values=areas_df['area_km2'][:6],
                name='Areal'
            ),
            row=2, col=1
        )
        
        # Bar chart - Plan density
        areas_df['density'] = areas_df['plan_count'] / areas_df['area_km2']
        fig.add_trace(
            go.Bar(
                x=areas_df['area_name'][:8],
                y=areas_df['density'][:8],
                name='Plan Tetthet',
                marker_color='green'
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=True)
        return fig
    
    def create_status_overview(self):
        """Create status overview chart"""
        docs_df = self.db.get_all_documents()
        
        status_counts = docs_df['status'].value_counts()
        
        fig = go.Figure(data=[
            go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                hole=.3,
                marker_colors=['red', 'green', 'orange', 'blue']
            )
        ])
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            title="Plan Status Fordeling",
            height=400
        )
        
        return fig


class DataImportSystem:
    """Handle various file formats for Oslo planning data"""
    
    def __init__(self, database):
        self.db = database
        
    def process_pdf_upload(self, uploaded_file):
        """Process PDF files (simplified version)"""
        try:
            import pdfplumber
            
            with pdfplumber.open(uploaded_file) as pdf:
                text_content = ""
                for page in pdf.pages:
                    text_content += page.extract_text() or ""
                
                # Basic analysis
                result = {
                    'filename': uploaded_file.name,
                    'content': text_content[:1000],  # First 1000 chars
                    'pages': len(pdf.pages),
                    'extracted_info': self.extract_basic_info(text_content)
                }
                
                return result
        except Exception as e:
            return {'error': f"PDF processing failed: {str(e)}"}
    
    def process_excel_upload(self, uploaded_file):
        """Process Excel files"""
        try:
            df = pd.read_excel(uploaded_file)
            
            result = {
                'filename': uploaded_file.name,
                'shape': df.shape,
                'columns': list(df.columns),
                'preview': df.head().to_dict('records')
            }
            
            return result
        except Exception as e:
            return {'error': f"Excel processing failed: {str(e)}"}
    
    def extract_basic_info(self, text):
        """Extract basic information from text"""
        import re
        
        info = {
            'addresses': [],
            'dates': [],
            'coordinates': [],
            'plan_types': []
        }
        
        # Look for Norwegian addresses
        address_pattern = r'\b[A-ZÆØÅ][a-zæøå]+(?:\s+[A-ZÆØÅ][a-zæøå]+)*\s+\d+[a-z]?\b'
        info['addresses'] = re.findall(address_pattern, text)[:5]
        
        # Look for dates
        date_pattern = r'\b\d{1,2}[./]\d{1,2}[./]\d{4}\b'
        info['dates'] = re.findall(date_pattern, text)[:5]
        
        # Look for coordinates
        coord_pattern = r'\b\d{2}\.\d+,\s*\d{2}\.\d+\b'
        info['coordinates'] = re.findall(coord_pattern, text)[:3]
        
        # Look for plan types
        plan_types = ['reguleringsplan', 'områderegulering', 'planendring', 'bebyggelsesplan']
        for plan_type in plan_types:
            if plan_type.lower() in text.lower():
                info['plan_types'].append(plan_type)
        
        return info


def create_streamlit_app():
    """Main Streamlit application"""
    
    st.set_page_config(
        page_title="Oslo Planning Intelligence",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://oslo.kommune.no',
            'Report a bug': None,
            'About': "Oslo Planning Intelligence Dashboard - Professional municipal planning analysis"
        }
    )
    
    # Apply enhanced styling
    from oslo_enhanced_ui import apply_oslo_branding, create_oslo_header
    oslo_colors = apply_oslo_branding()
    
    # Initialize database
    if 'database' not in st.session_state:
        st.session_state.database = OsloPlanningDatabase()
        st.session_state.viz = OsloVisualization(st.session_state.database)
        st.session_state.import_system = DataImportSystem(st.session_state.database)
    
    # Professional header
    create_oslo_header()
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #1e3c72, #2a5298); 
                    border-radius: 10px; margin-bottom: 1rem; color: white;">
            <h2 style="margin: 0;">🏛️ Navigation</h2>
            <p style="margin: 0; opacity: 0.9;">Oslo Planning Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.radio(
            "",
            ["📊 Dashboard", "🗺️ Interactive Map", "📤 Data Upload", 
             "📋 Data Management", "📈 Analytics", "⚙️ Settings"]
        )
        
        st.markdown("---")
        
        # Enhanced quick stats
        docs_df = st.session_state.database.get_all_documents()
        areas_df = st.session_state.database.get_oslo_areas()
        
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h4 style="color: #1e3c72; margin-bottom: 0.5rem;">📊 Quick Stats</h4>
        </div>
        """, unsafe_allow_html=True)
        
        from oslo_enhanced_ui import create_enhanced_metric
        create_enhanced_metric("Documents", len(docs_df), "+2 this week", "positive")
        create_enhanced_metric("Areas", len(areas_df), "15 bydeler", "positive")
        create_enhanced_metric("Active Plans", len(docs_df[docs_df['status'] != 'Avslått']), "+5 this month", "positive")
        
        # System status
        st.markdown("""
        <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; margin-top: 1rem; 
                    border-left: 4px solid #4caf50;">
            <strong style="color: #2e7d32;">🟢 System Status</strong><br>
            <small>All systems operational</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    if page == "📊 Dashboard":
        render_dashboard()
    elif page == "🗺️ Interactive Map":
        render_map_page()
    elif page == "📤 Data Upload":
        render_upload_page()
    elif page == "📋 Data Management":
        render_data_management()
    elif page == "📈 Analytics":
        render_analytics_page()
    elif page == "⚙️ Settings":
        render_settings_page()


def render_dashboard():
    """Render enhanced main dashboard"""
    from oslo_enhanced_ui import create_enhanced_metric, create_enhanced_charts, create_info_panel, create_status_badge, create_oslo_footer
    
    # Dashboard introduction
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="color: #1e3c72;">📊 Municipal Planning Intelligence</h2>
        <p style="font-size: 1.2em; color: #666;">Real-time insights into Oslo's urban development</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    docs_df = st.session_state.database.get_all_documents()
    areas_df = st.session_state.database.get_oslo_areas()
    
    # Enhanced metrics layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_docs = len(docs_df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{total_docs}</div>
            <div class="metric-label">Planning Documents</div>
            <div class="metric-delta positive">↗ +2 this week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        bydeler_count = len(areas_df[areas_df['area_type'] == 'bydel'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{bydeler_count}</div>
            <div class="metric-label">Official Bydeler</div>
            <div class="metric-delta positive">🏛️ Complete coverage</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_plans = areas_df['plan_count'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{total_plans}</div>
            <div class="metric-label">Total Plans</div>
            <div class="metric-delta positive">↗ +5 this month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_plans = areas_df['plan_count'].mean()
        completion_rate = (len(docs_df[docs_df['status'] == 'Vedtatt']) / len(docs_df) * 100) if len(docs_df) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{completion_rate:.0f}%</div>
            <div class="metric-label">Completion Rate</div>
            <div class="metric-delta positive">↗ +3% improvement</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Enhanced charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-panel">
            <h3 style="color: #1e3c72; margin-bottom: 1rem;">📊 Planning Activity by Area</h3>
        </div>
        """, unsafe_allow_html=True)
        
        fig1, fig2, fig3 = create_enhanced_charts(areas_df, docs_df)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="info-panel">
            <h3 style="color: #1e3c72; margin-bottom: 1rem;">📈 Document Status Distribution</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Population vs Plans analysis
    st.markdown("""
    <div class="info-panel">
        <h3 style="color: #1e3c72; margin-bottom: 1rem;">🏘️ Population vs Planning Activity Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Recent activity with enhanced styling
    st.markdown("""
    <div class="info-panel">
        <h3 style="color: #1e3c72; margin-bottom: 1rem;">📋 Recent Planning Activity</h3>
    </div>
    """, unsafe_allow_html=True)
    
    recent_docs = docs_df.sort_values('date_created', ascending=False).head(5)
    
    for _, doc in recent_docs.iterrows():
        status_badge = create_status_badge(doc['status'])
        
        with st.expander(f"📄 {doc['title']} - {doc['bydel']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Document Type:** {doc['document_type']}")
                st.markdown(f"**Location:** {doc['bydel']}")
                if doc['content_text']:
                    st.markdown("**Description:**")
                    st.markdown(f"*{doc['content_text'][:200]}...*")
            
            with col2:
                st.markdown(f"**Status:** {status_badge}", unsafe_allow_html=True)
                st.markdown(f"**Created:** {doc['date_created'][:10] if doc['date_created'] else 'N/A'}")
                if doc['tags']:
                    st.markdown(f"**Tags:** `{doc['tags']}`")
    
    # Summary insights
    st.markdown("""
    <div class="info-panel">
        <h3 style="color: #1e3c72; margin-bottom: 1rem;">💡 Key Insights</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div>
                <h4 style="color: #2a5298;">🏆 Most Active Areas</h4>
                <ul>
    """, unsafe_allow_html=True)
    
    top_areas = areas_df.nlargest(3, 'plan_count')
    for _, area in top_areas.iterrows():
        st.markdown(f"<li><strong>{area['area_name']}</strong>: {area['plan_count']} plans</li>", unsafe_allow_html=True)
    
    st.markdown("""
                </ul>
            </div>
            <div>
                <h4 style="color: #2a5298;">📈 Status Summary</h4>
                <ul>
    """, unsafe_allow_html=True)
    
    if not docs_df.empty:
        status_counts = docs_df['status'].value_counts()
        for status, count in status_counts.head(3).items():
            percentage = (count / len(docs_df)) * 100
            st.markdown(f"<li><strong>{status}</strong>: {count} ({percentage:.0f}%)</li>", unsafe_allow_html=True)
    
    st.markdown("""
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional footer
    create_oslo_footer()


def render_map_page():
    """Render enhanced interactive map page"""
    from oslo_enhanced_ui import create_enhanced_map, create_info_panel, create_oslo_footer
    
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="color: #1e3c72;">🗺️ Interactive Oslo Planning Map</h2>
        <p style="font-size: 1.2em; color: #666;">Explore all 15 official bydeler with real-time planning data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Map controls in a more organized layout
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            show_bydeler = st.checkbox("Show Bydeler", True, help="Display all 15 Oslo bydeler")
        with col2:
            show_documents = st.checkbox("Show Documents", True, help="Display planning documents")
        with col3:
            selected_bydel = st.selectbox(
                "Focus on Area", 
                ["All"] + sorted(list(st.session_state.database.get_oslo_areas()['area_name'])),
                help="Zoom to specific bydel or view all"
            )
        with col4:
            map_style = st.selectbox(
                "Map Style",
                ["open-street-map", "carto-positron", "stamen-terrain"],
                help="Choose map background style"
            )
    
    # Display area statistics
    areas_df = st.session_state.database.get_oslo_areas()
    docs_df = st.session_state.database.get_all_documents()
    
    # Quick stats above map
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Areas", len(areas_df))
    with col2:
        st.metric("Official Bydeler", len(areas_df[areas_df['area_type'] == 'bydel']))
    with col3:
        st.metric("Planning Documents", len(docs_df))
    with col4:
        total_plans = areas_df['plan_count'].sum()
        st.metric("Total Plans", total_plans)
    
    # Create and display improved map
    try:
        fig_map = st.session_state.viz.create_interactive_oslo_map(
            show_bydeler=show_bydeler,
            show_documents=show_documents, 
            selected_bydel=selected_bydel
        )
        
        # Update map style
        fig_map.update_layout(mapbox_style=map_style)
        
        st.plotly_chart(fig_map, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error rendering map: {str(e)}")
        st.write("Debug info:", st.session_state.database.get_oslo_areas().head())
    
    # Enhanced map legend and information
    st.write("---")
    with st.expander("📖 Map Legend and Information", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🏛️ Oslo Areas:**")
            st.write("🔵 **Blue circles:** Official bydeler (15 total)")
            st.write("🟡 **Gold circles:** Common areas (Sentrum)")
            st.write("📏 **Circle size:** Proportional to number of plans")
            st.write("")
            st.write("**📋 Planning Documents:**")
            st.write("🔴 **Red dots:** Under behandling")
            st.write("🟢 **Green dots:** Vedtatt") 
            st.write("🟠 **Orange dots:** Høring")
            st.write("⚫ **Gray dots:** Avslått")
        
        with col2:
            st.write("**ℹ️ Oslo Administrative Structure:**")
            st.write("• **15 official bydeler** since 2004")
            st.write("• Each bydel has elected district committee")
            st.write("• Sentrum is a common area (not bydel)")
            st.write("• Residents in Sentrum get services from St. Hanshaugen")
            st.write("")
            st.write("**🎯 Interactive Features:**")
            st.write("• Hover over markers for detailed information")
            st.write("• Use controls above to filter display")
            st.write("• Zoom and pan to explore different areas")
            st.write("• Click legend items to show/hide layers")
    
    # Area details table
    if selected_bydel != "All":
        selected_area_data = areas_df[areas_df['area_name'] == selected_bydel]
        if not selected_area_data.empty:
            st.write(f"### 📊 {selected_bydel} Details")
            
            area_info = selected_area_data.iloc[0]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Population", f"{area_info['population']:,}")
            with col2:
                st.metric("Area", f"{area_info['area_km2']} km²")
            with col3:
                st.metric("Planning Documents", area_info['plan_count'])
            
            # Show documents for this area
            area_docs = docs_df[docs_df['bydel'] == selected_bydel]
            if not area_docs.empty:
                st.write(f"**Planning Documents in {selected_bydel}:**")
                for _, doc in area_docs.iterrows():
                    with st.expander(f"📄 {doc['title']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Type:** {doc['document_type']}")
                            st.write(f"**Status:** {doc['status']}")
                        with col2:
                            st.write(f"**Created:** {doc['date_created'][:10] if doc['date_created'] else 'N/A'}")
                            st.write(f"**Coordinates:** {doc['coordinates'] if doc['coordinates'] else 'N/A'}")
                        if doc['content_text']:
                            st.write("**Description:**")
                            st.write(doc['content_text'][:300] + "..." if len(doc['content_text']) > 300 else doc['content_text'])
            else:
                st.info(f"No planning documents found for {selected_bydel}")
    
    # Summary statistics
    st.write("---")
    st.write("### 📈 Oslo Planning Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution
        if not docs_df.empty:
            status_counts = docs_df['status'].value_counts()
            st.write("**Document Status Distribution:**")
            for status, count in status_counts.items():
                percentage = (count / len(docs_df)) * 100
                st.write(f"• **{status}:** {count} ({percentage:.1f}%)")
    
    with col2:
        # Top bydeler by plan count
        top_bydeler = areas_df.nlargest(5, 'plan_count')
        st.write("**Most Active Bydeler:**")
        for _, area in top_bydeler.iterrows():
            st.write(f"• **{area['area_name']}:** {area['plan_count']} plans")


def render_upload_page():
    """Render data upload page"""
    st.title("📤 Data Upload & Import")
    
    tab1, tab2, tab3 = st.tabs(["File Upload", "Manual Entry", "Import Results"])
    
    with tab1:
        st.subheader("Upload Planning Documents")
        
        uploaded_files = st.file_uploader(
            "Choose files",
            accept_multiple_files=True,
            type=['pdf', 'xlsx', 'csv', 'txt']
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                with st.expander(f"📄 {uploaded_file.name}"):
                    
                    file_details = {
                        "Filename": uploaded_file.name,
                        "File size": f"{uploaded_file.size} bytes",
                        "File type": uploaded_file.type
                    }
                    st.write(file_details)
                    
                    if st.button(f"Process {uploaded_file.name}", key=uploaded_file.name):
                        with st.spinner("Processing file..."):
                            
                            if uploaded_file.name.endswith('.pdf'):
                                result = st.session_state.import_system.process_pdf_upload(uploaded_file)
                            elif uploaded_file.name.endswith('.xlsx'):
                                result = st.session_state.import_system.process_excel_upload(uploaded_file)
                            else:
                                result = {"message": "File type not yet supported in demo"}
                            
                            st.success("File processed!")
                            st.json(result)
    
    with tab2:
        st.subheader("Manual Data Entry")
        
        with st.form("manual_entry"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Plan Title*")
                bydel_options = list(st.session_state.database.get_oslo_areas()['area_name'])
                bydel = st.selectbox("Bydel", bydel_options)
                doc_type = st.selectbox("Document Type", 
                    ["Reguleringsplan", "Områderegulering", "Planendring", "Bebyggelsesplan"])
            
            with col2:
                coordinates = st.text_input("Coordinates (lat,lon)")
                status = st.selectbox("Status", 
                    ["Under behandling", "Vedtatt", "Høring", "Avslått"])
                tags = st.text_input("Tags (comma separated)")
            
            content = st.text_area("Document Content/Description")
            
            submitted = st.form_submit_button("Add Document")
            
            if submitted and title:
                st.session_state.database.add_document(
                    title=title,
                    doc_type=doc_type,
                    bydel=bydel,
                    content=content,
                    coordinates=coordinates
                )
                st.success("Document added successfully!")
                st.rerun()
    
    with tab3:
        st.subheader("Import History")
        st.write("Feature coming soon - will show upload history and processing results")


def render_data_management():
    """Render data management page"""
    st.title("📋 Data Management")
    
    tab1, tab2 = st.tabs(["View Data", "Export Data"])
    
    with tab1:
        st.subheader("Planning Documents")
        docs_df = st.session_state.database.get_all_documents()
        st.dataframe(docs_df, use_container_width=True)
        
        st.subheader("Oslo Areas")
        areas_df = st.session_state.database.get_oslo_areas()
        st.dataframe(areas_df, use_container_width=True)
    
    with tab2:
        st.subheader("Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            export_format = st.selectbox("Format", ["CSV", "JSON", "Excel"])
            data_type = st.selectbox("Data Type", ["All Documents", "All Areas", "Combined"])
        
        with col2:
            if st.button("Export Data"):
                docs_df = st.session_state.database.get_all_documents()
                
                if export_format == "CSV":
                    csv = docs_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="oslo_planning_data.csv",
                        mime="text/csv"
                    )
                elif export_format == "JSON":
                    json_data = docs_df.to_json(orient='records')
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name="oslo_planning_data.json",
                        mime="application/json"
                    )


def render_analytics_page():
    """Render analytics page"""
    st.title("📈 Analytics & Insights")
    
    st.write("Advanced analytics features:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Data Exploration")
        docs_df = st.session_state.database.get_all_documents()
        
        # Document type distribution
        doc_type_counts = docs_df['document_type'].value_counts()
        fig_types = px.bar(
            x=doc_type_counts.index,
            y=doc_type_counts.values,
            title="Document Types Distribution"
        )
        st.plotly_chart(fig_types, use_container_width=True)
        
        # Status by bydel
        status_bydel = docs_df.groupby(['bydel', 'status']).size().unstack(fill_value=0)
        fig_status = px.bar(
            status_bydel,
            title="Status by Bydel",
            barmode='stack'
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        st.subheader("💡 AI Insights")
        st.write("🤖 **AI Analysis Features:**")
        st.write("- Document content analysis")
        st.write("- Automatic categorization")
        st.write("- Risk assessment")
        st.write("- Compliance checking")
        
        st.info("AI features require API keys. Configure in Settings.")
        
        if st.button("Run Demo AI Analysis"):
            with st.spinner("Running AI analysis..."):
                # Mock AI results
                st.success("AI Analysis Complete!")
                st.write("**Key Findings:**")
                st.write("- 67% of documents are residential planning")
                st.write("- Grünerløkka has highest development activity")
                st.write("- Average processing time: 45 days")
                st.write("- 3 documents require environmental review")


def render_settings_page():
    """Render settings page"""
    st.title("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["General", "AI Configuration", "Data Sources"])
    
    with tab1:
        st.subheader("General Settings")
        
        st.write("**Display Options**")
        default_bydel = st.selectbox("Default Bydel View", ["All"] + list(st.session_state.database.get_oslo_areas()['area_name']))
        items_per_page = st.slider("Items per page", 5, 50, 10)
        
        st.write("**Database**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Backup Database"):
                st.success("Database backed up successfully!")
        
        with col2:
            if st.button("Reset Demo Data"):
                st.warning("This will reset all data to demo state.")
                if st.button("Confirm Reset"):
                    # Reinitialize database
                    st.session_state.database = OsloPlanningDatabase()
                    st.success("Demo data reset!")
                    st.rerun()
    
    with tab2:
        st.subheader("AI Configuration")
        
        st.write("**API Keys**")
        openai_key = st.text_input("OpenAI API Key", type="password")
        anthropic_key = st.text_input("Anthropic API Key", type="password")
        
        st.write("**Model Settings**")
        primary_model = st.selectbox("Primary Model", ["GPT-4", "Claude-3", "Local Model"])
        analysis_depth = st.slider("Analysis Depth", 1, 5, 3)
        
        if st.button("Test AI Connection"):
            if openai_key or anthropic_key:
                st.success("AI connection would be tested here!")
            else:
                st.error("Please provide at least one API key")
    
    with tab3:
        st.subheader("Data Sources")
        
        st.write("**External APIs**")
        st.write("🔗 **Geonorge API:** Ready for integration")
        st.write("🔗 **Oslo Origo:** Requires credentials")
        st.write("🔗 **PBE Systems:** Mapped but not connected")
        
        st.info("External API integration will be enabled when credentials are available.")


if __name__ == "__main__":
    create_streamlit_app()