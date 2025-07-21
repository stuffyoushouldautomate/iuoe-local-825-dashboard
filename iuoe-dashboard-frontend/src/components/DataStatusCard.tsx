import React from 'react';
import { LucideIcon, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';

interface DataStatusCardProps {
  title: string;
  available: boolean;
  error: string | null;
  icon: LucideIcon;
}

const DataStatusCard: React.FC<DataStatusCardProps> = ({ title, available, error, icon: Icon }) => {
  const getStatusIcon = () => {
    if (available) {
      return <CheckCircle className="h-5 w-5 text-green-500" />;
    } else if (error) {
      return <XCircle className="h-5 w-5 text-red-500" />;
    } else {
      return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
    }
  };

  const getStatusText = () => {
    if (available) {
      return 'Available';
    } else if (error) {
      return 'Error';
    } else {
      return 'Unavailable';
    }
  };

  const getStatusColor = () => {
    if (available) {
      return 'text-green-600 bg-green-50 border-green-200';
    } else if (error) {
      return 'text-red-600 bg-red-50 border-red-200';
    } else {
      return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    }
  };

  return (
    <div className={`card ${getStatusColor()}`}>
      <div className="flex items-center justify-between mb-3">
        <Icon className="h-6 w-6" />
        {getStatusIcon()}
      </div>
      
      <div>
        <h3 className="font-semibold text-gray-900 mb-1">{title}</h3>
        <p className={`text-sm font-medium ${available ? 'text-green-600' : error ? 'text-red-600' : 'text-yellow-600'}`}>
          {getStatusText()}
        </p>
        {error && (
          <p className="text-xs text-red-600 mt-2 truncate" title={error}>
            {error}
          </p>
        )}
      </div>
    </div>
  );
};

export default DataStatusCard; 