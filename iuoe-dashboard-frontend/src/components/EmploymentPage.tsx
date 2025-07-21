import React, { useState, useEffect } from 'react';
import { BLSService, DOLService } from '../services/api';
import { LoadingState } from '../types';
import Chart from './Chart';
import { Users, TrendingUp, AlertTriangle } from 'lucide-react';

const EmploymentPage = () => {
  const [blsData, setBlsData] = useState<any>(null);
  const [dolData, setDolData] = useState<any>(null);
  const [loading, setLoading] = useState<LoadingState>({ isLoading: true, error: null });

  useEffect(() => {
    fetchEmploymentData();
  }, []);

  const fetchEmploymentData = async () => {
    setLoading({ isLoading: true, error: null });

    try {
      const [blsResponse, dolResponse] = await Promise.allSettled([
        BLSService.fetchNJConstructionData(),
        DOLService.fetchNJLaborData()
      ]);

      if (blsResponse.status === 'fulfilled') {
        setBlsData(blsResponse.value);
      }

      if (dolResponse.status === 'fulfilled') {
        setDolData(dolResponse.value);
      }

      setLoading({ isLoading: false, error: null });
    } catch (error) {
      setLoading({ isLoading: false, error: 'Failed to fetch employment data' });
    }
  };

  if (loading.isLoading) {
    return (
      <div className="p-8">
        <div className="flex items-center justify-center h-64">
          <div className="loading-spinner"></div>
          <span className="ml-3 text-gray-600">Loading employment data...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Employment & Wages</h1>
        <p className="text-gray-600">Real NJ construction employment and wage data</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="card">
          <div className="flex items-center mb-4">
            <Users className="h-6 w-6 text-primary-600 mr-2" />
            <h3 className="text-lg font-semibold">BLS Employment Data</h3>
          </div>
          
          {blsData?.success ? (
            <Chart
              type="line"
              data={[]} // Will be populated with real BLS data
              title="NJ Construction Employment"
            />
          ) : (
            <div className="error-card">
              <AlertTriangle className="h-8 w-8 text-red-500 mb-2" />
              <p className="text-red-700">BLS data not available</p>
              <p className="text-sm text-red-600 mt-1">{blsData?.error}</p>
            </div>
          )}
        </div>

        <div className="card">
          <div className="flex items-center mb-4">
            <TrendingUp className="h-6 w-6 text-primary-600 mr-2" />
            <h3 className="text-lg font-semibold">DOL Labor Data</h3>
          </div>
          
          {dolData?.success ? (
            <Chart
              type="line"
              data={[]} // Will be populated with real DOL data
              title="NJ Labor Trends"
            />
          ) : (
            <div className="error-card">
              <AlertTriangle className="h-8 w-8 text-red-500 mb-2" />
              <p className="text-red-700">DOL data not available</p>
              <p className="text-sm text-red-600 mt-1">{dolData?.error}</p>
            </div>
          )}
        </div>
      </div>

      {loading.error && (
        <div className="mt-8 error-card">
          <AlertTriangle className="h-6 w-6 text-red-500 mb-2" />
          <h3 className="font-semibold text-red-700">Employment Data Error</h3>
          <p className="text-red-600">{loading.error}</p>
        </div>
      )}
    </div>
  );
};

export default EmploymentPage; 