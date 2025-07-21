import axios from 'axios';
import { 
  BLSSeries, 
  USASpendingContract, 
  OSHAInspection, 
  DOLData,
  APIResponse 
} from '../types';

// API Configuration with your real keys
const API_CONFIG = {
  BLS_API_KEY: "79129dd32b5a4e1296cff5eec19d598c",
  DOL_API_KEY: "2KZ-OoBMvNjt8ZLKRBTh1tOqfCjnx5x3mruYKvIwnSY",
  OSHA_API_KEY: "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImFhODI4ZDIzMWIwNmIxMzdjNjU3YWVhMjdiNmE2YjUwZDBmYzI2MTAyNThmNjI4YjcwOGQ5Yzk0MTZlODUxODJjMzIxYjZkZjRmMDBhMjBiIn0.eyJhdWQiOiIwMmMzZDM3NC1iMDI3LTQ4YjItOGMyYS0xNjc4NmQ3ZTBkMjgiLCJqdGkiOiJhYTgyOGQyMzFiMDZiMTM3YzY1N2FlYTI3YjZhNmI2YjUwZDBmYzI2MTAyMjU4ZjYyOGI3MDhkOWM5NDE2ZTg1MTgyYzMyMWI2ZGY0ZjAwYTIwYiIsImlhdCI6MTc0NjIxNDcxMywibmJmIjoxNzQ2MjE0NzEzLCJleHAiOjE3NDkyMTQ3MTMuNTQ2MDMxLCJzdWIiOiIzNTk2MDgiLCJzY29wZSI6WyJhdXRoZW50aWNhdGVkIl19.v1EOhdX9vnqcye8MAfbhdBkKqWkZZ0g_RpQFmoA1C9cpKja5qC-Z7tBHmNC2HG_VpKKY-5Lzj5plnN4ZboU-jfUDWNVEbo9X63ClumlVNLZNGKa5rcuc2VKwAnB7sG-f4N_Ov7hZ2KV8B22R5n9722BxqkCgk8hGT7IVuOhPf8inQTKa_ly1KrK8SmKBnyeOu43eXUV0_mBxdgU4BArWiuaK6QKT6XQjx5kNA9LfM9d_lqqRDVLLOpscQdBKLuhEw-ZvyHz95-2MXXNEwBG4JOf_zG00HJX1xefl1wBC7Y4zQACmMwpLQkCvyaABJXldD6yo7Mn7lVBAnFXAxs5sm3jLGHqwu_Y1uEYlPT2XvnqFzq54CcvJwMCG4tRipmS3dOSLB0-gx2lngjXuagQkafFEqYY9txMdEejF0CsyBqiJ0Yft6ah-qme769ytBRCQp6Y-YEwcJ6aT5paR54flOUFM5LhZ8f8ypuNt2wYz-6q8B1haPZ2jdRyc-65EFN4G_qATJJCAIc4Wa8Xx07COe_pcKCmMQ6TvhLXzDiqWo_QI-gK3jeCeCvG6CaRdVbIyafX16ZXNqQYn3Lwkpz08Rki7SdrQt-WEvMCbC8XzCWnAJFaCl3es6haVszcETRKSnOgjrKR6bwrufgSKQ74p94pcA6olTcxNKjvZEpAFGow"
};

// BLS API Service
export const BLSService = {
  async fetchNJConstructionData(): Promise<APIResponse<BLSSeries[]>> {
    try {
      const seriesIds = [
        "CES2023230001", // NJ Construction Employment
        "CES2023230002", // NJ Construction Wages
        "CES2023600001"  // NJ Total Nonfarm Employment
      ];

      const response = await axios.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', {
        seriesid: seriesIds,
        startyear: "2020",
        endyear: "2024",
        registrationkey: API_CONFIG.BLS_API_KEY
      }, {
        headers: {
          'BLS-API-KEY': API_CONFIG.BLS_API_KEY,
          'Content-Type': 'application/json'
        }
      });

      if (response.data.Results?.series) {
        return {
          data: response.data.Results.series,
          success: true
        };
      } else {
        return {
          data: [],
          success: false,
          error: 'No BLS data found'
        };
      }
    } catch (error) {
      return {
        data: [],
        success: false,
        error: `BLS API Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      };
    }
  }
};

// USA Spending API Service
export const USASpendingService = {
  async fetchNJConstructionContracts(): Promise<APIResponse<USASpendingContract[]>> {
    try {
      const response = await axios.post('https://api.usaspending.gov/api/v2/search/spending_by_award/', {
        filters: {
          award_type_codes: ["A", "B", "C", "D"],
          naics_codes: ["23"], // Construction
          recipient_locations: [{ country: "USA", state: "NJ" }],
          time_period: [{ start_date: "2023-01-01", end_date: "2024-12-31" }]
        },
        fields: [
          "award_id", "recipient_name", "total_obligation", 
          "award_date", "naics_code", "naics_description"
        ],
        page: 1,
        limit: 50,
        sort: "total_obligation",
        order: "desc"
      });

      if (response.data.results) {
        return {
          data: response.data.results,
          success: true
        };
      } else {
        return {
          data: [],
          success: false,
          error: 'No USA Spending data found'
        };
      }
    } catch (error) {
      return {
        data: [],
        success: false,
        error: `USA Spending API Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      };
    }
  }
};

// OSHA API Service
export const OSHAService = {
  async fetchNJInspections(): Promise<APIResponse<OSHAInspection[]>> {
    try {
      const response = await axios.get('https://data.osha.gov/api/v1/inspections', {
        headers: {
          'Authorization': `Bearer ${API_CONFIG.OSHA_API_KEY}`,
          'Content-Type': 'application/json'
        },
        params: {
          state: 'NJ',
          limit: 100,
          offset: 0
        }
      });

      if (response.data.results) {
        return {
          data: response.data.results,
          success: true
        };
      } else {
        return {
          data: [],
          success: false,
          error: 'No OSHA data found'
        };
      }
    } catch (error) {
      return {
        data: [],
        success: false,
        error: `OSHA API Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      };
    }
  }
};

// DOL API Service
export const DOLService = {
  async fetchNJLaborData(): Promise<APIResponse<DOLData[]>> {
    try {
      // DOL API endpoint for NJ labor data
      const response = await axios.get('https://api.dol.gov/v1/timeseries', {
        headers: {
          'Authorization': `Bearer ${API_CONFIG.DOL_API_KEY}`,
          'Content-Type': 'application/json'
        },
        params: {
          series_id: 'CES2023230001', // NJ Construction Employment
          start_year: '2020',
          end_year: '2024'
        }
      });

      if (response.data.series) {
        return {
          data: response.data.series,
          success: true
        };
      } else {
        return {
          data: [],
          success: false,
          error: 'No DOL data found'
        };
      }
    } catch (error) {
      return {
        data: [],
        success: false,
        error: `DOL API Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      };
    }
  }
}; 