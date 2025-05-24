def render_executive_dashboard():
    """Render premium executive dashboard"""
    
    st.markdown("## 📊 Executive Planning Intelligence Dashboard")
    st.markdown("*Real-time insights into Oslo's comprehensive planning landscape*")
    
    all_docs = st.session_state.oslo_premium.get_all_documents()
    categories = st.session_state.oslo_premium.get_categories()
    
    # Enhanced KPI Cards and Category Overview
    if ENHANCEMENTS_AVAILABLE:
        create_enhanced_kpi_cards(all_docs)
        st.markdown("<br>", unsafe_allow_html=True)
        create_premium_category_overview(all_docs, categories)
    else:
        # Fallback simple metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Documents", len(all_docs))
        with col2:
            vedtatt_count = len(all_docs[all_docs['status'] == 'Vedtatt'])
            completion_rate = round((vedtatt_count / len(all_docs)) * 100)
            st.metric("Completion Rate", f"{completion_rate}%")
        with col3:
            priority_docs = len(all_docs[all_docs['priority'] >= 3])
            st.metric("High Priority", priority_docs)
        with col4:
            under_development = len(all_docs[all_docs['status'] == 'Under behandling'])
            st.metric("In Development", under_development)
    
    # Professional footer
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
        color: white;
        padding: 2rem 1rem;
        margin-top: 3rem;
        border-radius: 15px;
        text-align: center;
    ">
        <h4>🏛️ Oslo Planning Documents - Premium</h4>
        <p>Professional Planning Intelligence Platform</p>
        <small>© 2024 Oslo Kommune • All documents remain property of Oslo Kommune</small>
    </div>
    """, unsafe_allow_html=True)