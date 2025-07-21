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
    page_title="IUOE Local 825 - Real Data Only",
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
    
    .error-box {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #dc3545;
        margin: 1rem 0;
        color: #721c24;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #28a745;
        margin: 1rem 0;
        color: #155724;
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
st.markdown('<h1 class="main-header">🏗️ IUOE Local 825 - Real Data Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### Construction Industry Analytics for New Jersey - REAL DATA ONLY")

# ============================================================================
# 🔑 API KEY CONFIGURATION - PUT YOUR KEYS HERE
# ============================================================================

# BLS API Key (you already provided this)
BLS_API_KEY = "79129dd32b5a4e1296cff5eec19d598c"

# FRED API Key (you need to get this from https://fred.stlouisfed.org/docs/api/api_key.html)
FRED_API_KEY = "YOUR_FRED_API_KEY_HERE"  # ← PUT YOUR FRED KEY HERE

# SEC API (no key needed - free)
SEC_API_ENABLED = True

# USA Spending API (no key needed - free)
USA_SPENDING_ENABLED = True

# ============================================================================
# API FUNCTIONS - REAL DATA ONLY
# ============================================================================

def fetch_real_bls_nj_data():
    """Fetch REAL BLS data for New Jersey construction"""
    try:
        # NJ Construction Employment series IDs
        series_ids = [
            "CES2023600001",  # NJ Total Nonfarm Employment
            "CES2023230001",  # NJ Construction Employment
            "CES2023230002",  # NJ Construction Wages
        ]
        
        url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
        
        headers = {
            "BLS-API-KEY": BLS_API_KEY,
            "Content-Type": "application/json"
        }
        
        payload = {
            "seriesid": series_ids,
            "startyear": "2020",
            "endyear": "2024",
            "registrationkey": BLS_API_KEY
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'Results' in data and data['Results']:
                # Process the real BLS data
                processed_data = []
                
                for series in data['Results']['series']:
                    series_id = series['seriesID']
                    series_title = series['seriesTitle']
                    
                    for item in series['data']:
                        year = item['year']
                        period = item['period']
                        value = item['value']
                        
                        # Convert BLS period to date
                        if period == 'M01': month = 1
                        elif period == 'M02': month = 2
                        elif period == 'M03': month = 3
                        elif period == 'M04': month = 4
                        elif period == 'M05': month = 5
                        elif period == 'M06': month = 6
                        elif period == 'M07': month = 7
                        elif period == 'M08': month = 8
                        elif period == 'M09': month = 9
                        elif period == 'M10': month = 10
                        elif period == 'M11': month = 11
                        elif period == 'M12': month = 12
                        else: continue
                        
                        date = pd.Timestamp(year=int(year), month=month, day=1)
                        
                        processed_data.append({
                            'date': date,
                            'series_id': series_id,
                            'series_title': series_title,
                            'value': float(value)
                        })
                
                if processed_data:
                    df = pd.DataFrame(processed_data)
                    return df
                else:
                    return None
            else:
                return None
        else:
            st.error(f"BLS API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Error fetching BLS data: {str(e)}")
        return None

def fetch_real_fred_nj_data():
    """Fetch REAL FRED data for New Jersey"""
    if FRED_API_KEY == "YOUR_FRED_API_KEY_HERE":
        st.error("❌ FRED API Key not configured! Get your free key at: https://fred.stlouisfed.org/docs/api/api_key.html")
        return None
    
    try:
        # NJ Economic indicators from FRED
        series_ids = [
            "NJURN",  # NJ Unemployment Rate
            "NJCONS",  # NJ Construction Employment
            "NJWAGE"   # NJ Average Hourly Earnings
        ]
        
        url = f"https://api.stlouisfed.org/fred/series/observations"
        
        all_data = []
        
        for series_id in series_ids:
            params = {
                "series_id": series_id,
                "api_key": FRED_API_KEY,
                "file_type": "json",
                "observation_start": "2020-01-01",
                "observation_end": "2024-12-31"
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'observations' in data:
                    for obs in data['observations']:
                        if obs['value'] != '.':
                            all_data.append({
                                'date': pd.to_datetime(obs['date']),
                                'series_id': series_id,
                                'value': float(obs['value'])
                            })
        
        if all_data:
            return pd.DataFrame(all_data)
        else:
            return None
            
    except Exception as e:
        st.error(f"Error fetching FRED data: {str(e)}")
        return None

def fetch_real_usa_spending_nj():
    """Fetch REAL USA Spending data for NJ construction"""
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
                st.error("❌ No USA Spending data found for NJ construction contracts")
                return None
        else:
            st.error(f"❌ USA Spending API Error: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"❌ Error fetching USA Spending data: {str(e)}")
        return None

def fetch_real_sec_nj_data():
    """Fetch REAL SEC data for NJ construction companies"""
    try:
        # Search for NJ construction companies
        url = "https://data.sec.gov/submissions/CIK0000000001.json"
        
        # This is a simplified example - SEC API requires more complex setup
        # For now, we'll show what's available
        st.info("ℹ️ SEC API requires additional setup for company filings. Data not available in this demo.")
        return None
        
    except Exception as e:
        st.error(f"❌ Error fetching SEC data: {str(e)}")
        return None

# Sidebar navigation
st.sidebar.title("📊 Dashboard Navigation")
page = st.sidebar.selectbox(
    "Select Section",
    ["🏠 Overview", "📈 Employment & Wages", "💰 Federal Spending", 
     "🏦 Economic Indicators", "🏢 Industry Analysis", "🗺️ Counties", "🔑 API Setup", "ℹ️ About"]
)

# Main dashboard logic
if page == "🏠 Overview":
    st.markdown('<h2 class="section-header">📊 New Jersey Executive Summary</h2>', unsafe_allow_html=True)
    
    # Check API configuration
    st.markdown("### 🔑 API Status Check")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if BLS_API_KEY != "YOUR_BLS_API_KEY_HERE":
            st.success("✅ BLS API Key: Configured")
        else:
            st.error("❌ BLS API Key: Not configured")
    
    with col2:
        if FRED_API_KEY != "YOUR_FRED_API_KEY_HERE":
            st.success("✅ FRED API Key: Configured")
        else:
            st.error("❌ FRED API Key: Not configured")
    
    with col3:
        st.success("✅ USA Spending API: Free (no key needed)")
    
    with col4:
        st.info("ℹ️ SEC API: Requires setup")
    
    # Fetch real data
    st.markdown("### 📊 Real Data Status")
    
    # BLS Data
    st.markdown("**🔍 Fetching REAL BLS data for New Jersey...**")
    bls_data = fetch_real_bls_nj_data()
    
    if bls_data is not None and not bls_data.empty:
        st.success("✅ Successfully fetched REAL BLS data!")
        
        # Display BLS metrics
        construction_data = bls_data[bls_data['series_id'] == 'CES2023230001']
        
        if not construction_data.empty:
            latest_employment = construction_data['value'].iloc[-1]
            prev_employment = construction_data['value'].iloc[-2] if len(construction_data) > 1 else latest_employment
            growth_rate = ((latest_employment - prev_employment) / prev_employment) * 100
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-label">NJ Construction Employment (REAL)</p>
                    <p class="metric-value">{latest_employment:,.0f}</p>
                    <p style="color: #28a745; margin: 0;">↗️ {growth_rate:+.1f}% from last month</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show BLS data chart
            fig = px.line(construction_data, x='date', y='value',
                          title='REAL NJ Construction Employment (BLS Data)',
                          labels={'value': 'Employment', 'date': 'Date'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("❌ No construction employment data found in BLS response")
    else:
        st.error("❌ Could not fetch BLS data. Check your API key and try again.")
    
    # USA Spending Data
    st.markdown("**🔍 Fetching REAL USA Spending data for NJ...**")
    spending_data = fetch_real_usa_spending_nj()
    
    if spending_data is not None and not spending_data.empty:
        st.success("✅ Successfully fetched REAL USA Spending data!")
        
        total_spending = spending_data['total_obligation'].sum()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(spending_data, x='recipient_name', y='total_obligation',
                         title='REAL NJ Federal Construction Contracts',
                         color='total_obligation',
                         color_continuous_scale='Blues')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.pie(spending_data, values='total_obligation', names='recipient_name',
                         title='Distribution of REAL NJ Federal Spending')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ Could not fetch USA Spending data.")

elif page == "📈 Employment & Wages":
    st.markdown('<h2 class="section-header">👷 NJ Employment & Wage Analysis (REAL DATA)</h2>', unsafe_allow_html=True)
    
    # Fetch real BLS data
    bls_data = fetch_real_bls_nj_data()
    
    if bls_data is not None and not bls_data.empty:
        st.success("✅ Using REAL BLS data for analysis")
        
        # Create comprehensive analysis with real data
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('NJ Construction Employment (REAL)', 'NJ Total Employment (REAL)', 
                           'NJ Construction Wages (REAL)', 'Employment Growth (REAL)'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Employment trends
        construction_data = bls_data[bls_data['series_id'] == 'CES2023230001']
        total_data = bls_data[bls_data['series_id'] == 'CES2023600001']
        
        if not construction_data.empty:
            fig.add_trace(
                go.Scatter(x=construction_data['date'], y=construction_data['value'],
                           mode='lines+markers', name='Construction Employment',
                           line=dict(color='#1f77b4', width=3)),
                row=1, col=1
            )
        
        if not total_data.empty:
            fig.add_trace(
                go.Scatter(x=total_data['date'], y=total_data['value'],
                           mode='lines+markers', name='Total Employment',
                           line=dict(color='#ff7f0e', width=3)),
                row=1, col=2
            )
        
        fig.update_layout(height=600, showlegend=True, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
        
        # Show raw data
        st.markdown("### 📋 Raw BLS Data")
        st.dataframe(bls_data, use_container_width=True)
        
    else:
        st.error("❌ No real employment data available. Configure your BLS API key.")

elif page == "💰 Federal Spending":
    st.markdown('<h2 class="section-header">💰 NJ Federal Spending Analysis (REAL DATA)</h2>', unsafe_allow_html=True)
    
    spending_data = fetch_real_usa_spending_nj()
    
    if spending_data is not None and not spending_data.empty:
        st.success("✅ Using REAL USA Spending data")
        
        # Spending overview
        total_spending = spending_data['total_obligation'].sum()
        avg_contract = spending_data['total_obligation'].mean()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total NJ Federal Spending (REAL)", f"${total_spending:,.0f}")
        
        with col2:
            st.metric("Average Contract Value (REAL)", f"${avg_contract:,.0f}")
        
        with col3:
            st.metric("Number of NJ Contracts (REAL)", len(spending_data))
        
        # Spending trends
        st.markdown('<h3 class="section-header">📊 NJ Spending Trends (REAL)</h3>', unsafe_allow_html=True)
        
        fig = px.bar(spending_data, x='recipient_name', y='total_obligation',
                     title='REAL NJ Federal Construction Contracts by Recipient',
                     color='total_obligation',
                     color_continuous_scale='Reds')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Contract types
        st.markdown('<h3 class="section-header">🏗️ NJ Contract Types (REAL)</h3>', unsafe_allow_html=True)
        
        contract_types = spending_data['naics_description'].value_counts()
        fig = px.pie(values=contract_types.values, names=contract_types.index,
                     title='Distribution of REAL NJ Construction Types')
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.markdown('<h3 class="section-header">📋 NJ Contract Details (REAL)</h3>', unsafe_allow_html=True)
        
        spending_data_display = spending_data.copy()
        spending_data_display['total_obligation'] = spending_data_display['total_obligation'].apply(
            lambda x: f"${x:,.0f}")
        spending_data_display['award_date'] = spending_data_display['award_date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(spending_data_display, use_container_width=True)
        
    else:
        st.error("❌ No real federal spending data available.")

elif page == "🏦 Economic Indicators":
    st.markdown('<h2 class="section-header">📈 NJ Economic Indicators (REAL DATA)</h2>', unsafe_allow_html=True)
    
    # Try to get FRED data
    if FRED_API_KEY != "YOUR_FRED_API_KEY_HERE":
        fred_data = fetch_real_fred_nj_data()
        
        if fred_data is not None and not fred_data.empty:
            st.success("✅ Using REAL FRED data for economic indicators")
            
            # Economic indicators dashboard
            col1, col2 = st.columns(2)
            
            with col1:
                unemployment_data = fred_data[fred_data['series_id'] == 'NJURN']
                if not unemployment_data.empty:
                    fig = px.line(unemployment_data, x='date', y='value',
                                  title='REAL NJ Unemployment Rate (FRED)',
                                  labels={'value': 'Unemployment Rate (%)', 'date': 'Date'})
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                construction_data = fred_data[fred_data['series_id'] == 'NJCONS']
                if not construction_data.empty:
                    fig = px.line(construction_data, x='date', y='value',
                                  title='REAL NJ Construction Employment (FRED)',
                                  labels={'value': 'Employment', 'date': 'Date'})
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
            
            # Show raw FRED data
            st.markdown("### 📋 Raw FRED Data")
            st.dataframe(fred_data, use_container_width=True)
            
        else:
            st.error("❌ Could not fetch FRED data. Check your API key.")
    else:
        st.error("❌ FRED API key not configured. Get your free key at: https://fred.stlouisfed.org/docs/api/api_key.html")

elif page == "🏢 Industry Analysis":
    st.markdown('<h2 class="section-header">🏗️ NJ Construction Industry Analysis</h2>', unsafe_allow_html=True)
    
    st.error("❌ Industry analysis requires additional data sources. This section needs more API integrations.")

elif page == "🗺️ Counties":
    st.markdown('<h2 class="section-header">🗺️ NJ County Analysis</h2>', unsafe_allow_html=True)
    
    st.error("❌ County-level data requires additional BLS series or Census API. This section needs more API integrations.")

elif page == "🔑 API Setup":
    st.markdown('<h2 class="section-header">🔑 API Key Configuration</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>🔑 Required API Keys for Real Data</h3>
        <p>This dashboard only shows REAL data. You need to configure the following API keys:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 📋 API Key Status
    
    #### ✅ BLS API Key (Bureau of Labor Statistics)
    - **Status**: Configured ✅
    - **Your Key**: `79129dd32b5a4e1296cff5eec19d598c`
    - **What it provides**: NJ employment, wages, unemployment data
    - **Cost**: Free
    
    #### ❌ FRED API Key (Federal Reserve Economic Data)
    - **Status**: NOT CONFIGURED ❌
    - **Get your free key**: https://fred.stlouisfed.org/docs/api/api_key.html
    - **What it provides**: NJ economic indicators, unemployment rates
    - **Cost**: Free
    
    #### ✅ USA Spending API
    - **Status**: No key needed ✅
    - **What it provides**: NJ federal contract data
    - **Cost**: Free
    
    #### ℹ️ SEC API
    - **Status**: Requires additional setup
    - **What it provides**: NJ company filings
    - **Cost**: Free
    """)
    
    st.markdown("""
    ### 🔧 How to Configure API Keys
    
    #### 1. Get Your FRED API Key:
    1. Go to: https://fred.stlouisfed.org/docs/api/api_key.html
    2. Fill out the form (it's free)
    3. Copy your API key
    4. Replace `YOUR_FRED_API_KEY_HERE` in the code with your actual key
    
    #### 2. Update the Code:
    ```python
    # In the dashboard code, find this line:
    FRED_API_KEY = "YOUR_FRED_API_KEY_HERE"
    
    # Replace it with your actual key:
    FRED_API_KEY = "your_actual_fred_api_key_here"
    ```
    
    #### 3. Restart the Dashboard:
    After updating the API key, restart the Streamlit app to load the new configuration.
    """)

elif page == "ℹ️ About":
    st.markdown('<h2 class="section-header">ℹ️ About This Dashboard</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>🏗️ IUOE Local 825 - Real Data Only</h3>
        <p>This dashboard shows ONLY REAL data from government sources. No mock data is used.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Dashboard Features
    
    #### 📊 Real Data Sources:
    - **BLS API** - Real NJ employment and wage data
    - **FRED API** - Real NJ economic indicators
    - **USA Spending API** - Real NJ federal contract data
    - **SEC API** - Real NJ company filings (requires setup)
    
    #### 🚫 No Mock Data:
    - If data is unavailable, clear error messages are shown
    - No fake or simulated data
    - Transparent about data availability
    
    ### 🔧 Technical Stack
    
    **Built with:**
    - **Streamlit** - Web application framework
    - **Plotly** - Interactive visualizations
    - **Pandas** - Data manipulation
    - **Requests** - API integration
    
    **Real Data Sources:**
    - **BLS API** - Bureau of Labor Statistics
    - **FRED API** - Federal Reserve Economic Data
    - **USA Spending API** - Federal contract data
    - **SEC API** - Securities and Exchange Commission
    
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
    <p style='font-size: 1.2rem; font-weight: 600;'>🏗️ IUOE Local 825 - Real Data Dashboard</p>
    <p>Built with Streamlit | REAL DATA ONLY | Last updated: """ + datetime.now().strftime("%B %d, %Y") + """</p>
</div>
""", unsafe_allow_html=True) 