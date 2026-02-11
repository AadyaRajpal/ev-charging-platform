import React, { createContext, useState, useContext, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { authService } from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authToken, setAuthToken] = useState(null);

  useEffect(() => {
    loadStoredAuth();
  }, []);

  const loadStoredAuth = async () => {
    try {
      const token = await AsyncStorage.getItem('authToken');
      const userData = await AsyncStorage.getItem('user');
      
      if (token && userData) {
        setAuthToken(token);
        setUser(JSON.parse(userData));
      }
    } catch (error) {
      console.error('Error loading auth data:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await authService.login(email, password);
      
      await AsyncStorage.setItem('authToken', response.access_token);
      await AsyncStorage.setItem('refreshToken', response.refresh_token);
      
      // Get user profile
      const userProfile = await authService.getProfile(response.access_token);
      await AsyncStorage.setItem('user', JSON.stringify(userProfile));
      
      setAuthToken(response.access_token);
      setUser(userProfile);
      
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      };
    }
  };

  const register = async (email, password, name, phone) => {
    try {
      const response = await authService.register(email, password, name, phone);
      
      await AsyncStorage.setItem('authToken', response.access_token);
      await AsyncStorage.setItem('refreshToken', response.refresh_token);
      
      // Get user profile
      const userProfile = await authService.getProfile(response.access_token);
      await AsyncStorage.setItem('user', JSON.stringify(userProfile));
      
      setAuthToken(response.access_token);
      setUser(userProfile);
      
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      };
    }
  };

  const logout = async () => {
    try {
      await AsyncStorage.multiRemove(['authToken', 'refreshToken', 'user']);
      setAuthToken(null);
      setUser(null);
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  const refreshAuthToken = async () => {
    try {
      const refreshToken = await AsyncStorage.getItem('refreshToken');
      if (!refreshToken) return false;
      
      const response = await authService.refreshToken(refreshToken);
      
      await AsyncStorage.setItem('authToken', response.access_token);
      await AsyncStorage.setItem('refreshToken', response.refresh_token);
      
      setAuthToken(response.access_token);
      return true;
    } catch (error) {
      console.error('Error refreshing token:', error);
      await logout();
      return false;
    }
  };

  const value = {
    user,
    authToken,
    loading,
    login,
    register,
    logout,
    refreshAuthToken,
    isAuthenticated: !!authToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
