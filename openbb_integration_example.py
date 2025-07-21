"""
OpenBB Integration Example for IUOE Local 825 Dashboard

This script demonstrates how to integrate real OpenBB data for the labor union dashboard.
Replace the mock data functions in iuoe_local_825_dashboard.py with these real data functions.
"""

from openbb import obb
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def get_real_construction_employment():
    """
    Get real construction employment data for New Jersey using OpenBB Platform
    """
    try:
        # Get construction employment data from BLS
        # Survey: SM (State and Area Employment)
        # Area: 3400000 (New Jersey)
        # Industry: 20000000 (Construction)
        # Measure: 05 (Employment)
        
        data = obb.economy.bls(
            survey="SM",
            area="3400000",  # New Jersey
            industry="20000000",  # Construction
            measure="05",  # Employment
            start_date="2020-01-01"
        )
        
        return data.to_dataframe()
    
    except Exception as e:
        print(f"Error fetching construction employment data: {e}")
        # Return mock data as fallback
        return get_mock_construction_employment()

def get_real_wage_data():
    """
    Get real wage data for construction in New Jersey
    """
    try:
        # Get Employment Cost Index for construction
        # Survey: CI (Employment Cost Index)
        # Industry: 230000 (Construction)
        
        data = obb.economy.bls(
            survey="CI",
            industry="230000",  # Construction
            measure="02",  # Wages and salaries
            start_date="2020-01-01"
        )
        
        return data.to_dataframe()
    
    except Exception as e:
        print(f"Error fetching wage data: {e}")
        return get_mock_wage_data()

def get_real_unemployment_data():
    """
    Get real unemployment data for New Jersey
    """
    try:
        # Get Local Area Unemployment Statistics
        # Survey: LA (Local Area Unemployment Statistics)
        # Area: 3400000 (New Jersey)
        # Measure: 03 (Unemployment rate)
        
        data = obb.economy.bls(
            survey="LA",
            area="3400000",  # New Jersey
            measure="03",  # Unemployment rate
            start_date="2020-01-01"
        )
        
        return data.to_dataframe()
    
    except Exception as e:
        print(f"Error fetching unemployment data: {e}")
        return get_mock_unemployment_data()

def get_real_economic_indicators():
    """
    Get real economic indicators from FRED
    """
    try:
        # Get CPI data
        cpi_data = obb.economy.fred_series(
            symbol="CPIAUCSL",  # Consumer Price Index
            start_date="2020-01-01"
        )
        
        # Get PPI for construction
        ppi_data = obb.economy.fred_series(
            symbol="WPUFD4",  # Producer Price Index - Construction
            start_date="2020-01-01"
        )
        
        # Get Federal Funds Rate
        interest_data = obb.economy.fred_series(
            symbol="FEDFUNDS",  # Federal Funds Rate
            start_date="2020-01-01"
        )
        
        # Combine data
        combined_data = pd.DataFrame({
            'date': cpi_data.to_dataframe()['date'],
            'cpi': cpi_data.to_dataframe()['value'],
            'ppi_construction': ppi_data.to_dataframe()['value'],
            'interest_rate': interest_data.to_dataframe()['value']
        })
        
        return combined_data
    
    except Exception as e:
        print(f"Error fetching economic indicators: {e}")
        return get_mock_economic_indicators()

def get_real_jolts_data():
    """
    Get JOLTS (Job Openings and Labor Turnover Survey) data for construction
    """
    try:
        # Get JOLTS data for construction
        # Survey: JL (Job Openings and Labor Turnover Survey)
        # Industry: 200000 (Construction)
        
        data = obb.economy.bls(
            survey="JL",
            industry="200000",  # Construction
            measure="JO",  # Job openings
            start_date="2020-01-01"
        )
        
        return data.to_dataframe()
    
    except Exception as e:
        print(f"Error fetching JOLTS data: {e}")
        return get_mock_jolts_data()

def get_real_benefits_data():
    """
    Get employer costs for employee compensation data
    """
    try:
        # Get Employer Costs for Employee Compensation
        # Survey: CC (Employer Costs for Employee Compensation)
        # Industry: 230000 (Construction)
        
        data = obb.economy.bls(
            survey="CC",
            industry="230000",  # Construction
            measure="03",  # Total benefits
            start_date="2020-01-01"
        )
        
        return data.to_dataframe()
    
    except Exception as e:
        print(f"Error fetching benefits data: {e}")
        return get_mock_benefits_data()

# Mock data functions as fallbacks
def get_mock_construction_employment():
    """Fallback mock data for construction employment"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='M')
    employment = [150000 + i*100 + np.random.normal(0, 500) for i in range(len(dates))]
    return pd.DataFrame({
        'date': dates,
        'employment': employment
    })

def get_mock_wage_data():
    """Fallback mock data for wages"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='Q')
    return pd.DataFrame({
        'date': dates,
        'hourly_wage': [35 + i*0.5 + np.random.normal(0, 1) for i in range(len(dates))]
    })

def get_mock_unemployment_data():
    """Fallback mock data for unemployment"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='M')
    return pd.DataFrame({
        'date': dates,
        'unemployment_rate': [5.2 + np.random.normal(0, 0.5) for _ in range(len(dates))]
    })

def get_mock_economic_indicators():
    """Fallback mock data for economic indicators"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='M')
    return pd.DataFrame({
        'date': dates,
        'cpi': [100 + i*0.2 + np.random.normal(0, 0.1) for i in range(len(dates))],
        'ppi_construction': [100 + i*0.3 + np.random.normal(0, 0.2) for i in range(len(dates))],
        'interest_rate': [2.5 + i*0.1 + np.random.normal(0, 0.05) for i in range(len(dates))]
    })

def get_mock_jolts_data():
    """Fallback mock data for JOLTS"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='M')
    return pd.DataFrame({
        'date': dates,
        'job_openings': [5000 + np.random.normal(0, 200) for _ in range(len(dates))]
    })

def get_mock_benefits_data():
    """Fallback mock data for benefits"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='Q')
    return pd.DataFrame({
        'date': dates,
        'benefits_cost': [15 + i*0.3 + np.random.normal(0, 0.5) for i in range(len(dates))]
    })

# Example usage
if __name__ == "__main__":
    print("Testing OpenBB Integration for IUOE Local 825 Dashboard")
    print("=" * 60)
    
    # Test each data function
    print("\n1. Testing Construction Employment Data:")
    employment_data = get_real_construction_employment()
    print(f"   Retrieved {len(employment_data)} records")
    print(f"   Latest employment: {employment_data['employment'].iloc[-1]:,.0f}")
    
    print("\n2. Testing Wage Data:")
    wage_data = get_real_wage_data()
    print(f"   Retrieved {len(wage_data)} records")
    
    print("\n3. Testing Unemployment Data:")
    unemployment_data = get_real_unemployment_data()
    print(f"   Retrieved {len(unemployment_data)} records")
    
    print("\n4. Testing Economic Indicators:")
    economic_data = get_real_economic_indicators()
    print(f"   Retrieved {len(economic_data)} records")
    
    print("\n5. Testing JOLTS Data:")
    jolts_data = get_real_jolts_data()
    print(f"   Retrieved {len(jolts_data)} records")
    
    print("\n6. Testing Benefits Data:")
    benefits_data = get_real_benefits_data()
    print(f"   Retrieved {len(benefits_data)} records")
    
    print("\n" + "=" * 60)
    print("Integration test completed!")
    print("\nTo use this in the dashboard:")
    print("1. Replace the mock data functions in iuoe_local_825_dashboard.py")
    print("2. Import these real data functions")
    print("3. Update the dashboard to use real data instead of mock data") 