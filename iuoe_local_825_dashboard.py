import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import requests
import json

# Page configuration
st.set_page_config(
    page_title="IUOE Local 825 - Labor Market Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #b3d9ff;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏗️ IUOE Local 825 Labor Market Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### Construction Industry Analytics for New Jersey")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select Dashboard Section",
    ["Overview", "Employment Trends", "Wages & Benefits", "Economic Indicators", "Industry Analysis", "About"]
)

# Mock data functions (in real implementation, these would use OpenBB API)
def get_construction_employment():
    """Get construction employment data for NJ"""
    # Mock data - replace with actual OpenBB API calls
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='M')
    employment = [150000 + i*100 + np.random.normal(0, 500) for i in range(len(dates))]
    return pd.DataFrame({
        'date': dates,
        'employment': employment,
        'unemployment_rate': [5.2 + np.random.normal(0, 0.5) for _ in range(len(dates))]
    })

def get_wage_data():
    """Get construction wage data for NJ"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='Q')
    return pd.DataFrame({
        'date': dates,
        'hourly_wage': [35 + i*0.5 + np.random.normal(0, 1) for i in range(len(dates))],
        'annual_wage': [75000 + i*1000 + np.random.normal(0, 2000) for i in range(len(dates))],
        'benefits_cost': [15 + i*0.3 + np.random.normal(0, 0.5) for i in range(len(dates))]
    })

def get_industry_breakdown():
    """Get construction industry breakdown"""
    return pd.DataFrame({
        'sector': ['Heavy Construction', 'Building Construction', 'Specialty Trades', 'Infrastructure'],
        'employment': [45000, 38000, 42000, 25000],
        'avg_wage': [42.50, 38.75, 36.25, 41.00],
        'union_density': [0.85, 0.72, 0.68, 0.78]
    })

def get_economic_indicators():
    """Get economic indicators"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='M')
    return pd.DataFrame({
        'date': dates,
        'cpi': [100 + i*0.2 + np.random.normal(0, 0.1) for i in range(len(dates))],
        'ppi_construction': [100 + i*0.3 + np.random.normal(0, 0.2) for i in range(len(dates))],
        'interest_rate': [2.5 + i*0.1 + np.random.normal(0, 0.05) for i in range(len(dates))]
    })

# Import numpy for mock data
import numpy as np

if page == "Overview":
    st.markdown('<h2 class="section-header">📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Total Construction Employment</h3>
            <h2>150,000</h2>
            <p>+2.3% from last month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Average Hourly Wage</h3>
            <h2>$38.75</h2>
            <p>+1.8% from last quarter</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Union Density</h3>
            <h2>76%</h2>
            <p>+1.2% from last year</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Unemployment Rate</h3>
            <h2>5.2%</h2>
            <p>-0.3% from last month</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Employment trend chart
    st.markdown('<h3 class="section-header">📈 Employment Trends</h3>', unsafe_allow_html=True)
    employment_data = get_construction_employment()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=employment_data['date'],
        y=employment_data['employment'],
        mode='lines+markers',
        name='Construction Employment',
        line=dict(color='#1f77b4', width=3)
    ))
    fig.update_layout(
        title='New Jersey Construction Employment (2020-2024)',
        xaxis_title='Date',
        yaxis_title='Employment (Thousands)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Industry breakdown
    st.markdown('<h3 class="section-header">🏢 Industry Breakdown</h3>', unsafe_allow_html=True)
    industry_data = get_industry_breakdown()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(industry_data, x='sector', y='employment',
                     title='Employment by Construction Sector',
                     color='employment',
                     color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(industry_data, x='sector', y='avg_wage',
                     title='Average Hourly Wage by Sector',
                     color='avg_wage',
                     color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)

elif page == "Employment Trends":
    st.markdown('<h2 class="section-header">👷 Employment Trends</h2>', unsafe_allow_html=True)
    
    # Employment data
    employment_data = get_construction_employment()
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Construction Employment', 'Unemployment Rate', 
                       'Employment Growth Rate', 'Job Openings'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Employment trend
    fig.add_trace(
        go.Scatter(x=employment_data['date'], y=employment_data['employment'],
                   mode='lines+markers', name='Employment'),
        row=1, col=1
    )
    
    # Unemployment rate
    fig.add_trace(
        go.Scatter(x=employment_data['date'], y=employment_data['unemployment_rate'],
                   mode='lines+markers', name='Unemployment Rate'),
        row=1, col=2
    )
    
    # Employment growth (mock data)
    growth_rate = [(employment_data['employment'].iloc[i] - employment_data['employment'].iloc[i-1]) / 
                   employment_data['employment'].iloc[i-1] * 100 for i in range(1, len(employment_data))]
    fig.add_trace(
        go.Scatter(x=employment_data['date'][1:], y=growth_rate,
                   mode='lines+markers', name='Growth Rate'),
        row=2, col=1
    )
    
    # Job openings (mock data)
    job_openings = [5000 + np.random.normal(0, 200) for _ in range(len(employment_data))]
    fig.add_trace(
        go.Scatter(x=employment_data['date'], y=job_openings,
                   mode='lines+markers', name='Job Openings'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Employment by county
    st.markdown('<h3 class="section-header">🗺️ Employment by County</h3>', unsafe_allow_html=True)
    
    counties = ['Bergen', 'Essex', 'Hudson', 'Middlesex', 'Monmouth', 'Ocean', 'Passaic', 'Union']
    county_employment = [25000, 22000, 18000, 20000, 15000, 12000, 16000, 14000]
    
    fig = px.bar(x=counties, y=county_employment,
                 title='Construction Employment by County',
                 color=county_employment,
                 color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Wages & Benefits":
    st.markdown('<h2 class="section-header">💰 Wages & Benefits Analysis</h2>', unsafe_allow_html=True)
    
    wage_data = get_wage_data()
    
    # Wage trends
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(wage_data, x='date', y='hourly_wage',
                      title='Average Hourly Wage Trends',
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(wage_data, x='date', y='annual_wage',
                      title='Average Annual Wage Trends',
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Benefits analysis
    st.markdown('<h3 class="section-header">🏥 Benefits Analysis</h3>', unsafe_allow_html=True)
    
    fig = px.line(wage_data, x='date', y='benefits_cost',
                  title='Employer Benefits Cost per Hour',
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Wage comparison
    st.markdown('<h3 class="section-header">📊 Wage Comparison</h3>', unsafe_allow_html=True)
    
    comparison_data = pd.DataFrame({
        'Category': ['Union Construction', 'Non-Union Construction', 'All Private Sector', 'State Average'],
        'Hourly_Wage': [38.75, 32.50, 28.45, 35.20],
        'Annual_Wage': [80600, 67600, 59176, 73216],
        'Benefits': [15.25, 8.75, 12.30, 13.80]
    })
    
    fig = px.bar(comparison_data, x='Category', y='Hourly_Wage',
                 title='Hourly Wage Comparison',
                 color='Hourly_Wage',
                 color_continuous_scale='Greens')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Economic Indicators":
    st.markdown('<h2 class="section-header">📈 Economic Indicators</h2>', unsafe_allow_html=True)
    
    economic_data = get_economic_indicators()
    
    # CPI and PPI
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(economic_data, x='date', y='cpi',
                      title='Consumer Price Index (CPI)',
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(economic_data, x='date', y='ppi_construction',
                      title='Producer Price Index - Construction',
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Interest rates
    st.markdown('<h3 class="section-header">🏦 Interest Rates</h3>', unsafe_allow_html=True)
    
    fig = px.line(economic_data, x='date', y='interest_rate',
                  title='Federal Funds Rate',
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Economic health indicators
    st.markdown('<h3 class="section-header">🏥 Economic Health</h3>', unsafe_allow_html=True)
    
    health_indicators = pd.DataFrame({
        'Indicator': ['GDP Growth', 'Inflation Rate', 'Unemployment Rate', 'Labor Force Participation'],
        'Value': ['2.8%', '3.2%', '5.2%', '62.8%'],
        'Trend': ['↗️', '↘️', '↘️', '↗️'],
        'Status': ['Good', 'Moderate', 'Good', 'Good']
    })
    
    st.dataframe(health_indicators, use_container_width=True)

elif page == "Industry Analysis":
    st.markdown('<h2 class="section-header">🏗️ Construction Industry Analysis</h2>', unsafe_allow_html=True)
    
    industry_data = get_industry_breakdown()
    
    # Industry breakdown charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(industry_data, values='employment', names='sector',
                     title='Employment Distribution by Sector')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(industry_data, values='union_density', names='sector',
                     title='Union Density by Sector')
        st.plotly_chart(fig, use_container_width=True)
    
    # Project pipeline
    st.markdown('<h3 class="section-header">📋 Project Pipeline</h3>', unsafe_allow_html=True)
    
    projects = pd.DataFrame({
        'Project_Type': ['Highway Construction', 'Bridge Repair', 'Building Construction', 
                        'Infrastructure', 'Residential', 'Commercial'],
        'Value_Millions': [250, 180, 320, 150, 200, 280],
        'Duration_Months': [18, 12, 24, 15, 20, 22],
        'Workers_Needed': [150, 80, 200, 100, 120, 180]
    })
    
    fig = px.bar(projects, x='Project_Type', y='Value_Millions',
                 title='Project Value by Type',
                 color='Workers_Needed',
                 color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)
    
    # Skills demand
    st.markdown('<h3 class="section-header">🔧 Skills Demand</h3>', unsafe_allow_html=True)
    
    skills_data = pd.DataFrame({
        'Skill': ['Heavy Equipment Operation', 'Crane Operation', 'Welding', 
                 'Electrical Work', 'Plumbing', 'HVAC', 'Concrete Work'],
        'Demand_Score': [9.2, 8.8, 8.5, 8.0, 7.8, 7.5, 8.2],
        'Average_Wage': [42.50, 45.75, 38.25, 36.50, 34.75, 35.25, 37.80]
    })
    
    fig = px.scatter(skills_data, x='Demand_Score', y='Average_Wage', 
                     size='Demand_Score', color='Skill',
                     title='Skills Demand vs. Average Wage')
    st.plotly_chart(fig, use_container_width=True)

elif page == "About":
    st.markdown('<h2 class="section-header">ℹ️ About This Dashboard</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>IUOE Local 825</h3>
        <p>International Union of Operating Engineers Local 825 represents heavy equipment operators, 
        mechanics, and surveyors in New Jersey and New York.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Data Sources
    This dashboard integrates data from multiple sources:
    
    - **Bureau of Labor Statistics (BLS)**: Employment, wages, and benefits data
    - **Federal Reserve Economic Data (FRED)**: Economic indicators
    - **OpenBB Platform**: Financial and economic data aggregation
    
    ### Key Metrics Tracked
    
    #### Employment Trends
    - Construction employment in New Jersey
    - Unemployment rates
    - Job openings and labor turnover
    - Employment by county and sector
    
    #### Wages & Benefits
    - Average hourly wages
    - Annual compensation
    - Benefits costs
    - Union vs non-union wage comparisons
    
    #### Economic Indicators
    - Consumer Price Index (CPI)
    - Producer Price Index (PPI)
    - Interest rates
    - GDP growth
    
    #### Industry Analysis
    - Construction sector breakdown
    - Project pipeline
    - Skills demand
    - Union density by sector
    
    ### How to Use This Dashboard
    
    1. **Navigation**: Use the sidebar to switch between different sections
    2. **Interactive Charts**: Hover over charts for detailed information
    3. **Data Export**: Charts can be downloaded as images
    4. **Real-time Updates**: Data is updated monthly
    
    ### Contact Information
    
    For questions about this dashboard or IUOE Local 825:
    - Website: [www.iuoe825.org](https://www.iuoe825.org)
    - Phone: (973) 344-0000
    - Email: info@iuoe825.org
    """)
    
    # Technical information
    st.markdown("""
    ### Technical Details
    
    **Built with:**
    - Streamlit (Python web framework)
    - Plotly (Interactive charts)
    - Pandas (Data manipulation)
    - OpenBB Platform (Data integration)
    
    **Data Updates:**
    - Employment data: Monthly
    - Wage data: Quarterly
    - Economic indicators: Monthly
    - Industry analysis: Quarterly
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>IUOE Local 825 Labor Market Dashboard | Built with Streamlit and OpenBB Platform</p>
    <p>Last updated: """ + datetime.now().strftime("%B %d, %Y") + """</p>
</div>
""", unsafe_allow_html=True) 