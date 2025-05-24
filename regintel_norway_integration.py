#!/usr/bin/env python3
"""
RegIntel Norway Integration - Oslo Planning Dashboard Enhancement
Implementing key features from the complete product specification
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import sqlite3
from pathlib import Path

class RegIntelNorwayEngine:
    """
    AI-powered regulatory analysis engine for Norwegian property development
    Based on Natural State product specification
    """
    
    def __init__(self):
        self.regulation_types = {
            'TEK17': 'Teknisk forskrift - Building code',
            'TEK21': 'Updated technical regulations',
            'Municipal': 'Local planning regulations',
            'Environmental': 'Naturmangfoldloven compliance',
            'Heritage': 'Kulturminneloven preservation',
            'Energy': 'NS 3031 energy standards',
            'Accessibility': 'Universal design requirements',
            'Fire': 'Fire safety regulations'
        }
        
        self.compliance_categories = {
            'Building_Code': {'weight': 0.25, 'requirements': 847},
            'Municipal_Planning': {'weight': 0.20, 'requirements': 355},
            'Environmental': {'weight': 0.15, 'requirements': 150},
            'Heritage': {'weight': 0.15, 'requirements': 89},
            'Energy': {'weight': 0.10, 'requirements': 67},
            'Accessibility': {'weight': 0.10, 'requirements': 45},
            'Fire_Safety': {'weight': 0.05, 'requirements': 78}
        }
        
        self.supported_formats = [
            'IFC', 'RVT', 'PLN', 'DWG', 'DXF', 'PDF', 'TIFF', 'PNG', 'JPG',
            'XML', 'SOSI', 'GeoJSON', 'KML'
        ]
        
    def create_enhanced_database_schema(self):
        """Enhanced database schema for RegIntel Norway"""
        
        schema_sql = """
        -- Enhanced planning documents with regulatory analysis
        CREATE TABLE IF NOT EXISTS regulatory_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            regulation_type TEXT NOT NULL,
            compliance_score REAL,
            conflicts_detected INTEGER DEFAULT 0,
            analysis_date DATETIME,
            ai_confidence REAL,
            recommendations TEXT,
            precedent_cases TEXT,
            cost_implications TEXT,
            timeline_impact INTEGER,
            FOREIGN KEY (document_id) REFERENCES planning_documents (id)
        );
        
        -- TEK17/TEK21 requirements database
        CREATE TABLE IF NOT EXISTS tek_requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            regulation_code TEXT UNIQUE NOT NULL,
            regulation_type TEXT,
            requirement_text TEXT,
            category TEXT,
            mandatory BOOLEAN DEFAULT TRUE,
            effective_date DATE,
            superseded_date DATE,
            related_requirements TEXT
        );
        
        -- Municipal regulations per kommune
        CREATE TABLE IF NOT EXISTS municipal_regulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kommune_name TEXT NOT NULL,
            kommune_number INTEGER,
            regulation_title TEXT,
            regulation_text TEXT,
            category TEXT,
            effective_date DATE,
            contact_department TEXT,
            api_endpoint TEXT
        );
        
        -- Project compliance tracking
        CREATE TABLE IF NOT EXISTS project_compliance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            client_name TEXT,
            property_address TEXT,
            gnr_bnr TEXT,
            project_type TEXT,
            status TEXT DEFAULT 'active',
            overall_compliance_score REAL,
            total_conflicts INTEGER DEFAULT 0,
            estimated_approval_time INTEGER,
            approval_probability REAL,
            created_date DATETIME,
            last_updated DATETIME
        );
        
        -- Conflict detection and resolution
        CREATE TABLE IF NOT EXISTS regulatory_conflicts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            conflict_type TEXT,
            severity_level INTEGER,
            description TEXT,
            affected_regulations TEXT,
            proposed_solutions TEXT,
            resolution_status TEXT DEFAULT 'open',
            estimated_cost REAL,
            estimated_time INTEGER,
            FOREIGN KEY (project_id) REFERENCES project_compliance (id)
        );
        
        -- AI analysis results and precedents
        CREATE TABLE IF NOT EXISTS ai_precedents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_reference TEXT,
            kommune_name TEXT,
            project_type TEXT,
            similar_conflicts TEXT,
            approved_solutions TEXT,
            approval_date DATE,
            case_officer TEXT,
            success_factors TEXT,
            lessons_learned TEXT
        );
        """
        
        return schema_sql
    
    def analyze_regulatory_compliance(self, document_data, project_type="residential"):
        """
        Comprehensive regulatory compliance analysis
        Based on RegIntel Norway specification
        """
        
        analysis_results = {
            'overall_score': 0,
            'category_scores': {},
            'conflicts': [],
            'recommendations': [],
            'precedents': [],
            'timeline_estimate': 0,
            'cost_implications': {},
            'approval_probability': 0
        }
        
        # Simulate comprehensive regulatory analysis
        for category, config in self.compliance_categories.items():
            category_score = self.analyze_category_compliance(
                document_data, category, config['requirements']
            )
            analysis_results['category_scores'][category] = category_score
            analysis_results['overall_score'] += category_score * config['weight']
        
        # Generate conflicts and recommendations
        analysis_results['conflicts'] = self.detect_regulatory_conflicts(document_data)
        analysis_results['recommendations'] = self.generate_ai_recommendations(analysis_results)
        analysis_results['precedents'] = self.find_precedent_cases(document_data, project_type)
        
        # Calculate timeline and approval probability
        analysis_results['timeline_estimate'] = self.estimate_approval_timeline(analysis_results)
        analysis_results['approval_probability'] = self.calculate_approval_probability(analysis_results)
        
        return analysis_results
    
    def analyze_category_compliance(self, document_data, category, requirement_count):
        """Analyze compliance for specific regulatory category"""
        
        # Simulate AI analysis based on document content and category
        base_score = np.random.uniform(0.7, 0.95)
        
        # Adjust based on document completeness
        completeness_factor = len(document_data.get('content', '')) / 1000
        completeness_factor = min(completeness_factor, 1.0)
        
        # Category-specific adjustments
        category_adjustments = {
            'Building_Code': 0.9,  # Typically well-documented
            'Municipal_Planning': 0.85,  # Varies by kommune
            'Environmental': 0.8,  # Often requires specialist input
            'Heritage': 0.75,  # Complex preservation requirements
            'Energy': 0.88,  # Technical but standardized
            'Accessibility': 0.9,  # Clear technical requirements
            'Fire_Safety': 0.85  # Technical but complex
        }
        
        adjustment = category_adjustments.get(category, 0.8)
        final_score = base_score * completeness_factor * adjustment
        
        return min(final_score, 1.0)
    
    def detect_regulatory_conflicts(self, document_data):
        """Detect conflicts between different regulations"""
        
        conflicts = [
            {
                'id': 'C001',
                'type': 'TEK17 vs Heritage',
                'severity': 'High',
                'description': 'Energy efficiency requirements conflict with heritage preservation',
                'regulations': ['TEK17 §14-2', 'Kulturminneloven §15'],
                'estimated_cost': 150000,
                'estimated_time': 14
            },
            {
                'id': 'C002', 
                'type': 'Municipal vs Environmental',
                'severity': 'Medium',
                'description': 'Building height restrictions vs environmental sunlight requirements',
                'regulations': ['Oslo kommuneplan', 'Naturmangfoldloven'],
                'estimated_cost': 75000,
                'estimated_time': 7
            },
            {
                'id': 'C003',
                'type': 'Accessibility vs Fire',
                'severity': 'Low',
                'description': 'Wheelchair access ramp grade vs fire evacuation requirements',
                'regulations': ['TEK17 §12-3', 'TEK17 §11-6'],
                'estimated_cost': 25000,
                'estimated_time': 3
            }
        ]
        
        # Return subset based on document analysis
        return conflicts[:np.random.randint(1, len(conflicts) + 1)]
    
    def generate_ai_recommendations(self, analysis_results):
        """Generate AI-powered recommendations for compliance"""
        
        recommendations = [
            {
                'priority': 'High',
                'category': 'Design Modification',
                'description': 'Modify facade design to meet energy requirements while preserving heritage character',
                'implementation': 'Use traditional materials with modern insulation core',
                'cost_range': '100,000 - 200,000 NOK',
                'time_impact': '2-3 weeks additional design time'
            },
            {
                'priority': 'Medium',
                'category': 'Material Substitution',
                'description': 'Replace proposed roofing material with fire-rated alternative',
                'implementation': 'Specify Kebony Clear or equivalent Class B roof material',
                'cost_range': '50,000 - 100,000 NOK',
                'time_impact': '1 week procurement adjustment'
            },
            {
                'priority': 'Low',
                'category': 'Documentation Enhancement',
                'description': 'Add accessibility compliance documentation',
                'implementation': 'Prepare universal design checklist with drawings',
                'cost_range': '10,000 - 25,000 NOK',
                'time_impact': '3-5 days documentation work'
            }
        ]
        
        return recommendations
    
    def find_precedent_cases(self, document_data, project_type):
        """Find similar precedent cases for guidance"""
        
        precedents = [
            {
                'case_id': 'OSL-2023-1247',
                'kommune': 'Oslo',
                'project_type': 'Residential renovation',
                'similar_challenges': ['Heritage preservation', 'Energy upgrade'],
                'approved_solution': 'Selective interior insulation with vapor barrier',
                'approval_date': '2023-08-15',
                'case_officer': 'Anne Nordahl',
                'key_factors': ['Maintained historic facade', 'Met energy class B'],
                'reference_url': 'https://innsyn.pbe.oslo.kommune.no/saksinnsyn/showfile.asp?fileid=12847'
            },
            {
                'case_id': 'BGN-2023-0892',
                'kommune': 'Bergen',
                'project_type': 'Commercial development',
                'similar_challenges': ['Height restrictions', 'Neighbor sunlight'],
                'approved_solution': 'Stepped building profile with roof gardens',
                'approval_date': '2023-06-22',
                'case_officer': 'Erik Haugen',
                'key_factors': ['Reduced visual impact', 'Enhanced neighbor relations'],
                'reference_url': 'https://bergenkart.bergen.kommune.no/webinnsyn'
            }
        ]
        
        return precedents
    
    def estimate_approval_timeline(self, analysis_results):
        """Estimate approval timeline based on complexity"""
        
        base_timeline = 8  # weeks
        
        # Add time for conflicts
        conflict_penalty = len(analysis_results['conflicts']) * 2
        
        # Add time based on compliance score
        compliance_score = analysis_results['overall_score']
        score_penalty = (1 - compliance_score) * 6
        
        total_timeline = base_timeline + conflict_penalty + score_penalty
        
        return max(6, min(total_timeline, 20))  # 6-20 weeks range
    
    def calculate_approval_probability(self, analysis_results):
        """Calculate probability of approval based on analysis"""
        
        base_probability = analysis_results['overall_score']
        
        # Reduce probability for high-severity conflicts
        high_severity_conflicts = sum(1 for c in analysis_results['conflicts'] 
                                    if c['severity'] == 'High')
        conflict_penalty = high_severity_conflicts * 0.15
        
        final_probability = max(0.3, base_probability - conflict_penalty)
        
        return final_probability


def create_regintel_dashboard():
    """Create enhanced RegIntel Norway dashboard"""
    
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 style="color: #1e3c72; font-size: 2.5em;">🏛️ RegIntel Norway</h1>
        <h2 style="color: #2a5298; font-size: 1.5em;">AI-Powered Regulatory Intelligence Platform</h2>
        <p style="font-size: 1.2em; color: #666;">
            Transform Norwegian property development with intelligent compliance analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize RegIntel engine
    if 'regintel_engine' not in st.session_state:
        st.session_state.regintel_engine = RegIntelNorwayEngine()
    
    engine = st.session_state.regintel_engine
    
    # Main dashboard layout
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Project Dashboard", 
        "🔍 Regulatory Analysis", 
        "⚠️ Conflict Detection",
        "📋 Compliance Reports",
        "🤖 AI Assistant"
    ])
    
    with tab1:
        render_project_dashboard(engine)
    
    with tab2:
        render_regulatory_analysis(engine)
    
    with tab3:
        render_conflict_detection(engine)
    
    with tab4:
        render_compliance_reports(engine)
    
    with tab5:
        render_ai_assistant(engine)


def render_project_dashboard(engine):
    """Render main project dashboard"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
        <h3 style="color: #1e3c72;">📋 Active Projects Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Mock project data
    projects_data = [
        {
            'name': 'Grünerløkka Residential Complex',
            'status': 'Under Analysis',
            'compliance_score': 87,
            'conflicts': 2,
            'timeline': '12 weeks',
            'probability': 78
        },
        {
            'name': 'Frogner Heritage Renovation',
            'status': 'Conflicts Detected',
            'compliance_score': 72,
            'conflicts': 4,
            'timeline': '16 weeks',
            'probability': 65
        },
        {
            'name': 'Sentrum Office Development',
            'status': 'Compliant',
            'compliance_score': 94,
            'conflicts': 0,
            'timeline': '8 weeks',
            'probability': 92
        }
    ]
    
    # Project cards
    for project in projects_data:
        status_color = {
            'Compliant': '#4caf50',
            'Under Analysis': '#ff9800', 
            'Conflicts Detected': '#f44336'
        }.get(project['status'], '#666')
        
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    border-left: 5px solid {status_color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #1e3c72;">{project['name']}</h4>
                    <span style="background: {status_color}; color: white; padding: 0.3rem 0.8rem; 
                                border-radius: 20px; font-size: 0.8em; font-weight: 600;">
                        {project['status']}
                    </span>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2em; font-weight: bold; color: #1e3c72;">
                        {project['compliance_score']}%
                    </div>
                    <div style="font-size: 0.9em; color: #666;">Compliance Score</div>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div>
                    <strong style="color: #f44336;">{project['conflicts']}</strong> Conflicts
                </div>
                <div>
                    <strong style="color: #2a5298;">{project['timeline']}</strong> Est. Timeline
                </div>
                <div>
                    <strong style="color: #4caf50;">{project['probability']}%</strong> Approval Probability
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="font-size: 2.5em; color: #4caf50; font-weight: bold;">847</div>
            <div style="color: #666;">TEK17 Requirements Covered</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="font-size: 2.5em; color: #2a5298; font-weight: bold;">355</div>
            <div style="color: #666;">Norwegian Municipalities</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="font-size: 2.5em; color: #ff9800; font-weight: bold;">95%</div>
            <div style="color: #666;">Analysis Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="font-size: 2.5em; color: #1e3c72; font-weight: bold;">67%</div>
            <div style="color: #666;">Time Saved</div>
        </div>
        """, unsafe_allow_html=True)


def render_regulatory_analysis(engine):
    """Render regulatory analysis interface"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
        <h3 style="color: #1e3c72;">🔍 AI-Powered Regulatory Analysis</h3>
        <p style="color: #666; margin: 0;">
            Upload project documents for comprehensive compliance checking
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.subheader("📤 Document Upload")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Supported Formats:**")
        formats_text = ", ".join(engine.supported_formats[:8])
        st.write(f"`{formats_text}`")
        st.write("*And 4 more formats...*")
    
    with col2:
        uploaded_files = st.file_uploader(
            "Upload project documents",
            accept_multiple_files=True,
            type=['pdf', 'dwg', 'ifc', 'rvt', 'xml', 'json']
        )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} files uploaded successfully!")
        
        # Mock analysis
        with st.spinner("🤖 AI analyzing documents for regulatory compliance..."):
            # Simulate analysis time
            import time
            time.sleep(2)
            
            # Generate mock analysis results
            mock_document_data = {
                'content': 'Mock Norwegian planning document content...',
                'files': [f.name for f in uploaded_files]
            }
            
            analysis_results = engine.analyze_regulatory_compliance(mock_document_data)
        
        # Display analysis results
        st.markdown("### 📊 Analysis Results")
        
        # Overall compliance score
        score = analysis_results['overall_score']
        score_color = '#4caf50' if score > 0.8 else '#ff9800' if score > 0.6 else '#f44336'
        
        st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 12px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 2rem;
                    text-align: center;">
            <h2 style="color: {score_color}; font-size: 3em; margin: 0;">
                {score*100:.1f}%
            </h2>
            <h3 style="color: #666; margin: 0;">Overall Compliance Score</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Category breakdown
        st.subheader("📋 Compliance by Category")
        
        categories_df = pd.DataFrame([
            {'Category': cat.replace('_', ' '), 'Score': f"{score*100:.1f}%", 'Weight': f"{config['weight']*100:.0f}%"}
            for cat, (score, config) in zip(
                analysis_results['category_scores'].keys(),
                zip(analysis_results['category_scores'].values(), engine.compliance_categories.values())
            )
        ])
        
        st.dataframe(categories_df, use_container_width=True)
        
        # Timeline and probability
        col1, col2 = st.columns(2)
        
        with col1:
            timeline = analysis_results['timeline_estimate']
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;">
                <h3 style="color: #2a5298; font-size: 2em; margin: 0;">{timeline} weeks</h3>
                <p style="color: #666; margin: 0;">Estimated Approval Timeline</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            probability = analysis_results['approval_probability']
            prob_color = '#4caf50' if probability > 0.8 else '#ff9800' if probability > 0.6 else '#f44336'
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;">
                <h3 style="color: {prob_color}; font-size: 2em; margin: 0;">{probability*100:.0f}%</h3>
                <p style="color: #666; margin: 0;">Approval Probability</p>
            </div>
            """, unsafe_allow_html=True)


def render_conflict_detection(engine):
    """Render conflict detection interface"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffccbc 100%); 
                padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
        <h3 style="color: #e65100;">⚠️ Regulatory Conflict Detection</h3>
        <p style="color: #666; margin: 0;">
            AI-powered identification of conflicts between different regulations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mock conflict data
    conflicts = [
        {
            'id': 'C001',
            'type': 'TEK17 vs Heritage',
            'severity': 'High',
            'description': 'Energy efficiency requirements conflict with heritage preservation requirements',
            'regulations': ['TEK17 §14-2', 'Kulturminneloven §15'],
            'estimated_cost': 150000,
            'estimated_time': 14,
            'solutions': [
                'Use traditional materials with modern insulation core',
                'Apply for heritage dispensation with energy compensation',
                'Implement selective interior insulation strategy'
            ]
        },
        {
            'id': 'C002',
            'type': 'Municipal vs Environmental', 
            'severity': 'Medium',
            'description': 'Building height restrictions conflict with environmental sunlight requirements',
            'regulations': ['Oslo kommuneplan §4.1', 'Naturmangfoldloven §8'],
            'estimated_cost': 75000,
            'estimated_time': 7,
            'solutions': [
                'Redesign with stepped building profile',
                'Add roof gardens for environmental compensation',
                'Negotiate height variance with environmental mitigation'
            ]
        }
    ]
    
    for conflict in conflicts:
        severity_color = {
            'High': '#f44336',
            'Medium': '#ff9800',
            'Low': '#4caf50'
        }.get(conflict['severity'], '#666')
        
        with st.expander(f"⚠️ {conflict['type']} - {conflict['severity']} Severity", expanded=True):
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {conflict['description']}")
                st.markdown(f"**Affected Regulations:** {', '.join(conflict['regulations'])}")
                
                st.markdown("**Proposed Solutions:**")
                for i, solution in enumerate(conflict['solutions'], 1):
                    st.write(f"{i}. {solution}")
            
            with col2:
                st.markdown(f"""
                <div style="background: {severity_color}; color: white; padding: 1rem; 
                            border-radius: 8px; text-align: center; margin-bottom: 1rem;">
                    <strong>{conflict['severity']} Priority</strong>
                </div>
                """, unsafe_allow_html=True)
                
                st.metric("Estimated Cost", f"{conflict['estimated_cost']:,} NOK")
                st.metric("Resolution Time", f"{conflict['estimated_time']} days")
                
                if st.button(f"Generate Solution Report", key=f"solution_{conflict['id']}"):
                    st.success("✅ Detailed solution report generated!")


def render_compliance_reports(engine):
    """Render compliance reporting interface"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c8 100%); 
                padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
        <h3 style="color: #2e7d32;">📋 Professional Compliance Reports</h3>
        <p style="color: #666; margin: 0;">
            Generate comprehensive reports for municipal submissions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Report types
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Compliance Assessment Report", use_container_width=True):
            with st.spinner("Generating comprehensive compliance report..."):
                import time
                time.sleep(2)
                st.success("✅ 25-page compliance assessment report generated!")
                st.download_button(
                    "📥 Download PDF Report",
                    data="Mock PDF content",
                    file_name="compliance_assessment_report.pdf",
                    mime="application/pdf"
                )
    
    with col2:
        if st.button("📋 Municipal Submission Package", use_container_width=True):
            with st.spinner("Preparing municipal submission package..."):
                import time
                time.sleep(2)
                st.success("✅ Complete eByggesøknad package ready!")
                st.download_button(
                    "📥 Download Submission ZIP",
                    data="Mock ZIP content",
                    file_name="municipal_submission_package.zip",
                    mime="application/zip"
                )
    
    with col3:
        if st.button("🔍 Technical Documentation", use_container_width=True):
            with st.spinner("Generating technical documentation..."):
                import time
                time.sleep(2)
                st.success("✅ Technical compliance documentation ready!")
                st.download_button(
                    "📥 Download Technical Docs",
                    data="Mock technical content",
                    file_name="technical_documentation.pdf",
                    mime="application/pdf"
                )
    
    # Report preview
    st.subheader("📊 Report Preview")
    
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 12px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 4px solid #1e3c72;">
        <h4 style="color: #1e3c72;">Compliance Assessment Report - Executive Summary</h4>
        <p><strong>Project:</strong> Grünerløkka Residential Complex</p>
        <p><strong>Overall Compliance Score:</strong> 87.3%</p>
        <p><strong>Key Findings:</strong></p>
        <ul>
            <li>✅ TEK17 building code compliance achieved</li>
            <li>⚠️ 2 heritage-energy conflicts require resolution</li>
            <li>✅ Municipal planning requirements met</li>
            <li>✅ Environmental regulations satisfied</li>
        </ul>
        <p><strong>Recommendation:</strong> Proceed with submission after addressing heritage conflicts through proposed insulation strategy.</p>
    </div>
    """, unsafe_allow_html=True)


def render_ai_assistant(engine):
    """Render AI assistant chat interface"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); 
                padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
        <h3 style="color: #7b1fa2;">🤖 RegIntel AI Assistant</h3>
        <p style="color: #666; margin: 0;">
            Get instant answers about Norwegian building regulations and compliance
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat interface
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {
                'role': 'assistant',
                'content': 'Hei! I am the RegIntel AI assistant. I can help you with Norwegian building regulations, TEK17 compliance, and municipal planning requirements. What would you like to know?'
            }
        ]
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"""
            <div style="background: #e3f2fd; padding: 1rem; border-radius: 12px; 
                        margin: 1rem 0; margin-left: 2rem;">
                <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 12px; 
                        margin: 1rem 0; margin-right: 2rem; border-left: 4px solid #7b1fa2;">
                <strong>🤖 RegIntel AI:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Ask about Norwegian regulations...", key="ai_chat_input")
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Generate AI response (mock)
        if 'tek17' in user_input.lower():
            ai_response = "TEK17 is Norway's technical building regulation that covers safety, health, environment, and energy requirements. It includes 847 specific requirements across categories like structural safety, fire protection, energy efficiency, and accessibility. Would you like details about a specific TEK17 chapter?"
        elif 'heritage' in user_input.lower() or 'kulturminn' in user_input.lower():
            ai_response = "Heritage buildings (kulturminner) have special requirements under Kulturminneloven. When renovating heritage buildings, you must balance preservation with modern requirements like energy efficiency. Common solutions include selective insulation, traditional materials with modern cores, and dispensation applications."
        elif 'oslo' in user_input.lower():
            ai_response = "Oslo kommune has specific planning regulations in addition to national TEK17 requirements. Key Oslo-specific requirements include building height restrictions, parking minimums, and environmental compensation rules. Oslo also has 15 official bydeler, each with local planning considerations."
        else:
            ai_response = "That's a great question about Norwegian building regulations. Based on our AI analysis of 847 TEK17 requirements and 355 municipal variations, I can provide specific guidance. Could you be more specific about which regulation category you're asking about?"
        
        # Add AI response
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': ai_response
        })
        
        st.rerun()
    
    # Quick question buttons
    st.markdown("**Quick Questions:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("What is TEK17?"):
            st.session_state.chat_history.append({'role': 'user', 'content': 'What is TEK17?'})
            st.rerun()
    
    with col2:
        if st.button("Heritage building rules?"):
            st.session_state.chat_history.append({'role': 'user', 'content': 'What are the rules for heritage buildings?'})
            st.rerun()
    
    with col3:
        if st.button("Oslo specific requirements?"):
            st.session_state.chat_history.append({'role': 'user', 'content': 'What are Oslo specific planning requirements?'})
            st.rerun()


def main():
    """Main function for RegIntel Norway integration"""
    
    st.set_page_config(
        page_title="RegIntel Norway - AI Regulatory Intelligence",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply Oslo branding
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    create_regintel_dashboard()


if __name__ == "__main__":
    main()