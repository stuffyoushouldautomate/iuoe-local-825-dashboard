# IUOE Local 825 - Construction Analytics Dashboard

A modern React dashboard for IUOE Local 825 that displays real construction industry data for New Jersey using government APIs.

## 🏗️ Features

### Real Data Sources
- **BLS (Bureau of Labor Statistics)** - NJ construction employment and wage data
- **USA Spending API** - Federal contract spending in NJ
- **OSHA (Occupational Safety and Health Administration)** - NJ safety inspection data
- **DOL (Department of Labor)** - NJ labor market data
- **FRED (Federal Reserve Economic Data)** - NJ economic indicators (requires API key)

### Dashboard Sections
- **Overview Dashboard** - Key metrics and data status
- **Employment & Wages** - BLS and DOL employment data
- **Federal Spending** - USA Spending contract data
- **Safety & OSHA** - OSHA inspection and violation data
- **Economic Indicators** - FRED economic data
- **API Setup** - Configure your API keys

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. **Navigate to the dashboard directory:**
   ```bash
   cd iuoe-dashboard-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000`

## 🔑 API Configuration

### Already Configured APIs
- ✅ **BLS API Key**: `79129dd32b5a4e1296cff5eec19d598c`
- ✅ **DOL API Key**: `2KZ-OoBMvNjt8ZLKRBTh1tOqfCjnx5x3mruYKvIwnSY`
- ✅ **OSHA API Key**: Configured with your JWT token
- ✅ **USA Spending API**: No key required (public API)

### Optional: FRED API Key
To get economic indicators data:

1. Visit [FRED API Key Request](https://fred.stlouisfed.org/docs/api/api_key.html)
2. Fill out the free form
3. Copy your API key
4. Update `src/services/api.ts`:
   ```typescript
   FRED_API_KEY: "YOUR_ACTUAL_FRED_KEY_HERE"
   ```

## 📊 Data Sources

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

### FRED (Federal Reserve Economic Data)
- **Series**: NJURN (Unemployment), NJCONS (Construction), NJWAGE (Wages)
- **Coverage**: NJ economic indicators
- **Requirement**: Free API key

## 🛠️ Technology Stack

- **Frontend**: React 18 + TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Plotly.js
- **Icons**: Lucide React
- **Build Tool**: Vite
- **HTTP Client**: Axios

## 📁 Project Structure

```
iuoe-dashboard-frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Dashboard.tsx   # Main dashboard
│   │   ├── Sidebar.tsx     # Navigation
│   │   ├── MetricCard.tsx  # Metric display
│   │   ├── Chart.tsx       # Chart component
│   │   └── ...             # Other pages
│   ├── services/           # API services
│   │   └── api.ts         # All API integrations
│   ├── types/             # TypeScript types
│   │   └── index.ts       # Type definitions
│   ├── App.tsx            # Main app component
│   └── main.tsx           # Entry point
├── package.json           # Dependencies
├── vite.config.ts         # Build configuration
└── README.md             # This file
```

## 🎨 UI Features

- **Modern Design**: Clean, professional interface
- **Responsive**: Works on desktop, tablet, and mobile
- **Real-time Data**: Live API calls with loading states
- **Error Handling**: Graceful error display for API failures
- **Data Status**: Visual indicators for API availability
- **Interactive Charts**: Plotly.js visualizations

## 🔧 Development

### Available Scripts
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

### Adding New Data Sources
1. Add API service in `src/services/api.ts`
2. Create TypeScript types in `src/types/index.ts`
3. Add new page component in `src/components/`
4. Update routing in `src/App.tsx`

## 📈 Data Visualization

The dashboard uses Plotly.js for interactive charts:
- **Line Charts**: Employment trends over time
- **Bar Charts**: Contract values by recipient
- **Pie Charts**: Spending distribution
- **Tables**: Detailed data listings

## 🚨 Error Handling

The dashboard includes comprehensive error handling:
- **API Failures**: Clear error messages with retry options
- **Missing Data**: Graceful fallbacks and status indicators
- **Network Issues**: Loading states and timeout handling
- **Invalid API Keys**: Helpful setup instructions

## 🎯 IUOE Local 825 Focus

This dashboard is specifically designed for IUOE Local 825:
- **NJ Construction Focus**: All data filtered for New Jersey
- **Union-Relevant Metrics**: Employment, wages, safety, contracts
- **Strategic Planning**: Economic indicators for union leadership
- **Contract Monitoring**: Federal spending affecting NJ construction

## 📞 Support

For technical support or questions about the dashboard:
- Check the API Setup page for configuration help
- Review the console for detailed error messages
- Ensure all API keys are properly configured

## 🔄 Updates

The dashboard automatically:
- Fetches fresh data on page load
- Shows real-time API status
- Displays loading states during data retrieval
- Handles API rate limits gracefully

---

**Built for IUOE Local 825 - New Jersey Construction Analytics** 