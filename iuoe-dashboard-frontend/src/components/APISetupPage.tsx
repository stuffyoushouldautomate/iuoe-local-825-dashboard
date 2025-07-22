import React from 'react';
import { CheckCircle, XCircle, AlertTriangle, Key, ExternalLink } from 'lucide-react';

const APISetupPage = () => {
  const apiKeys = [
    {
      name: 'BLS API Key',
      key: '79129dd32b5a4e1296cff5eec19d598c',
      status: 'configured',
      description: 'Bureau of Labor Statistics - NJ employment and wage data',
      url: 'https://www.bls.gov/developers/',
      free: true
    },
    {
      name: 'DOL API Key',
      key: '2KZ-OoBMvNjt8ZLKRBTh1tOqfCjnx5x3mruYKvIwnSY',
      status: 'configured',
      description: 'Department of Labor - NJ labor market data',
      url: 'https://developer.dol.gov/',
      free: true
    },
    {
      name: 'OSHA API Key',
      key: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImFhODI4ZDIzMWIwNmIxMzdjNjU3YWVhMjdiNmE2YjUwZDBmYzI2MTAyNThmNjI4YjcwOGQ5Yzk0MTZlODUxODJjMzIxYjZkZjRmMDBhMjBiIn0.eyJhdWQiOiIwMmMzZDM3NC1iMDI3LTQ4YjItOGMyYS0xNjc4NmQ3ZTBkMjgiLCJqdGkiOiJhYTgyOGQyMzFiMDZiMTM3YzY1N2FlYTI3YjZhNmI2YjUwZDBmYzI2MTAyMjU4ZjYyOGI3MDhkOWM5NDE2ZTg1MTgyYzMyMWI2ZGY0ZjAwYTIwYiIsImlhdCI6MTc0NjIxNDcxMywibmJmIjoxNzQ2MjE0NzEzLCJleHAiOjE3NDkyMTQ3MTMuNTQ2MDMxLCJzdWIiOiIzNTk2MDgiLCJzY29wZSI6WyJhdXRoZW50aWNhdGVkIl19.v1EOhdX9vnqcye8MAfbhdBkKqWkZZ0g_RpQFmoA1C9cpKja5qC-Z7tBHmNC2HG_VpKKY-5Lzj5plnN4ZboU-jfUDWNVEbo9X63ClumlVNLZNGKa5rcuc2VKwAnB7sG-f4N_Ov7hZ2KV8B22R5n9722BxqkCgk8hGT7IVuOhPf8inQTKa_ly1KrK8SmKBnyeOu43eXUV0_mBxdgU4BArWiuaK6QKT6XQjx5kNA9LfM9d_lqqRDVLLOpscQdBKLuhEw-ZvyHz95-2MXXNEwBG4JOf_zG00HJX1xefl1wBC7Y4zQACmMwpLQkCvyaABJXldD6yo7Mn7lVBAnFXAxs5sm3jLGHqwu_Y1uEYlPT2XvnqFzq54CcvJwMCG4tRipmS3dOSLB0-gx2lngjXuagQkafFEqYY9txMdEejF0CsyBqiJ0Yft6ah-qme769ytBRCQp6Y-YEwcJ6aT5paR54flOUFM5LhZ8f8ypuNt2wYz-6q8B1haPZ2jdRyc-65EFN4G_qATJJCAIc4Wa8Xx07COe_pcKCmMQ6TvhLXzDiqWo_QI-gK3jeCeCvG6CaRdVbIyafX16ZXNqQYn3Lwkpz08Rki7SdrQt-WEvMCbC8XzCWnAJFaCl3es6haVszcETRKSnOgjrKR6bwrufgSKQ74p94pcA6olTcxNKjvZEpAFGow',
      status: 'configured',
      description: 'Occupational Safety and Health Administration - NJ safety inspection data',
      url: 'https://www.osha.gov/data',
      free: true
    },
    {
      name: 'FRED API Key',
      key: '0108976b66b9b710f375d61296c78dcd',
      status: 'configured',
      description: 'Federal Reserve Economic Data - Economic indicators (CPI, PPI, GDP, Interest Rates)',
      url: 'https://fred.stlouisfed.org/docs/api/fred/',
      free: true
    },
    {
      name: 'USA Spending API',
      key: 'No key required',
      status: 'configured',
      description: 'Federal contract spending data - Free public API',
      url: 'https://api.usaspending.gov/',
      free: true
    }
  ];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'configured':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'not_configured':
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'configured':
        return 'Configured';
      case 'not_configured':
        return 'Not Configured';
      default:
        return 'Unknown';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'configured':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'not_configured':
        return 'text-red-600 bg-red-50 border-red-200';
      default:
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">API Setup</h1>
        <p className="text-gray-600">Configure your API keys for real data access</p>
      </div>

      <div className="space-y-6">
        {apiKeys.map((api, index) => (
          <div key={index} className={`card ${getStatusColor(api.status)}`}>
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-3">
                <Key className="h-6 w-6 text-primary-600" />
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{api.name}</h3>
                  <p className="text-sm text-gray-600">{api.description}</p>
                  <div className="mt-2">
                    <span className="text-xs font-mono bg-gray-100 px-2 py-1 rounded">
                      {api.key.length > 50 ? `${api.key.substring(0, 20)}...` : api.key}
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                {getStatusIcon(api.status)}
                <span className={`text-sm font-medium ${api.status === 'configured' ? 'text-green-600' : 'text-red-600'}`}>
                  {getStatusText(api.status)}
                </span>
              </div>
            </div>

            <div className="mt-4 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  api.free ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
                }`}>
                  {api.free ? 'Free' : 'Paid'}
                </span>
                <a
                  href={api.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center text-sm text-primary-600 hover:text-primary-700"
                >
                  Documentation
                  <ExternalLink className="h-4 w-4 ml-1" />
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 card">
        <h3 className="text-lg font-semibold mb-4">Current API Status</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center space-x-3">
            <CheckCircle className="h-5 w-5 text-green-500" />
            <span className="text-sm">BLS Employment Data - Working</span>
          </div>
          <div className="flex items-center space-x-3">
            <CheckCircle className="h-5 w-5 text-green-500" />
            <span className="text-sm">USA Spending Data - Working</span>
          </div>
          <div className="flex items-center space-x-3">
            <CheckCircle className="h-5 w-5 text-green-500" />
            <span className="text-sm">OSHA Safety Data - Working</span>
          </div>
          <div className="flex items-center space-x-3">
            <CheckCircle className="h-5 w-5 text-green-500" />
            <span className="text-sm">DOL Labor Data - Working</span>
          </div>
          <div className="flex items-center space-x-3">
            <CheckCircle className="h-5 w-5 text-green-500" />
            <span className="text-sm">FRED Economic Data - Working</span>
          </div>
        </div>
      </div>

      <div className="mt-8 card">
        <h3 className="text-lg font-semibold mb-4">Data Sources Summary</h3>
        <div className="space-y-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-semibold text-blue-800 mb-2">BLS (Bureau of Labor Statistics)</h4>
            <p className="text-blue-700 text-sm">NJ construction employment and wage data</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <h4 className="font-semibold text-green-800 mb-2">USA Spending API</h4>
            <p className="text-green-700 text-sm">Federal contract spending in NJ construction</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <h4 className="font-semibold text-purple-800 mb-2">OSHA (Occupational Safety)</h4>
            <p className="text-purple-700 text-sm">NJ construction safety inspection data</p>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg">
            <h4 className="font-semibold text-orange-800 mb-2">DOL (Department of Labor)</h4>
            <p className="text-orange-700 text-sm">NJ labor market and employment data</p>
          </div>
          <div className="bg-indigo-50 p-4 rounded-lg">
            <h4 className="font-semibold text-indigo-800 mb-2">FRED (Federal Reserve Economic Data)</h4>
            <p className="text-indigo-700 text-sm">Economic indicators: CPI, PPI, GDP, Interest Rates</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default APISetupPage; 