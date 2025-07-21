import React, { useState, useEffect } from 'react';
import { USASpendingService } from '../services/api';
import { LoadingState } from '../types';
import Chart from './Chart';
import { DollarSign, Building2, AlertTriangle } from 'lucide-react';

const SpendingPage = () => {
  const [spendingData, setSpendingData] = useState<any>(null);
  const [loading, setLoading] = useState<LoadingState>({ isLoading: true, error: null });

  useEffect(() => {
    fetchSpendingData();
  }, []);

  const fetchSpendingData = async () => {
    setLoading({ isLoading: true, error: null });

    try {
      const response = await USASpendingService.fetchNJConstructionContracts();
      setSpendingData(response);
      setLoading({ isLoading: false, error: null });
    } catch (error) {
      setLoading({ isLoading: false, error: 'Failed to fetch spending data' });
    }
  };

  if (loading.isLoading) {
    return (
      <div className="p-8">
        <div className="flex items-center justify-center h-64">
          <div className="loading-spinner"></div>
          <span className="ml-3 text-gray-600">Loading federal spending data...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Federal Spending</h1>
        <p className="text-gray-600">Real NJ construction contract data from USA Spending</p>
      </div>

      {spendingData?.success ? (
        <div className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="metric-card">
              <DollarSign className="h-6 w-6 text-green-600 mb-2" />
              <p className="text-sm text-gray-600">Total Spending</p>
              <p className="text-2xl font-bold">
                ${(spendingData.data.reduce((sum: number, contract: any) => sum + contract.total_obligation, 0) / 1000000).toFixed(1)}M
              </p>
            </div>
            <div className="metric-card">
              <Building2 className="h-6 w-6 text-blue-600 mb-2" />
              <p className="text-sm text-gray-600">Active Contracts</p>
              <p className="text-2xl font-bold">{spendingData.data.length}</p>
            </div>
            <div className="metric-card">
              <DollarSign className="h-6 w-6 text-purple-600 mb-2" />
              <p className="text-sm text-gray-600">Average Contract</p>
              <p className="text-2xl font-bold">
                ${(spendingData.data.reduce((sum: number, contract: any) => sum + contract.total_obligation, 0) / spendingData.data.length / 1000000).toFixed(1)}M
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Contract Values by Recipient</h3>
              <Chart
                type="bar"
                data={[]} // Will be populated with real spending data
                title="Contract Values"
              />
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Spending Distribution</h3>
              <Chart
                type="pie"
                data={[]} // Will be populated with real spending data
                title="Spending Distribution"
              />
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Contract Details</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Recipient
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Contract Value
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Award Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Type
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {spendingData.data.slice(0, 10).map((contract: any, index: number) => (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {contract.recipient_name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        ${(contract.total_obligation / 1000000).toFixed(1)}M
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {new Date(contract.award_date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {contract.naics_description}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        <div className="error-card">
          <AlertTriangle className="h-8 w-8 text-red-500 mb-2" />
          <p className="text-red-700">USA Spending data not available</p>
          <p className="text-sm text-red-600 mt-1">{spendingData?.error}</p>
        </div>
      )}

      {loading.error && (
        <div className="mt-8 error-card">
          <AlertTriangle className="h-6 w-6 text-red-500 mb-2" />
          <h3 className="font-semibold text-red-700">Spending Data Error</h3>
          <p className="text-red-600">{loading.error}</p>
        </div>
      )}
    </div>
  );
};

export default SpendingPage; 