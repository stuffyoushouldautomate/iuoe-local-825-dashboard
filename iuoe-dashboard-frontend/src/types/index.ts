export interface BLSSeries {
  seriesID: string;
  seriesTitle: string;
  data: BLSDataPoint[];
}

export interface BLSDataPoint {
  year: string;
  period: string;
  value: string;
  date?: string;
}

export interface USASpendingContract {
  award_id: string;
  recipient_name: string;
  total_obligation: number;
  award_date: string;
  naics_code: string;
  naics_description: string;
}

export interface OSHAInspection {
  activity_nr: string;
  estab_name: string;
  city: string;
  state: string;
  inspection_date: string;
  inspection_type: string;
  violation_type: string;
  penalty_amount: number;
}

export interface DOLData {
  series_id: string;
  title: string;
  data: DOLDataPoint[];
}

export interface DOLDataPoint {
  year: string;
  period: string;
  value: number;
  date?: string;
}

export interface DashboardMetrics {
  totalEmployment: number;
  employmentGrowth: number;
  totalSpending: number;
  contractCount: number;
  averageWage: number;
  unemploymentRate: number;
}

export interface APIResponse<T> {
  data: T;
  success: boolean;
  error?: string;
}

export interface LoadingState {
  isLoading: boolean;
  error: string | null;
} 