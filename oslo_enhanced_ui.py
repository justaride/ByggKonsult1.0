#!/usr/bin/env python3
"""
Oslo Planning Dashboard - Enhanced UI Components
Professional graphics and styling for finished product look
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def apply_oslo_branding():
    """Apply Oslo kommune branding and professional styling"""
    
    # Oslo kommune color palette
    oslo_colors = {
        'primary': '#1e3c72',      # Oslo blue
        'secondary': '#2a5298',    # Lighter blue
        'accent': '#ff6b35',       # Oslo orange
        'success': '#4caf50',      # Green
        'warning': '#ff9800',      # Orange
        'error': '#f44336',        # Red
        'light_blue': '#e3f2fd',   # Very light blue
        'dark_blue': '#0d47a1',    # Dark blue
        'grey': '#f5f5f5'          # Light grey
    }
    
    # Custom CSS for professional look
    st.markdown(f"""
    <style>
    /* Oslo kommune branding */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    
    /* Header styling */
    .oslo-header {{
        background: linear-gradient(135deg, {oslo_colors['primary']} 0%, {oslo_colors['secondary']} 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(30, 60, 114, 0.3);
    }}
    
    .oslo-logo {{
        font-size: 3.5em;
        margin-bottom: 0.5rem;
        animation: pulse 3s infinite;
    }}
    
    .oslo-title {{
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    .oslo-subtitle {{
        font-size: 1.2em;
        opacity: 0.9;
        font-weight: 300;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
    /* Card styling */
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 4px solid {oslo_colors['primary']};
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }}
    
    .metric-number {{
        font-size: 2.5em;
        font-weight: bold;
        color: {oslo_colors['primary']};
        margin-bottom: 0.5rem;
    }}
    
    .metric-label {{
        color: #666;
        font-size: 1.1em;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }}
    
    .metric-delta {{
        font-size: 0.9em;
        margin-top: 0.5rem;
    }}
    
    .metric-delta.positive {{
        color: {oslo_colors['success']};
    }}
    
    .metric-delta.negative {{
        color: {oslo_colors['error']};
    }}
    
    /* Status badges */
    .status-badge {{
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
        margin: 0.2rem;
    }}
    
    .status-active {{
        background: {oslo_colors['success']};
        color: white;
    }}
    
    .status-pending {{
        background: {oslo_colors['warning']};
        color: white;
    }}
    
    .status-inactive {{
        background: {oslo_colors['error']};
        color: white;
    }}
    
    /* Control panels */
    .control-panel {{
        background: {oslo_colors['light_blue']};
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid {oslo_colors['secondary']};
    }}
    
    /* Info panels */
    .info-panel {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-top: 3px solid {oslo_colors['accent']};
        margin: 1rem 0;
    }}
    
    /* Navigation improvements */
    .nav-button {{
        background: {oslo_colors['primary']};
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 0.2rem;
    }}
    
    .nav-button:hover {{
        background: {oslo_colors['secondary']};
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(30, 60, 114, 0.3);
    }}
    
    /* Footer */
    .oslo-footer {{
        background: {oslo_colors['grey']};
        padding: 2rem;
        border-radius: 12px;
        margin-top: 3rem;
        text-align: center;
        color: #666;
        border-top: 3px solid {oslo_colors['primary']};
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .oslo-title {{
            font-size: 2em;
        }}
        
        .oslo-logo {{
            font-size: 2.5em;
        }}
        
        .metric-card {{
            margin-bottom: 1rem;
        }}
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {oslo_colors['grey']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {oslo_colors['primary']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {oslo_colors['secondary']};
    }}
    </style>
    """, unsafe_allow_html=True)
    
    return oslo_colors

def create_oslo_header():
    """Create professional Oslo kommune header"""
    st.markdown("""
    <div class="oslo-header">
        <div class="oslo-logo">🏛️</div>
        <div class="oslo-title">Oslo Planning Intelligence</div>
        <div class="oslo-subtitle">Comprehensive Municipal Planning Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

def create_enhanced_metric(label, value, delta=None, delta_color="positive"):
    """Create enhanced metric cards with professional styling"""
    delta_html = ""
    if delta:
        delta_html = f'<div class="metric-delta {delta_color}">{delta}</div>'
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_status_badge(status):
    """Create status badges with Oslo styling"""
    status_class = {
        'Under behandling': 'status-pending',
        'Vedtatt': 'status-active', 
        'Høring': 'status-pending',
        'Avslått': 'status-inactive'
    }.get(status, 'status-pending')
    
    return f'<span class="status-badge {status_class}">{status}</span>'

def create_enhanced_map(viz, show_bydeler=True, show_documents=True, selected_bydel="All"):
    """Create enhanced map with professional styling"""
    
    # Create base map
    fig = viz.create_interactive_oslo_map(show_bydeler, show_documents, selected_bydel)
    
    # Enhanced map styling
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=50, b=0),
        height=700,
        title=dict(
            text=f"🗺️ Oslo Planning Map{' - ' + selected_bydel if selected_bydel != 'All' else ''}",
            x=0.5,
            font=dict(size=20, color='#1e3c72', family="Arial Black"),
            pad=dict(t=20)
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#1e3c72",
            borderwidth=1,
            font=dict(size=11),
            x=0.02,
            y=0.98
        )
    )
    
    return fig

def create_enhanced_charts(areas_df, docs_df):
    """Create professional charts with Oslo branding"""
    
    oslo_colors = ['#1e3c72', '#2a5298', '#ff6b35', '#4caf50', '#ff9800', '#f44336']
    
    # Chart 1: Bydeler by plan count
    fig1 = px.bar(
        areas_df.nlargest(10, 'plan_count'),
        x='area_name',
        y='plan_count',
        title="📊 Most Active Oslo Areas",
        color='plan_count',
        color_continuous_scale='Blues'
    )
    
    fig1.update_layout(
        font=dict(family="Arial, sans-serif"),
        title_font=dict(size=18, color='#1e3c72'),
        xaxis_title="Oslo Areas",
        yaxis_title="Number of Plans",
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig1.update_traces(
        marker_line_color='#1e3c72',
        marker_line_width=1
    )
    
    # Chart 2: Status distribution
    if not docs_df.empty:
        status_counts = docs_df['status'].value_counts()
        
        fig2 = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="📈 Planning Document Status",
            color_discrete_sequence=oslo_colors
        )
        
        fig2.update_layout(
            font=dict(family="Arial, sans-serif"),
            title_font=dict(size=18, color='#1e3c72'),
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(
                orientation="v",
                x=1.02,
                y=1
            )
        )
        
        fig2.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12,
            marker=dict(line=dict(color='white', width=2))
        )
    else:
        fig2 = go.Figure()
        fig2.add_annotation(text="No data available", 
                           xref="paper", yref="paper",
                           x=0.5, y=0.5, showarrow=False)
    
    # Chart 3: Population vs Plans scatter
    fig3 = px.scatter(
        areas_df,
        x='population',
        y='plan_count',
        size='area_km2',
        hover_name='area_name',
        title="🏘️ Population vs Planning Activity",
        color='plan_count',
        color_continuous_scale='Viridis'
    )
    
    fig3.update_layout(
        font=dict(family="Arial, sans-serif"),
        title_font=dict(size=18, color='#1e3c72'),
        xaxis_title="Population",
        yaxis_title="Number of Plans",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig1, fig2, fig3

def create_info_panel(title, content, icon="ℹ️"):
    """Create styled information panels"""
    st.markdown(f"""
    <div class="info-panel">
        <h3 style="color: #1e3c72; margin-bottom: 1rem;">{icon} {title}</h3>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

def create_oslo_footer():
    """Create professional footer with Oslo branding"""
    st.markdown("""
    <div class="oslo-footer">
        <div style="margin-bottom: 1rem;">
            <strong>Oslo Planning Intelligence Dashboard</strong>
        </div>
        <div style="font-size: 0.9em;">
            Official planning data for Oslo Kommune • Real-time updates • AI-powered analysis
        </div>
        <div style="margin-top: 1rem; font-size: 0.8em; opacity: 0.7;">
            Built with modern technology for Norwegian municipal planning
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_control_panel(title, content):
    """Create styled control panels"""
    st.markdown(f"""
    <div class="control-panel">
        <h4 style="color: #1e3c72; margin-bottom: 1rem;">{title}</h4>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)