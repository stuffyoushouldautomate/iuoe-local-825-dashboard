import React, { useState, useEffect } from 'react';
import { FREDService } from '../services/api';
import { LoadingState } from '../types';
import Chart from './Chart';
import { TrendingUp, AlertTriangle, DollarSign } from 'lucide-react';

const EconomicPage = () => {
  const [fredData, setFredData] = useState<any>(null);
  const [loading, setLoading] = useState<LoadingState>({ isLoading: true, error: null });

  useEffect(() => {
    fetchEconomicData();
  }, []);

  const fetchEconomicData = async () => {
    setLoading({ isLoading: true, error: null });

    try {
      const response = await FREDService.fetchNJEconomicData();
      setFredData(response);
      setLoading({ isLoading: false, error: null });
    } catch (error) {
      setLoading({ isLoading: false, error: 'Failed to fetch economic data' });
    }
  };

  if (loading.isLoading) {
    return (
      <div className="p-8">
        <div className="flex items-center justify-center h-64">
          <div className="loading-spinner"></div>
          <span className="ml-3 text-gray-600">Loading economic indicators...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Economic Indicators</h1>
        <p className="text-gray-600">Real NJ economic data from FRED</p>
      </div>

      {fredData?.success ? (
        <div className="space-y-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">NJ Unemployment Rate</h3>
              <Chart
                type="line"
                data={[]} // Will be populated with real FRED data
                title="Unemployment Rate"
              />
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold mb-4">NJ Construction Employment</h3>
              <Chart
                type="line"
                data={[]} // Will be populated with real FRED data
                title="Construction Employment"
              />
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Economic Data Summary</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="metric-card">
                <TrendingUp className="h-6 w-6 text-blue-600 mb-2" />
                <p className="text-sm text-gray-600">Unemployment Rate</p>
                <p className="text-2xl font-bold">--</p>
              </div>
              <div className="metric-card">
                <DollarSign className="h-6 w-6 text-green-600 mb-2" />
                <p className="text-sm text-gray-600">Average Wage</p>
                <p className="text-2xl font-bold">--</p>
              </div>
              <div className="metric-card">
                <TrendingUp className="h-6 w-6 text-purple-600 mb-2" />
                <p className="text-sm text-gray-600">Employment Growth</p>
                <p className="text-2xl font-bold">--</p>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="error-card">
          <AlertTriangle className="h-8 w-8 text-red-500 mb-2" />
          <p className="text-red-700">FRED data not available</p>
          <p className="text-sm text-red-600 mt-1">{fredData?.error}</p>
          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <h4 className="font-semibold text-blue-800 mb-2">Get Your FRED API Key</h4>
            <p className="text-blue-700 text-sm mb-2">
              To access real economic data, you need a free FRED API key:
            </p>
            <ol className="text-blue-700 text-sm space-y-1">
              <li>1. Go to: <a href="https://fred.stlouisfed.org/docs/api/api_key.html" className="underline" target="_blank" rel="noopener noreferrer">FRED API Key Request</a></li>
              <li>2. Fill out the form (it's free)</li>
              <li>3. Copy your API key</li>
              <li>4. Update the key in the API Setup page</li>
            </ol>
          </div>
        </div>
      )}

      {loading.error && (
        <div className="mt-8 error-card">
          <AlertTriangle className="h-6 w-6 text-red-500 mb-2" />
          <h3 className="font-semibold text-red-700">Economic Data Error</h3>
          <p className="text-red-600">{loading.error}</p>
        </div>
      )}
    </div>
  );
};

export default EconomicPage; 