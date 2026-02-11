import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_BASE_URL } from '@env';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = await AsyncStorage.getItem('refreshToken');
        
        if (!refreshToken) {
          throw new Error('No refresh token');
        }

        // Request new tokens
        const response = await axios.post(
          `${API_BASE_URL}/auth/refresh`,
          { refresh_token: refreshToken }
        );

        const { access_token, refresh_token: newRefreshToken } = response.data;

        // Store new tokens
        await AsyncStorage.setItem('authToken', access_token);
        await AsyncStorage.setItem('refreshToken', newRefreshToken);

        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        await AsyncStorage.multiRemove(['authToken', 'refreshToken', 'user']);
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth Service
export const authService = {
  login: async (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await axios.post(
      `${API_BASE_URL}/auth/login`,
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
      }
    );
    return response.data;
  },

  register: async (email, password, name, phone) => {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, {
      email,
      password,
      name,
      phone,
    });
    return response.data;
  },

  refreshToken: async (refreshToken) => {
    const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
      refresh_token: refreshToken,
    });
    return response.data;
  },

  getProfile: async (token) => {
    const response = await axios.get(`${API_BASE_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },
};

// Stations Service
export const stationsService = {
  getNearbyStations: async (latitude, longitude, radius = 5000, filters = {}) => {
    const params = { latitude, longitude, radius, ...filters };
    const response = await apiClient.get('/stations/nearby', { params });
    return response.data;
  },

  getStationDetails: async (stationId, provider) => {
    const response = await apiClient.get(`/stations/${stationId}`, {
      params: { provider },
    });
    return response.data;
  },

  getStationAvailability: async (stationId) => {
    const response = await apiClient.get(`/stations/${stationId}/availability`);
    return response.data;
  },

  addFavorite: async (stationId) => {
    const response = await apiClient.post(`/stations/${stationId}/favorite`);
    return response.data;
  },

  removeFavorite: async (stationId) => {
    const response = await apiClient.delete(`/stations/${stationId}/favorite`);
    return response.data;
  },

  getFavorites: async () => {
    const response = await apiClient.get('/stations/user/favorites');
    return response.data;
  },
};

// Sessions Service
export const sessionsService = {
  startSession: async (stationId, chargerId, provider, estimatedKwh) => {
    const response = await apiClient.post('/sessions/start', {
      station_id: stationId,
      charger_id: chargerId,
      provider,
      estimated_kwh: estimatedKwh,
    });
    return response.data;
  },

  stopSession: async (sessionId, provider) => {
    const response = await apiClient.post(`/sessions/${sessionId}/stop`, null, {
      params: { provider },
    });
    return response.data;
  },

  getActiveSessions: async () => {
    const response = await apiClient.get('/sessions/active');
    return response.data;
  },

  getSessionStatus: async (sessionId, provider) => {
    const response = await apiClient.get(`/sessions/${sessionId}/status`, {
      params: { provider },
    });
    return response.data;
  },

  getSessionHistory: async (limit = 20, offset = 0) => {
    const response = await apiClient.get('/sessions/history', {
      params: { limit, offset },
    });
    return response.data;
  },

  getSessionDetails: async (sessionId) => {
    const response = await apiClient.get(`/sessions/${sessionId}`);
    return response.data;
  },

  getStats: async () => {
    const response = await apiClient.get('/sessions/stats/summary');
    return response.data;
  },
};

// Payments Service
export const paymentsService = {
  addPaymentMethod: async (paymentMethodId) => {
    const response = await apiClient.post('/payments/methods', {
      payment_method_id: paymentMethodId,
    });
    return response.data;
  },

  getPaymentMethods: async () => {
    const response = await apiClient.get('/payments/methods');
    return response.data;
  },

  removePaymentMethod: async (paymentMethodId) => {
    const response = await apiClient.delete(`/payments/methods/${paymentMethodId}`);
    return response.data;
  },

  createPaymentIntent: async (amount, sessionId, stationId, paymentMethodId) => {
    const response = await apiClient.post('/payments/create-intent', {
      amount,
      currency: 'usd',
      session_id: sessionId,
      station_id: stationId,
      payment_method_id: paymentMethodId,
    });
    return response.data;
  },

  confirmPayment: async (paymentIntentId) => {
    const response = await apiClient.post('/payments/confirm', null, {
      params: { payment_intent_id: paymentIntentId },
    });
    return response.data;
  },

  getPaymentHistory: async (limit = 10) => {
    const response = await apiClient.get('/payments/history', {
      params: { limit },
    });
    return response.data;
  },
};

// User Service
export const userService = {
  getProfile: async () => {
    const response = await apiClient.get('/user/profile');
    return response.data;
  },

  updateProfile: async (profileData) => {
    const response = await apiClient.put('/user/profile', profileData);
    return response.data;
  },

  getVehicles: async () => {
    const response = await apiClient.get('/user/vehicles');
    return response.data;
  },

  addVehicle: async (vehicleData) => {
    const response = await apiClient.post('/user/vehicles', vehicleData);
    return response.data;
  },

  updateVehicle: async (vehicleId, updates) => {
    const response = await apiClient.put(`/user/vehicles/${vehicleId}`, updates);
    return response.data;
  },

  deleteVehicle: async (vehicleId) => {
    const response = await apiClient.delete(`/user/vehicles/${vehicleId}`);
    return response.data;
  },

  getNotifications: async (limit = 20) => {
    const response = await apiClient.get('/user/notifications', {
      params: { limit },
    });
    return response.data;
  },
};

export default apiClient;
