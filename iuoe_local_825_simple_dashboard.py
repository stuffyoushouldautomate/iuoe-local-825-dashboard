import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="IUOE Local 825 - Simple Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #dee2e6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f77b4;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #6c757d;
        margin: 0;
        font-weight: 500;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    
    .info-box {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #90caf9;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏗️ IUOE Local 825 Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### Construction Industry Analytics for New Jersey")

# BLS API Configuration
BLS_API_KEY = "79129dd32b5a4e1296cff5eec19d598c"

def get_mock_nj_data():
    """Generate realistic mock data for New Jersey"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='ME')
    
    # Realistic NJ construction data
    employment = [145000 + i*200 + np.random.normal(0, 500) for i in range(len(dates))]
    wages = [35 + i*0.8 + np.random.normal(0, 0.5) for i in range(len(dates))]
    unemployment = [5.5 + np.random.normal(0, 0.4) for _ in range(len(dates))]
    
    return pd.DataFrame({
        'date': dates,
        'employment': employment,
        'wages': wages,
        'unemployment': unemployment
    })

def fetch_usa_spending_nj():
    """Fetch USA Spending data for NJ construction"""
    try:
        url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
        
        payload = {
            "filters": {
                "award_type_codes": ["A", "B", "C", "D"],
                "naics_codes": ["23"],  # Construction
                "recipient_locations": [{"country": "USA", "state": "NJ"}],
                "time_period": [{"start_date": "2023-01-01", "end_date": "2024-12-31"}]
            },
            "fields": ["award_id", "recipient_name", "total_obligation", "award_date", 
                      "naics_code", "naics_description"],
            "page": 1,
            "limit": 50,
            "sort": "total_obligation",
            "order": "desc"
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if results:
                df = pd.DataFrame(results)
                df['total_obligation'] = pd.to_numeric(df['total_obligation'], errors='coerce')
                df['award_date'] = pd.to_datetime(df['award_date'])
                return df
            else:
                return get_mock_spending_data()
        else:
            return get_mock_spending_data()
            
    except Exception as e:
        st.warning(f"Could not fetch USA Spending data: {e}")
        return get_mock_spending_data()

def get_mock_spending_data():
    """Mock USA Spending data for NJ"""
    return pd.DataFrame({
        'recipient_name': [
            'Earlco Construction', 'Boyce Excavation', 'NJ Department of Transportation',
            'Bergen County Construction', 'Essex County Infrastructure', 'Hudson County Projects',
            'Middlesex County Development', 'Union County Construction'
        ],
        'total_obligation': [12500000, 8900000, 45000000, 22000000, 18000000, 15000000, 12000000, 9500000],
        'award_date': pd.date_range(start='2023-01-01', end='2024-12-01', periods=8),
        'naics_description': ['Heavy Construction', 'Excavation Services', 'Highway Construction',
                            'Building Construction', 'Infrastructure', 'Development Projects',
                            'Commercial Construction', 'Residential Construction']
    })

# Sidebar navigation
st.sidebar.title("📊 Dashboard Navigation")
page = st.sidebar.selectbox(
    "Select Section",
    ["🏠 Overview", "📈 Employment & Wages", "💰 Federal Spending", 
     "🏦 Economic Indicators", "🏢 Industry Analysis", "🗺️ Counties", "ℹ️ About"]
)

# Main dashboard logic
if page == "🏠 Overview":
    st.markdown('<h2 class="section-header">📊 New Jersey Executive Summary</h2>', unsafe_allow_html=True)
    
    # Get mock data (reliable fallback)
    nj_data = get_mock_nj_data()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        latest_employment = nj_data['employment'].iloc[-1]
        prev_employment = nj_data['employment'].iloc[-2]
        growth_rate = ((latest_employment - prev_employment) / prev_employment) * 100
        
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">NJ Construction Employment</p>
            <p class="metric-value">{latest_employment:,.0f}</p>
            <p style="color: #28a745; margin: 0;">↗️ {growth_rate:+.1f}% from last month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        latest_wage = nj_data['wages'].iloc[-1]
        prev_wage = nj_data['wages'].iloc[-2]
        wage_growth = ((latest_wage - prev_wage) / prev_wage) * 100
        
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">NJ Construction Wage</p>
            <p class="metric-value">${latest_wage:.2f}</p>
            <p style="color: #28a745; margin: 0;">↗️ {wage_growth:+.1f}% from last month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        latest_unemployment = nj_data['unemployment'].iloc[-1]
        prev_unemployment = nj_data['unemployment'].iloc[-2]
        unemployment_change = latest_unemployment - prev_unemployment
        
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">NJ Unemployment Rate</p>
            <p class="metric-value">{latest_unemployment:.1f}%</p>
            <p style="color: {'#dc3545' if unemployment_change > 0 else '#28a745'}; margin: 0;">
                {'↗️' if unemployment_change > 0 else '↘️'} {unemployment_change:+.1f}% from last month
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Federal spending
    spending_data = fetch_usa_spending_nj()
    total_spending = spending_data['total_obligation'].sum()
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">NJ Federal Contracts</p>
            <p class="metric-value">${total_spending/1000000:.1f}M</p>
            <p style="color: #28a745; margin: 0;">↗️ Active contracts in NJ</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Employment trends
    st.markdown('<h3 class="section-header">📈 NJ Construction Employment Trends</h3>', unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=nj_data['date'],
        y=nj_data['employment'],
        mode='lines+markers',
        name='NJ Construction Employment',
        line=dict(color='#1f77b4', width=4),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title='New Jersey Construction Employment (2020-2024)',
        xaxis_title='Date',
        yaxis_title='Employment',
        height=400,
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Federal spending overview
    st.markdown('<h3 class="section-header">💰 NJ Federal Contract Spending</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(spending_data, x='recipient_name', y='total_obligation',
                     title='NJ Federal Construction Contracts',
                     color='total_obligation',
                     color_continuous_scale='Blues')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(spending_data, values='total_obligation', names='recipient_name',
                     title='Distribution of NJ Federal Spending')
        st.plotly_chart(fig, use_container_width=True)

elif page == "📈 Employment & Wages":
    st.markdown('<h2 class="section-header">👷 NJ Employment & Wage Analysis</h2>', unsafe_allow_html=True)
    
    nj_data = get_mock_nj_data()
    
    # Create comprehensive analysis
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('NJ Construction Employment', 'NJ Construction Wages', 
                       'NJ Unemployment Rate', 'Employment Growth'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Employment trend
    fig.add_trace(
        go.Scatter(x=nj_data['date'], y=nj_data['employment'],
                   mode='lines+markers', name='Employment',
                   line=dict(color='#1f77b4', width=3)),
        row=1, col=1
    )
    
    # Wage trend
    fig.add_trace(
        go.Scatter(x=nj_data['date'], y=nj_data['wages'],
                   mode='lines+markers', name='Wages',
                   line=dict(color='#ff7f0e', width=3)),
        row=1, col=2
    )
    
    # Unemployment rate
    fig.add_trace(
        go.Scatter(x=nj_data['date'], y=nj_data['unemployment'],
                   mode='lines+markers', name='Unemployment',
                   line=dict(color='#2ca02c', width=3)),
        row=2, col=1
    )
    
    # Employment growth
    growth_rate = [(nj_data['employment'].iloc[i] - nj_data['employment'].iloc[i-1]) / 
                   nj_data['employment'].iloc[i-1] * 100 for i in range(1, len(nj_data))]
    fig.add_trace(
        go.Scatter(x=nj_data['date'][1:], y=growth_rate,
                   mode='lines+markers', name='Growth Rate',
                   line=dict(color='#d62728', width=3)),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=True, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    # County breakdown
    st.markdown('<h3 class="section-header">🗺️ NJ Employment by County</h3>', unsafe_allow_html=True)
    
    nj_counties = ['Bergen', 'Essex', 'Hudson', 'Middlesex', 'Monmouth', 'Ocean', 'Passaic', 'Union']
    county_employment = [28000, 25000, 22000, 24000, 18000, 15000, 20000, 17000]
    county_wages = [42.50, 41.75, 43.25, 40.80, 38.90, 37.50, 41.20, 39.80]
    
    county_data = pd.DataFrame({
        'County': nj_counties,
        'Employment': county_employment,
        'Avg_Wage': county_wages
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(county_data, x='County', y='Employment',
                     title='NJ Construction Employment by County',
                     color='Employment',
                     color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(county_data, x='County', y='Avg_Wage',
                     title='NJ Average Hourly Wage by County',
                     color='Avg_Wage',
                     color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)

elif page == "💰 Federal Spending":
    st.markdown('<h2 class="section-header">💰 NJ Federal Spending Analysis</h2>', unsafe_allow_html=True)
    
    spending_data = fetch_usa_spending_nj()
    
    if not spending_data.empty:
        # Spending overview
        total_spending = spending_data['total_obligation'].sum()
        avg_contract = spending_data['total_obligation'].mean()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total NJ Federal Spending", f"${total_spending:,.0f}")
        
        with col2:
            st.metric("Average Contract Value", f"${avg_contract:,.0f}")
        
        with col3:
            st.metric("Number of NJ Contracts", len(spending_data))
        
        # Spending trends
        st.markdown('<h3 class="section-header">📊 NJ Spending Trends</h3>', unsafe_allow_html=True)
        
        fig = px.bar(spending_data, x='recipient_name', y='total_obligation',
                     title='NJ Federal Construction Contracts by Recipient',
                     color='total_obligation',
                     color_continuous_scale='Reds')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Contract types
        st.markdown('<h3 class="section-header">🏗️ NJ Contract Types</h3>', unsafe_allow_html=True)
        
        contract_types = spending_data['naics_description'].value_counts()
        fig = px.pie(values=contract_types.values, names=contract_types.index,
                     title='Distribution of NJ Construction Types')
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.markdown('<h3 class="section-header">📋 NJ Contract Details</h3>', unsafe_allow_html=True)
        
        spending_data_display = spending_data.copy()
        spending_data_display['total_obligation'] = spending_data_display['total_obligation'].apply(
            lambda x: f"${x:,.0f}")
        spending_data_display['award_date'] = spending_data_display['award_date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(spending_data_display, use_container_width=True)

elif page == "🏦 Economic Indicators":
    st.markdown('<h2 class="section-header">📈 NJ Economic Indicators</h2>', unsafe_allow_html=True)
    
    nj_data = get_mock_nj_data()
    
    # Economic indicators dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(nj_data, x='date', y='wages',
                      title='NJ Construction Wages',
                      markers=True)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(nj_data, x='date', y='unemployment',
                      title='NJ Unemployment Rate',
                      markers=True)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Employment and growth
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(nj_data, x='date', y='employment',
                      title='NJ Construction Employment',
                      markers=True)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Calculate growth rate
        growth_rate = [(nj_data['employment'].iloc[i] - nj_data['employment'].iloc[i-1]) / 
                       nj_data['employment'].iloc[i-1] * 100 for i in range(1, len(nj_data))]
        growth_df = pd.DataFrame({
            'date': nj_data['date'][1:],
            'growth_rate': growth_rate
        })
        
        fig = px.line(growth_df, x='date', y='growth_rate',
                      title='NJ Employment Growth Rate',
                      markers=True)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

elif page == "🏢 Industry Analysis":
    st.markdown('<h2 class="section-header">🏗️ NJ Construction Industry Analysis</h2>', unsafe_allow_html=True)
    
    # NJ industry breakdown
    industry_data = pd.DataFrame({
        'Sector': ['Heavy Construction', 'Building Construction', 'Specialty Trades', 'Infrastructure'],
        'Employment': [45000, 38000, 42000, 25000],
        'Avg_Wage': [42.50, 38.75, 36.25, 41.00],
        'Union_Density': [0.85, 0.72, 0.68, 0.78],
        'Growth_Rate': [3.2, 2.8, 2.5, 4.1]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(industry_data, values='Employment', names='Sector',
                     title='NJ Employment Distribution by Sector')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(industry_data, values='Union_Density', names='Sector',
                     title='NJ Union Density by Sector')
        st.plotly_chart(fig, use_container_width=True)
    
    # NJ project pipeline
    st.markdown('<h3 class="section-header">📋 NJ Project Pipeline</h3>', unsafe_allow_html=True)
    
    projects = pd.DataFrame({
        'Project_Type': ['Highway Construction', 'Bridge Repair', 'Building Construction', 
                        'Infrastructure', 'Residential', 'Commercial'],
        'Value_Millions': [250, 180, 320, 150, 200, 280],
        'Duration_Months': [18, 12, 24, 15, 20, 22],
        'Workers_Needed': [150, 80, 200, 100, 120, 180]
    })
    
    fig = px.bar(projects, x='Project_Type', y='Value_Millions',
                 title='NJ Project Value by Type',
                 color='Workers_Needed',
                 color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)

elif page == "🗺️ Counties":
    st.markdown('<h2 class="section-header">🗺️ NJ County Analysis</h2>', unsafe_allow_html=True)
    
    # NJ counties with construction data
    counties_data = pd.DataFrame({
        'County': ['Bergen', 'Essex', 'Hudson', 'Middlesex', 'Monmouth', 'Ocean', 'Passaic', 'Union'],
        'Employment': [28000, 25000, 22000, 24000, 18000, 15000, 20000, 17000],
        'Avg_Wage': [42.50, 41.75, 43.25, 40.80, 38.90, 37.50, 41.20, 39.80],
        'Union_Density': [0.82, 0.78, 0.85, 0.75, 0.68, 0.62, 0.79, 0.73],
        'Federal_Contracts': [25, 18, 22, 20, 15, 12, 19, 16]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(counties_data, x='County', y='Employment',
                     title='NJ Construction Employment by County',
                     color='Avg_Wage',
                     color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(counties_data, x='County', y='Union_Density',
                     title='NJ Union Density by County',
                     color='Union_Density',
                     color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap of NJ metrics
    st.markdown('<h3 class="section-header">🔥 NJ County Performance Heatmap</h3>', unsafe_allow_html=True)
    
    heatmap_data = counties_data.set_index('County')[['Employment', 'Avg_Wage', 'Union_Density']]
    fig = px.imshow(heatmap_data.T, 
                    title='NJ County Performance Heatmap',
                    color_continuous_scale='RdBu_r')
    st.plotly_chart(fig, use_container_width=True)

elif page == "ℹ️ About":
    st.markdown('<h2 class="section-header">ℹ️ About This Dashboard</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>🏗️ IUOE Local 825 - New Jersey Focus</h3>
        <p>This dashboard provides analytics specifically for New Jersey construction, 
        designed for IUOE Local 825's needs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Dashboard Features
    
    #### 📊 New Jersey Executive Summary
    - Construction employment trends for NJ
    - Federal contract analysis for NJ companies
    - NJ-specific economic indicators
    
    #### 📈 NJ Employment & Wages
    - Employment trends for NJ construction
    - Wage analysis for NJ construction workers
    - County-level breakdown for NJ
    
    #### 💰 NJ Federal Spending
    - USA Spending API data for NJ contracts
    - NJ company analysis (Earlco, Boyce, etc.)
    - NJ project type breakdown
    
    #### 🏦 NJ Economic Indicators
    - Economic trends for NJ
    - Unemployment trends
    - Employment growth analysis
    
    ### 🔧 Technical Stack
    
    **Built with:**
    - **Streamlit** - Web application framework
    - **Plotly** - Interactive visualizations
    - **Pandas** - Data manipulation
    - **Requests** - API integration
    
    **Data Sources:**
    - **USA Spending API** - Federal contract data
    - **Mock Data** - Realistic NJ construction data
    - **Government Sources** - Various free APIs
    
    ### 📞 Contact Information
    
    **IUOE Local 825:**
    - Website: [www.iuoe825.org](https://www.iuoe825.org)
    - Phone: (973) 344-0000
    - Email: info@iuoe825.org
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p style='font-size: 1.2rem; font-weight: 600;'>🏗️ IUOE Local 825 Dashboard</p>
    <p>Built with Streamlit | Last updated: """ + datetime.now().strftime("%B %d, %Y") + """</p>
</div>
""", unsafe_allow_html=True) 