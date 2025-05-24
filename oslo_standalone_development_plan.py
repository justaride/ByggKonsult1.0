#!/usr/bin/env python3
"""
Oslo Planning Dashboard - Standalone Development Plan
Complete roadmap for independent software development
"""

import json
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import openai
import anthropic

class OsloStandaloneDevelopmentPlan:
    """
    Development roadmap for standalone Oslo planning system
    """
    
    def __init__(self):
        self.development_phases = {
            "Phase 1": "Local Data Architecture",
            "Phase 2": "Advanced Graphics & Visualization",
            "Phase 3": "Data Input & Import System",
            "Phase 4": "AI/ML Integration",
            "Phase 5": "Offline-First Architecture",
            "Phase 6": "Enhanced UI/UX",
            "Phase 7": "Export & Reporting System"
        }
    
    def generate_development_roadmap(self):
        """Generate complete development roadmap"""
        return f"""
# 🚀 OSLO PLANNING DASHBOARD - STANDALONE DEVELOPMENT PLAN

## Overview
Transform proof-of-concept into production-ready standalone software that operates independently of external APIs while maintaining full functionality and preparing for future API integration.

## 📊 PHASE 1: LOCAL DATA ARCHITECTURE

### 1.1 SQLite Database Implementation
```python
# Advanced database schema for planning data
class PlanningDatabase:
    def __init__(self, db_path="oslo_planning.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
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
            metadata JSON,
            ai_analysis JSON,
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
            metadata JSON
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
            extraction_results JSON,
            user_notes TEXT
        )
        ''')
        
        # AI analysis results
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            analysis_type TEXT,
            model_used TEXT,
            analysis_date DATETIME,
            results JSON,
            confidence_score REAL,
            FOREIGN KEY (document_id) REFERENCES planning_documents (id)
        )
        ''')
        
        conn.commit()
        conn.close()
```

### 1.2 Data Management System
```python
class DataManager:
    def __init__(self, db_path="oslo_planning.db"):
        self.db = PlanningDatabase(db_path)
    
    def import_json_data(self, json_file):
        """Import existing JSON data into database"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Process and store data
        for item in data.get('oslo_data', {{}}):
            self.store_planning_document(item)
    
    def export_data(self, format='json'):
        """Export data in various formats"""
        if format == 'json':
            return self.export_to_json()
        elif format == 'csv':
            return self.export_to_csv()
        elif format == 'excel':
            return self.export_to_excel()
    
    def backup_database(self):
        """Create timestamped database backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"oslo_planning_backup_{{timestamp}}.db"
        # Implementation for backup
```

## 🎨 PHASE 2: ADVANCED GRAPHICS & VISUALIZATION

### 2.1 Interactive Plotly Dashboard
```python
class AdvancedVisualization:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def create_interactive_oslo_map(self):
        """Create interactive Oslo map with planning data"""
        fig = go.Figure()
        
        # Add Oslo bydeler as polygons
        oslo_geojson = self.load_oslo_geojson()
        
        fig.add_trace(go.Choroplethmapbox(
            geojson=oslo_geojson,
            locations=['Sentrum', 'Grünerløkka', 'Frogner'],  # etc
            z=[15, 8, 12],  # Plan counts
            colorscale='Viridis',
            text=['Sentrum: 15 planer', 'Grünerløkka: 8 planer'],
            hovertemplate='<b>%{{text}}</b><extra></extra>',
            marker_opacity=0.7
        ))
        
        # Add planning documents as markers
        documents = self.data_manager.get_all_documents()
        
        for doc in documents:
            if doc.get('coordinates'):
                lat, lon = self.parse_coordinates(doc['coordinates'])
                fig.add_trace(go.Scattermapbox(
                    lat=[lat],
                    lon=[lon],
                    mode='markers',
                    marker=dict(size=10, color='red'),
                    text=doc['title'],
                    hovertemplate='<b>%{{text}}</b><extra></extra>'
                ))
        
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(center=dict(lat=59.9139, lon=10.7522), zoom=11),
            margin=dict(r=0, t=0, l=0, b=0),
            height=600
        )
        
        return fig
    
    def create_planning_analytics_dashboard(self):
        """Create comprehensive analytics dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Planer per Bydel', 'Trend over Tid', 
                          'Plantyper', 'Status Fordeling'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "pie"}, {"type": "sunburst"}]]
        )
        
        # Add various charts
        # Implementation for each chart type
        
        return fig
    
    def create_3d_city_visualization(self):
        \"\"\"Create 3D visualization of Oslo planning data\"\"\"
        # Three dimensional scatter plot with building heights, plan density, etc.
        fig = go.Figure(data=[go.Scatter3d(
            x=[], y=[], z=[],  # coordinates and heights
            mode='markers',
            marker=dict(
                size=12,
                color=[],  # color by plan type
                colorscale='Viridis',
                opacity=0.8
            )
        )])
        
        return fig

### 2.2 Streamlit Web Interface
```python
def create_streamlit_app():
    st.set_page_config(
        page_title="Oslo Planning Dashboard",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🏛️ Oslo Planning")
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "🗺️ Interactive Map", "📤 Data Upload", 
             "🤖 AI Analysis", "📈 Analytics", "⚙️ Settings"]
        )
    
    if page == "📊 Dashboard":
        render_main_dashboard()
    elif page == "🗺️ Interactive Map":
        render_interactive_map()
    elif page == "📤 Data Upload":
        render_data_upload()
    elif page == "🤖 AI Analysis":
        render_ai_analysis()
    elif page == "📈 Analytics":
        render_analytics_page()
    elif page == "⚙️ Settings":
        render_settings_page()

def render_main_dashboard():
    st.title("📊 Oslo Planning Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Planer", "49", "+3")
    with col2:
        st.metric("Aktive Bydeler", "11", "+1")
    with col3:
        st.metric("PDF Dokumenter", "23", "+5")
    with col4:
        st.metric("AI Analyser", "15", "+2")
    
    # Interactive charts
    viz = AdvancedVisualization(data_manager)
    fig = viz.create_planning_analytics_dashboard()
    st.plotly_chart(fig, use_container_width=True)
```

## 📤 PHASE 3: DATA INPUT & IMPORT SYSTEM

### 3.1 Multi-Format File Upload
```python
class DataImportSystem:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.supported_formats = [
            '.pdf', '.docx', '.xlsx', '.csv', '.json', 
            '.shp', '.geojson', '.kml', '.dwg'
        ]
    
    def process_upload(self, uploaded_file):
        """Process various file formats"""
        file_ext = Path(uploaded_file.name).suffix.lower()
        
        if file_ext == '.pdf':
            return self.process_pdf(uploaded_file)
        elif file_ext == '.xlsx':
            return self.process_excel(uploaded_file)
        elif file_ext == '.csv':
            return self.process_csv(uploaded_file)
        elif file_ext == '.json':
            return self.process_json(uploaded_file)
        elif file_ext == '.geojson':
            return self.process_geojson(uploaded_file)
        elif file_ext == '.shp':
            return self.process_shapefile(uploaded_file)
        else:
            raise ValueError(f"Unsupported file format: {{file_ext}}")
    
    def process_pdf(self, pdf_file):
        """Enhanced PDF processing with multiple libraries"""
        import pdfplumber
        import PyPDF2
        import fitz  # PyMuPDF
        
        results = {{
            'text_content': '',
            'metadata': {{}},
            'coordinates': [],
            'plan_info': {{}}
        }}
        
        # Try multiple extraction methods
        try:
            # Method 1: pdfplumber (best for tables)
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    results['text_content'] += page.extract_text() or ''
                    
                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        results['metadata']['tables'] = tables
        except:
            pass
        
        try:
            # Method 2: PyMuPDF (best for coordinates)
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            for page in doc:
                text = page.get_text()
                results['text_content'] += text
                
                # Extract coordinates
                coords = self.extract_coordinates_from_text(text)
                results['coordinates'].extend(coords)
        except:
            pass
        
        # AI-powered analysis
        results['ai_analysis'] = self.analyze_with_ai(results['text_content'])
        
        return results
    
    def process_excel(self, excel_file):
        """Process Excel files with planning data"""
        df = pd.read_excel(excel_file)
        
        # Auto-detect columns
        column_mapping = self.auto_detect_columns(df.columns)
        
        # Process data
        processed_data = []
        for _, row in df.iterrows():
            doc = {{
                'title': row.get(column_mapping.get('title', ''), ''),
                'bydel': row.get(column_mapping.get('bydel', ''), ''),
                'coordinates': row.get(column_mapping.get('coordinates', ''), ''),
                'date': row.get(column_mapping.get('date', ''), ''),
                'status': row.get(column_mapping.get('status', ''), '')
            }}
            processed_data.append(doc)
        
        return processed_data
    
    def process_geojson(self, geojson_file):
        """Process GeoJSON geographical data"""
        import geopandas as gpd
        
        gdf = gpd.read_file(geojson_file)
        
        # Extract planning-relevant information
        processed_features = []
        for _, feature in gdf.iterrows():
            processed_features.append({{
                'geometry': feature['geometry'],
                'properties': feature.drop('geometry').to_dict(),
                'coordinates': self.extract_centroid(feature['geometry'])
            }})
        
        return processed_features
```

### 3.2 Interactive Data Entry Forms
```python
def render_data_upload():
    st.title("📤 Data Upload & Import")
    
    tab1, tab2, tab3 = st.tabs(["File Upload", "Manual Entry", "Bulk Import"])
    
    with tab1:
        st.subheader("Upload Planning Documents")
        
        uploaded_files = st.file_uploader(
            "Choose files",
            accept_multiple_files=True,
            type=['pdf', 'xlsx', 'csv', 'json', 'geojson']
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                with st.expander(f"📄 {{uploaded_file.name}}"):
                    if st.button(f"Process {{uploaded_file.name}}"):
                        with st.spinner("Processing..."):
                            results = import_system.process_upload(uploaded_file)
                            st.success("File processed successfully!")
                            st.json(results)
    
    with tab2:
        st.subheader("Manual Data Entry")
        
        with st.form("manual_entry"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Plan Title*")
                bydel = st.selectbox("Bydel", oslo_bydeler)
                plan_type = st.selectbox("Plan Type", 
                    ["Reguleringsplan", "Områderegulering", "Planendring"])
                
            with col2:
                coordinates = st.text_input("Coordinates (lat, lon)")
                date_created = st.date_input("Date Created")
                status = st.selectbox("Status", 
                    ["Under behandling", "Vedtatt", "Høring", "Avslått"])
            
            description = st.text_area("Description")
            tags = st.text_input("Tags (comma separated)")
            
            submitted = st.form_submit_button("Add Planning Document")
            if submitted and title:
                # Save to database
                st.success("Planning document added!")
    
    with tab3:
        st.subheader("Bulk Import from APIs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Import from Geonorge"):
                with st.spinner("Fetching from Geonorge..."):
                    # Use existing Geonorge integration
                    pass
        
        with col2:
            if st.button("Import Demo Data"):
                with st.spinner("Loading demo data..."):
                    # Load comprehensive demo dataset
                    pass
```

## 🤖 PHASE 4: AI/ML INTEGRATION

### 4.1 Multi-Model AI Analysis
```python
class AIAnalysisEngine:
    def __init__(self):
        self.openai_client = openai.OpenAI()
        self.anthropic_client = anthropic.Anthropic()
        self.local_models = self.load_local_models()
    
    def analyze_planning_document(self, text_content, analysis_type="comprehensive"):
        """Multi-model analysis of planning documents"""
        
        results = {{
            'document_summary': '',
            'key_entities': [],
            'planning_categories': [],
            'risk_assessment': '',
            'recommendations': [],
            'compliance_check': {{}},
            'sentiment_analysis': {{}},
            'coordinate_extraction': [],
            'date_extraction': []
        }}
        
        # OpenAI GPT-4 Analysis
        try:
            gpt_analysis = self.openai_analysis(text_content)
            results.update(gpt_analysis)
        except Exception as e:
            st.warning(f"OpenAI analysis failed: {{e}}")
        
        # Anthropic Claude Analysis
        try:
            claude_analysis = self.anthropic_analysis(text_content)
            results.update(claude_analysis)
        except Exception as e:
            st.warning(f"Anthropic analysis failed: {{e}}")
        
        # Local ML Models
        results.update(self.local_ml_analysis(text_content))
        
        return results
    
    def openai_analysis(self, text):
        """OpenAI GPT-4 analysis"""
        prompt = f'''
        Analyze this Norwegian planning document and extract:
        1. Document summary (Norwegian)
        2. Key planning entities (addresses, areas, building types)
        3. Planning categories (reguleringsplan, områderegulering, etc.)
        4. Risk assessment for development
        5. Compliance recommendations
        6. Coordinates if mentioned
        7. Important dates
        
        Document text:
        {{text}}
        
        Return response in JSON format.
        '''
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{{"role": "user", "content": prompt}}],
            temperature=0.3
        )
        
        return json.loads(response.choices[0].message.content)
    
    def anthropic_analysis(self, text):
        """Anthropic Claude analysis"""
        prompt = f'''
        As a Norwegian planning expert, analyze this document for:
        - Regulatory compliance issues
        - Environmental impact considerations
        - Infrastructure requirements
        - Community impact assessment
        
        Text: {{text}}
        '''
        
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            messages=[{{"role": "user", "content": prompt}}]
        )
        
        return {{"expert_analysis": response.content[0].text}}
    
    def local_ml_analysis(self, text):
        """Local ML models for specific tasks"""
        from transformers import pipeline
        
        results = {{}}
        
        # Named Entity Recognition (Norwegian)
        try:
            ner_pipeline = pipeline("ner", 
                model="NbAiLab/nb-bert-base", 
                tokenizer="NbAiLab/nb-bert-base")
            entities = ner_pipeline(text[:512])  # Limit for BERT
            results['entities'] = entities
        except:
            pass
        
        # Sentiment Analysis
        try:
            sentiment_pipeline = pipeline("sentiment-analysis", 
                model="cardiffnlp/twitter-xlm-roberta-base-sentiment")
            sentiment = sentiment_pipeline(text[:512])
            results['sentiment'] = sentiment[0]
        except:
            pass
        
        # Text Classification (planning categories)
        results['planning_classification'] = self.classify_planning_document(text)
        
        return results
    
    def clustering_analysis(self, documents):
        """Cluster similar planning documents"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        # Vectorize documents
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        X = vectorizer.fit_transform([doc['content'] for doc in documents])
        
        # K-means clustering
        kmeans = KMeans(n_clusters=5, random_state=42)
        clusters = kmeans.fit_predict(X)
        
        # Assign clusters to documents
        for i, doc in enumerate(documents):
            doc['cluster'] = int(clusters[i])
        
        return documents
```

### 4.2 AI-Powered Insights Dashboard
```python
def render_ai_analysis():
    st.title("🤖 AI-Powered Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Document Analysis", "Predictive Insights", 
        "Pattern Recognition", "AI Settings"
    ])
    
    with tab1:
        st.subheader("Analyze Planning Documents")
        
        # Document selection
        documents = data_manager.get_all_documents()
        doc_options = [f"{{doc['title']}} ({{doc['bydel']}})" 
                      for doc in documents]
        
        selected_doc = st.selectbox("Select document to analyze", doc_options)
        
        if selected_doc and st.button("🔍 Analyze with AI"):
            with st.spinner("AI analysis in progress..."):
                # Get document content
                doc_content = "..."  # Get from database
                
                # Run AI analysis
                ai_engine = AIAnalysisEngine()
                results = ai_engine.analyze_planning_document(doc_content)
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Summary")
                    st.write(results.get('document_summary', ''))
                    
                    st.subheader("🏷️ Key Entities")
                    for entity in results.get('key_entities', []):
                        st.tag(entity)
                
                with col2:
                    st.subheader("⚠️ Risk Assessment")
                    st.write(results.get('risk_assessment', ''))
                    
                    st.subheader("💡 Recommendations")
                    for rec in results.get('recommendations', []):
                        st.write(f"• {{rec}}")
    
    with tab2:
        st.subheader("🔮 Predictive Insights")
        
        # Trend prediction
        st.write("**Development Trend Prediction**")
        
        # Mock prediction data
        future_dates = pd.date_range(start='2025-06-01', periods=12, freq='M')
        predicted_plans = np.random.poisson(5, 12)  # Poisson distribution
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=predicted_plans,
            mode='lines+markers',
            name='Predicted New Plans',
            line=dict(color='blue')
        ))
        
        st.plotly_chart(fig)
        
        # Risk heatmap
        st.write("**Development Risk Heatmap**")
        oslo_areas = ['Sentrum', 'Grünerløkka', 'Frogner', 'Sagene']
        risk_factors = ['Traffic Impact', 'Environmental', 'Infrastructure', 'Community']
        
        risk_matrix = np.random.rand(len(oslo_areas), len(risk_factors))
        
        fig = px.imshow(risk_matrix, 
                       x=risk_factors, 
                       y=oslo_areas,
                       color_continuous_scale='Reds')
        st.plotly_chart(fig)
    
    with tab3:
        st.subheader("🔍 Pattern Recognition")
        
        # Document similarity network
        if st.button("Generate Document Similarity Network"):
            # Create network graph of similar documents
            import networkx as nx
            
            G = nx.Graph()
            # Add nodes and edges based on document similarity
            # Implementation for network visualization
            
            st.success("Pattern analysis complete!")
    
    with tab4:
        st.subheader("⚙️ AI Configuration")
        
        st.write("**API Keys**")
        openai_key = st.text_input("OpenAI API Key", type="password")
        anthropic_key = st.text_input("Anthropic API Key", type="password")
        
        st.write("**Model Selection**")
        primary_model = st.selectbox("Primary Analysis Model", 
            ["GPT-4", "Claude-3", "Local Models", "Ensemble"])
        
        st.write("**Analysis Options**")
        enable_sentiment = st.checkbox("Enable Sentiment Analysis", True)
        enable_ner = st.checkbox("Enable Named Entity Recognition", True)
        enable_clustering = st.checkbox("Enable Document Clustering", True)
        
        if st.button("Save AI Settings"):
            st.success("AI settings saved!")
```

## 🔧 PHASE 5: OFFLINE-FIRST ARCHITECTURE

### 5.1 Local Storage & Sync
```python
class OfflineFirstArchitecture:
    def __init__(self):
        self.local_db = "oslo_planning_local.db"
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        
    def enable_offline_mode(self):
        """Configure system for offline operation"""
        # Cache all necessary data locally
        self.cache_map_tiles()
        self.cache_ai_models()
        self.preload_demo_data()
        
    def cache_map_tiles(self):
        """Download and cache map tiles for Oslo"""
        # Download Oslo map tiles for offline use
        oslo_bounds = {{
            'north': 59.95,
            'south': 59.85,
            'east': 10.85,
            'west': 10.65
        }}
        
        # Implementation for tile caching
        
    def sync_when_online(self):
        """Sync local changes when internet is available"""
        if self.check_internet_connection():
            # Upload local changes
            # Download remote updates
            # Resolve conflicts
            pass
```

### 5.2 Progressive Web App (PWA) Features
```python
def create_pwa_manifest():
    """Create PWA manifest for mobile installation"""
    manifest = {{
        "name": "Oslo Planning Dashboard",
        "short_name": "OsloPlan",
        "description": "Oslo Municipality Planning Dashboard",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#1e3c72",
        "theme_color": "#2a5298",
        "icons": [
            {{
                "src": "icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            }},
            {{
                "src": "icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }}
        ]
    }}
    
    with open('manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
```

## 🎨 PHASE 6: ENHANCED UI/UX

### 6.1 Modern Component Library
```python
# Custom Streamlit components for Oslo branding
def oslo_metric_card(title, value, delta=None, color="blue"):
    \"\"\"Custom metric card with Oslo styling\"\"\"
    delta_html = f'<span style="color: green;">{{delta}}</span>' if delta else ''
    
    st.markdown(f'''
    <div style="
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <h3 style="margin: 0; font-size: 1.2em;">{{title}}</h3>
        <h1 style="margin: 10px 0; font-size: 2.5em;">{{value}}</h1>
        {{delta_html}}
    </div>
    ''', unsafe_allow_html=True)

def oslo_progress_bar(value, max_value, label):
    \"\"\"Custom progress bar with Oslo styling\"\"\"
    percentage = (value / max_value) * 100
    
    st.markdown(f'''
    <div style="margin: 20px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span>{{label}}</span>
            <span>{{value}}/{{max_value}}</span>
        </div>
        <div style="
            background: #e0e0e0;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
        ">
            <div style="
                background: linear-gradient(90deg, #1e3c72, #2a5298);
                height: 100%;
                width: {{percentage}}%;
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
```

### 6.2 Responsive Design System
```python
def create_responsive_layout():
    \"\"\"Create responsive layout that adapts to screen size\"\"\"
    
    # Detect screen size using browser info
    screen_width = st.session_state.get('screen_width', 1200)
    
    if screen_width < 768:  # Mobile
        cols = st.columns(1)
        mobile_layout()
    elif screen_width < 1024:  # Tablet
        cols = st.columns(2)
        tablet_layout(cols)
    else:  # Desktop
        cols = st.columns([2, 1, 1])
        desktop_layout(cols)

def mobile_layout():
    \"\"\"Optimized layout for mobile devices\"\"\"
    st.write("📱 Mobile view optimized")
    # Vertical stack layout
    
def tablet_layout(cols):
    \"\"\"Optimized layout for tablets\"\"\"
    with cols[0]:
        st.write("📊 Main content")
    with cols[1]:
        st.write("📋 Sidebar")

def desktop_layout(cols):
    \"\"\"Full desktop layout\"\"\"
    with cols[0]:
        st.write("📊 Main dashboard")
    with cols[1]:
        st.write("📋 Quick stats")
    with cols[2]:
        st.write("🔔 Notifications")
```

## 📊 PHASE 7: EXPORT & REPORTING SYSTEM

### 7.1 Advanced Report Generation
```python
class ReportGenerator:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        
    def generate_comprehensive_report(self, bydel=None, date_range=None):
        \"\"\"Generate comprehensive planning report\"\"\"
        
        # Gather data
        documents = self.data_manager.get_documents(bydel=bydel, date_range=date_range)
        ai_analysis = self.data_manager.get_ai_analysis(documents)
        
        # Generate report sections
        report = {{
            'executive_summary': self.generate_executive_summary(documents),
            'data_overview': self.generate_data_overview(documents),
            'ai_insights': self.generate_ai_insights(ai_analysis),
            'visualizations': self.generate_report_visualizations(documents),
            'recommendations': self.generate_recommendations(documents, ai_analysis),
            'appendices': self.generate_appendices(documents)
        }}
        
        return report
    
    def export_to_pdf(self, report, filename):
        \"\"\"Export report to professional PDF\"\"\"
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Oslo kommune styling
        oslo_style = ParagraphStyle(
            'Oslo',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.Color(0.12, 0.24, 0.45),  # Oslo blue
            spaceAfter=30
        )
        
        story = []
        
        # Title page
        story.append(Paragraph("Oslo Kommune", oslo_style))
        story.append(Paragraph("Planning Analysis Report", styles['Heading2']))
        story.append(Spacer(1, 20))
        
        # Executive summary
        story.append(Paragraph("Executive Summary", styles['Heading2']))
        story.append(Paragraph(report['executive_summary'], styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Add charts as images
        for viz in report['visualizations']:
            story.append(Image(viz['image_path'], width=400, height=300))
            story.append(Spacer(1, 10))
        
        doc.build(story)
        
    def export_to_excel(self, report, filename):
        \"\"\"Export detailed data to Excel workbook\"\"\"
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            # Multiple sheets for different data types
            
            # Planning documents sheet
            docs_df = pd.DataFrame(report['data_overview']['documents'])
            docs_df.to_excel(writer, sheet_name='Planning Documents', index=False)
            
            # AI analysis sheet
            ai_df = pd.DataFrame(report['ai_insights'])
            ai_df.to_excel(writer, sheet_name='AI Analysis', index=False)
            
            # Statistics sheet
            stats_df = pd.DataFrame(report['data_overview']['statistics'])
            stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            
            # Format workbook
            workbook = writer.book
            oslo_format = workbook.add_format({{
                'bg_color': '#1e3c72',
                'font_color': 'white',
                'bold': True
            }})
            
            # Apply formatting to headers
            for sheet_name in ['Planning Documents', 'AI Analysis', 'Statistics']:
                worksheet = writer.sheets[sheet_name]
                worksheet.set_row(0, 20, oslo_format)
```

### 7.2 Interactive Export Interface
```python
def render_export_page():
    st.title("📤 Export & Reporting")
    
    tab1, tab2, tab3 = st.tabs(["Quick Export", "Custom Reports", "Scheduled Reports"])
    
    with tab1:
        st.subheader("Quick Data Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            export_format = st.selectbox("Format", 
                ["JSON", "CSV", "Excel", "PDF Report", "GeoJSON"])
            
            bydel_filter = st.multiselect("Filter by Bydel", oslo_bydeler)
            
        with col2:
            date_range = st.date_input("Date Range", value=[])
            
            include_ai = st.checkbox("Include AI Analysis", True)
            include_viz = st.checkbox("Include Visualizations", True)
        
        if st.button("🚀 Export Data"):
            with st.spinner("Generating export..."):
                # Generate export based on selections
                export_data = generate_export(
                    format=export_format,
                    bydel_filter=bydel_filter,
                    date_range=date_range,
                    include_ai=include_ai
                )
                
                # Provide download link
                st.download_button(
                    label=f"📁 Download {{export_format}} File",
                    data=export_data,
                    file_name=f"oslo_planning_export.{{export_format.lower()}}",
                    mime=get_mime_type(export_format)
                )
    
    with tab2:
        st.subheader("📊 Custom Report Builder")
        
        with st.form("custom_report"):
            report_name = st.text_input("Report Name")
            
            st.write("**Report Sections**")
            include_summary = st.checkbox("Executive Summary", True)
            include_data = st.checkbox("Data Overview", True)
            include_ai = st.checkbox("AI Insights", True)
            include_viz = st.checkbox("Visualizations", True)
            include_maps = st.checkbox("Interactive Maps", False)
            
            st.write("**Filters**")
            bydel_filter = st.multiselect("Bydeler", oslo_bydeler)
            plan_types = st.multiselect("Plan Types", 
                ["Reguleringsplan", "Områderegulering", "Planendring"])
            
            submitted = st.form_submit_button("Generate Custom Report")
            
            if submitted:
                with st.spinner("Building custom report..."):
                    report = ReportGenerator(data_manager).generate_comprehensive_report(
                        bydel=bydel_filter,
                        plan_types=plan_types
                    )
                    st.success("Custom report generated!")
    
    with tab3:
        st.subheader("⏰ Scheduled Reports")
        
        st.write("**Automatic Report Generation**")
        
        with st.form("schedule_report"):
            schedule_name = st.text_input("Schedule Name")
            frequency = st.selectbox("Frequency", 
                ["Daily", "Weekly", "Monthly", "Quarterly"])
            
            email_recipients = st.text_area("Email Recipients (one per line)")
            
            report_type = st.selectbox("Report Type",
                ["Summary Report", "Full Analysis", "AI Insights Only"])
            
            submitted = st.form_submit_button("Create Schedule")
            
            if submitted:
                st.success("Report schedule created!")
                st.info("Reports will be generated automatically and sent to specified recipients.")

# Implementation continuation...
```

## 🚀 DEVELOPMENT PRIORITIES

### Immediate (Week 1-2):
1. ✅ SQLite database implementation
2. ✅ File upload system (PDF, Excel, CSV)
3. ✅ Basic Streamlit interface
4. ✅ AI integration framework

### Short-term (Month 1):
1. 📊 Advanced Plotly visualizations
2. 🗺️ Interactive Oslo map with real coordinates
3. 🤖 Multi-model AI analysis pipeline
4. 📱 Responsive design implementation

### Medium-term (Month 2-3):
1. 🔧 Offline-first architecture
2. 📤 Comprehensive export system
3. 🎨 Advanced UI components
4. 📊 Custom reporting engine

### Long-term (Month 4-6):
1. 🌐 Progressive Web App features
2. 🤖 Advanced ML models for prediction
3. 🔄 Real-time collaboration features
4. 🚀 Production deployment preparation

## 💻 IMPLEMENTATION COMMANDS

```bash
# Install required packages
pip install streamlit plotly pandas sqlite3 pdfplumber PyPDF2 
pip install scikit-learn transformers openai anthropic geopandas
pip install reportlab xlsxwriter openpyxl

# Run the standalone application
streamlit run oslo_standalone_app.py

# For development
pip install streamlit-folium streamlit-plotly-events
pip install python-dotenv requests beautifulsoup4
```

This development plan transforms the Oslo planning dashboard into a comprehensive standalone software system that can operate independently while preparing for future API integration.
"""

def main():
    print("🚀 OSLO STANDALONE DEVELOPMENT PLAN")
    print("="*50)
    
    plan = OsloStandaloneDevelopmentPlan()
    roadmap = plan.generate_development_roadmap()
    
    # Save roadmap to file
    with open('oslo_development_roadmap.md', 'w', encoding='utf-8') as f:
        f.write(roadmap)
    
    print("📋 Complete development roadmap saved to: oslo_development_roadmap.md")
    print("\n🎯 Next steps:")
    print("1. Review the 7-phase development plan")
    print("2. Start with Phase 1: Local Data Architecture")
    print("3. Implement SQLite database and file upload system")
    print("4. Build advanced visualizations with Plotly")
    print("5. Integrate AI models for document analysis")
    
    return roadmap

if __name__ == "__main__":
    main()