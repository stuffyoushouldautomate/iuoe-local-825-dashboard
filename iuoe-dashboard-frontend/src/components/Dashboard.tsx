import React, { useState, useEffect } from 'react';
import { 
  Users, 
  DollarSign, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  Building2,
  Shield
} from 'lucide-react';
import { BLSService, USASpendingService, OSHAService, DOLService } from '../services/api';
import { DashboardMetrics, LoadingState } from '../types';
import MetricCard from './MetricCard';
import DataStatusCard from './DataStatusCard';
import Chart from './Chart';

const Dashboard = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState<LoadingState>({ isLoading: true, error: null });
  const [dataStatus, setDataStatus] = useState({
    bls: { available: false, error: null },
    spending: { available: false, error: null },
    osha: { available: false, error: null },
    dol: { available: false, error: null }
  });

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    setLoading({ isLoading: true, error: null });

    try {
      // Fetch all data sources in parallel
      const [blsData, spendingData, oshaData, dolData] = await Promise.allSettled([
        BLSService.fetchNJConstructionData(),
        USASpendingService.fetchNJConstructionContracts(),
        OSHAService.fetchNJInspections(),
        DOLService.fetchNJLaborData()
      ]);

      // Update data status
      setDataStatus({
        bls: {
          available: blsData.status === 'fulfilled' && blsData.value.success,
          error: blsData.status === 'rejected' ? blsData.reason : blsData.value.error
        },
        spending: {
          available: spendingData.status === 'fulfilled' && spendingData.value.success,
          error: spendingData.status === 'rejected' ? spendingData.reason : spendingData.value.error
        },
        osha: {
          available: oshaData.status === 'fulfilled' && oshaData.value.success,
          error: oshaData.status === 'rejected' ? oshaData.reason : oshaData.value.error
        },
        dol: {
          available: dolData.status === 'fulfilled' && dolData.value.success,
          error: dolData.status === 'rejected' ? dolData.reason : dolData.value.error
        }
      });

      // Calculate metrics from available data
      const calculatedMetrics = calculateMetrics(blsData, spendingData, oshaData, dolData);
      setMetrics(calculatedMetrics);

      setLoading({ isLoading: false, error: null });
    } catch (error) {
      setLoading({ isLoading: false, error: 'Failed to fetch dashboard data' });
    }
  };

  const calculateMetrics = (blsData: any, spendingData: any, oshaData: any, dolData: any) => {
    let totalEmployment = 0;
    let employmentGrowth = 0;
    let totalSpending = 0;
    let contractCount = 0;
    let averageWage = 0;
    let unemploymentRate = 0;

    // Calculate from BLS data
    if (blsData.status === 'fulfilled' && blsData.value.success) {
      const constructionSeries = blsData.value.data.find((s: any) => s.seriesID === 'CES2023230001');
      if (constructionSeries && constructionSeries.data.length > 0) {
        const latest = parseFloat(constructionSeries.data[0].value);
        const previous = constructionSeries.data.length > 1 ? parseFloat(constructionSeries.data[1].value) : latest;
        totalEmployment = latest;
        employmentGrowth = ((latest - previous) / previous) * 100;
      }
    }

    // Calculate from USA Spending data
    if (spendingData.status === 'fulfilled' && spendingData.value.success) {
      totalSpending = spendingData.value.data.reduce((sum: number, contract: any) => sum + contract.total_obligation, 0);
      contractCount = spendingData.value.data.length;
    }

    return {
      totalEmployment,
      employmentGrowth,
      totalSpending,
      contractCount,
      averageWage,
      unemploymentRate
    };
  };

  if (loading.isLoading) {
    return (
      <div className="p-8">
        <div className="flex items-center justify-center h-64">
          <div className="loading-spinner"></div>
          <span className="ml-3 text-gray-600">Loading real data...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          IUOE Local 825 Dashboard
        </h1>
        <p className="text-gray-600">
          Real-time construction analytics for New Jersey
        </p>
      </div>

      {/* Data Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <DataStatusCard
          title="BLS Employment Data"
          available={dataStatus.bls.available}
          error={dataStatus.bls.error}
          icon={Users}
        />
        <DataStatusCard
          title="USA Spending Data"
          available={dataStatus.spending.available}
          error={dataStatus.spending.error}
          icon={DollarSign}
        />
        <DataStatusCard
          title="OSHA Safety Data"
          available={dataStatus.osha.available}
          error={dataStatus.osha.error}
          icon={Shield}
        />
        <DataStatusCard
          title="DOL Labor Data"
          available={dataStatus.dol.available}
          error={dataStatus.dol.error}
          icon={Building2}
        />
      </div>

      {/* Key Metrics */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="NJ Construction Employment"
            value={metrics.totalEmployment.toLocaleString()}
            change={metrics.employmentGrowth}
            icon={Users}
            color="blue"
          />
          <MetricCard
            title="Federal Contract Spending"
            value={`$${(metrics.totalSpending / 1000000).toFixed(1)}M`}
            change={0}
            icon={DollarSign}
            color="green"
          />
          <MetricCard
            title="Active Contracts"
            value={metrics.contractCount.toString()}
            change={0}
            icon={Building2}
            color="purple"
          />
          <MetricCard
            title="Average Hourly Wage"
            value={`$${metrics.averageWage.toFixed(2)}`}
            change={0}
            icon={TrendingUp}
            color="orange"
          />
        </div>
      )}

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">NJ Construction Employment Trend</h3>
          {dataStatus.bls.available ? (
            <Chart
              type="line"
              data={[]} // Will be populated with real BLS data
              title="Employment Trend"
            />
          ) : (
            <div className="error-card">
              <XCircle className="h-8 w-8 text-red-500 mb-2" />
              <p className="text-red-700">BLS data not available</p>
              <p className="text-sm text-red-600 mt-1">{dataStatus.bls.error}</p>
            </div>
          )}
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">NJ Federal Contract Spending</h3>
          {dataStatus.spending.available ? (
            <Chart
              type="bar"
              data={[]} // Will be populated with real USA Spending data
              title="Contract Spending"
            />
          ) : (
            <div className="error-card">
              <XCircle className="h-8 w-8 text-red-500 mb-2" />
              <p className="text-red-700">USA Spending data not available</p>
              <p className="text-sm text-red-600 mt-1">{dataStatus.spending.error}</p>
            </div>
          )}
        </div>
      </div>

      {/* Error Summary */}
      {loading.error && (
        <div className="mt-8 error-card">
          <AlertTriangle className="h-6 w-6 text-red-500 mb-2" />
          <h3 className="font-semibold text-red-700">Dashboard Error</h3>
          <p className="text-red-600">{loading.error}</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard; 