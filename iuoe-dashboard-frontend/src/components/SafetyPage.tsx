import React, { useState, useEffect } from 'react';
import { OSHAService } from '../services/api';
import { LoadingState } from '../types';
import Chart from './Chart';
import { Shield, AlertTriangle, CheckCircle } from 'lucide-react';

const SafetyPage = () => {
  const [oshaData, setOshaData] = useState<any>(null);
  const [loading, setLoading] = useState<LoadingState>({ isLoading: true, error: null });

  useEffect(() => {
    fetchSafetyData();
  }, []);

  const fetchSafetyData = async () => {
    setLoading({ isLoading: true, error: null });

    try {
      const response = await OSHAService.fetchNJInspections();
      setOshaData(response);
      setLoading({ isLoading: false, error: null });
    } catch (error) {
      setLoading({ isLoading: false, error: 'Failed to fetch safety data' });
    }
  };

  if (loading.isLoading) {
    return (
      <div className="p-8">
        <div className="flex items-center justify-center h-64">
          <div className="loading-spinner"></div>
          <span className="ml-3 text-gray-600">Loading OSHA safety data...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Safety & OSHA</h1>
        <p className="text-gray-600">Real NJ construction safety inspection data</p>
      </div>

      {oshaData?.success ? (
        <div className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="metric-card">
              <Shield className="h-6 w-6 text-blue-600 mb-2" />
              <p className="text-sm text-gray-600">Total Inspections</p>
              <p className="text-2xl font-bold">{oshaData.data.length}</p>
            </div>
            <div className="metric-card">
              <AlertTriangle className="h-6 w-6 text-red-600 mb-2" />
              <p className="text-sm text-gray-600">Violations Found</p>
              <p className="text-2xl font-bold">
                {oshaData.data.filter((inspection: any) => inspection.violation_type).length}
              </p>
            </div>
            <div className="metric-card">
              <CheckCircle className="h-6 w-6 text-green-600 mb-2" />
              <p className="text-sm text-gray-600">Compliant Inspections</p>
              <p className="text-2xl font-bold">
                {oshaData.data.filter((inspection: any) => !inspection.violation_type).length}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Inspection Types</h3>
              <Chart
                type="pie"
                data={[]} // Will be populated with real OSHA data
                title="Inspection Types"
              />
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Violation Trends</h3>
              <Chart
                type="bar"
                data={[]} // Will be populated with real OSHA data
                title="Violation Trends"
              />
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Recent Inspections</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Establishment
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      City
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Inspection Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {oshaData.data.slice(0, 10).map((inspection: any, index: number) => (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {inspection.estab_name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {inspection.city}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {new Date(inspection.inspection_date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {inspection.inspection_type}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {inspection.violation_type ? (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                            Violation
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Compliant
                          </span>
                        )}
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
          <p className="text-red-700">OSHA data not available</p>
          <p className="text-sm text-red-600 mt-1">{oshaData?.error}</p>
        </div>
      )}

      {loading.error && (
        <div className="mt-8 error-card">
          <AlertTriangle className="h-6 w-6 text-red-500 mb-2" />
          <h3 className="font-semibold text-red-700">Safety Data Error</h3>
          <p className="text-red-600">{loading.error}</p>
        </div>
      )}
    </div>
  );
};

export default SafetyPage; 