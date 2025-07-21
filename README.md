# IUOE Local 825 - Construction Analytics Platform

A comprehensive analytics platform for IUOE Local 825 that provides real-time construction industry data for New Jersey using government APIs.

## 🏗️ Project Overview

This platform consists of two main components:
1. **React Frontend Dashboard** - Modern web interface for data visualization
2. **Streamlit Dashboards** - Python-based analytics dashboards

## 📊 Real Data Sources

### Government APIs Integrated:
- **BLS (Bureau of Labor Statistics)** - NJ construction employment and wage data
- **USA Spending API** - Federal contract spending in NJ construction
- **OSHA (Occupational Safety and Health Administration)** - NJ safety inspection data
- **DOL (Department of Labor)** - NJ labor market data

### API Keys Configured:
- ✅ **BLS API Key**: `79129dd32b5a4e1296cff5eec19d598c`
- ✅ **DOL API Key**: `2KZ-OoBMvNjt8ZLKRBTh1tOqfCjnx5x3mruYKvIwnSY`
- ✅ **OSHA API Key**: JWT token configured
- ✅ **USA Spending API**: No key required (public API)

## 🚀 Quick Start

### Option 1: React Frontend (Recommended)

```bash
# Navigate to the frontend directory
cd iuoe-dashboard-frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Open browser to http://localhost:3000
```

### Option 2: Streamlit Dashboards

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the main dashboard
streamlit run iuoe_local_825_real_only_dashboard.py --server.port 8506

# Open browser to http://localhost:8506
```

## 📁 Project Structure

```
IUOE-Local-825/
├── iuoe-dashboard-frontend/          # React frontend
│   ├── src/
│   │   ├── components/              # React components
│   │   ├── services/               # API services
│   │   ├── types/                  # TypeScript types
│   │   └── App.tsx                 # Main app
│   ├── package.json                # Dependencies
│   └── README.md                   # Frontend docs
├── iuoe_local_825_real_only_dashboard.py  # Streamlit dashboard
├── iuoe_local_825_simple_dashboard.py     # Simple Streamlit version
├── requirements.txt                 # Python dependencies
└── README.md                       # This file
```

## 🎯 Dashboard Features

### React Frontend Features:
- **Modern UI**: Clean, professional interface with Tailwind CSS
- **Real-time Data**: Live API calls with loading states
- **Interactive Charts**: Plotly.js visualizations
- **Error Handling**: Graceful error display for API failures
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Navigation**: Sidebar with multiple data sections

### Streamlit Dashboard Features:
- **Quick Setup**: Easy to run with minimal configuration
- **Real Data Integration**: Uses actual government APIs
- **Multiple Sections**: Employment, spending, safety, economic data
- **Error Handling**: Clear error messages when data unavailable

## 📊 Data Sections

### 1. Overview Dashboard
- Key metrics and data status
- Real-time API availability indicators
- Summary statistics

### 2. Employment & Wages
- BLS employment data for NJ construction
- DOL labor market indicators
- Wage trends and employment growth

### 3. Federal Spending
- USA Spending contract data
- NJ construction contracts
- Contract values and recipients

### 4. Safety & OSHA
- OSHA inspection data for NJ
- Safety violations and compliance
- Inspection trends

### 5. API Setup
- Configure API keys
- Monitor data source status
- Documentation links

## 🛠️ Technology Stack

### Frontend (React):
- **React 18** + TypeScript
- **Tailwind CSS** for styling
- **Plotly.js** for charts
- **Axios** for API calls
- **Vite** for build tooling

### Backend (Streamlit):
- **Python 3.8+**
- **Streamlit** for web app
- **Pandas** for data processing
- **Plotly** for visualizations
- **Requests** for API calls

## 🔧 Development

### Frontend Development:
```bash
cd iuoe-dashboard-frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend Development:
```bash
pip install -r requirements.txt
streamlit run iuoe_local_825_real_only_dashboard.py
```

## 📈 Data Sources Details

### BLS (Bureau of Labor Statistics)
- **Series IDs**: CES2023230001 (Construction Employment), CES2023230002 (Wages)
- **Coverage**: NJ construction employment and wage trends
- **Update Frequency**: Monthly

### USA Spending API
- **Filters**: NJ construction contracts (NAICS 23)
- **Data**: Contract values, recipients, award dates
- **Coverage**: Federal spending in NJ

### OSHA (Occupational Safety and Health Administration)
- **Data**: Safety inspections, violations, penalties
- **Coverage**: NJ construction safety data
- **Focus**: Workplace safety compliance

### DOL (Department of Labor)
- **Data**: Labor market indicators, employment trends
- **Coverage**: NJ labor market analysis
- **Series**: Employment, wages, labor force participation

## 🎯 IUOE Local 825 Focus

This platform is specifically designed for IUOE Local 825:
- **NJ Construction Focus**: All data filtered for New Jersey
- **Union-Relevant Metrics**: Employment, wages, safety, contracts
- **Strategic Planning**: Economic indicators for union leadership
- **Contract Monitoring**: Federal spending affecting NJ construction

## 🚨 Error Handling

Both dashboards include comprehensive error handling:
- **API Failures**: Clear error messages with retry options
- **Missing Data**: Graceful fallbacks and status indicators
- **Network Issues**: Loading states and timeout handling
- **Invalid API Keys**: Helpful setup instructions

## 📞 Support

For technical support or questions:
- Check the API Setup page for configuration help
- Review the console for detailed error messages
- Ensure all API keys are properly configured
- Contact the development team for additional support

## 🔄 Updates

The platform automatically:
- Fetches fresh data on page load
- Shows real-time API status
- Displays loading states during data retrieval
- Handles API rate limits gracefully

## 📝 License

This project is developed for IUOE Local 825 and is intended for internal use.

---

**Built for IUOE Local 825 - New Jersey Construction Analytics**
