import { useState, useEffect } from 'react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';
const TOKEN_KEY = process.env.NEXT_PUBLIC_JWT_STORAGE_KEY || 'zentix_auth_token';

// Types
export interface User {
  id: string;
  username: string;
  name: string;
  email: string;
  role: string;
}

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
}

export interface LoginResponse {
  access_token: string;
  user: User;
}

export interface DashboardStats {
  total_interactions: number;
  active_users: number;
  happiness_level: number;
  response_time: string;
  uptime: string;
  skills_count: number;
  dna_backup: string;
}

export interface ChatMessage {
  response: string;
  mood: string;
  personality: any;
  timestamp: string;
}

export interface EmotionData {
  name: string;
  سعادة: number;
  قلق: number;
  حياد: number;
}

export interface SkillData {
  name: string;
  status: string;
  performance: number;
  description: string;
}

// Auth Token Management
const getAuthToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(TOKEN_KEY);
};

const setAuthToken = (token: string): void => {
  if (typeof window === 'undefined') return;
  localStorage.setItem(TOKEN_KEY, token);
};

const removeAuthToken = (): void => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(TOKEN_KEY);
};

const getAuthHeaders = (): HeadersInit => ({
  'Content-Type': 'application/json',
  ...(getAuthToken() && { Authorization: `Bearer ${getAuthToken()}` }),
});

// Core API Function
const apiCall = async <T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> => {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      headers: getAuthHeaders(),
      ...options,
    });

    const data = await response.json();

    if (!response.ok) {
      if (response.status === 401) {
        removeAuthToken();
        if (typeof window !== 'undefined') {
          window.location.href = '/auth';
        }
      }
      return { error: data.error || 'An unexpected error occurred' };
    }

    return { data };
  } catch (error) {
    console.error('API call failed:', error);
    return { error: 'Failed to connect to server' };
  }
};

// API Modules
export const authApi = {
  async login(username: string, password: string): Promise<ApiResponse<LoginResponse>> {
    const response = await apiCall<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });

    if (response.data) {
      setAuthToken(response.data.access_token);
    }

    return response;
  },

  async getProfile(): Promise<ApiResponse<{ user: User }>> {
    return apiCall<{ user: User }>('/auth/profile');
  },

  logout(): void {
    removeAuthToken();
    if (typeof window !== 'undefined') {
      window.location.href = '/auth';
    }
  },

  isAuthenticated(): boolean {
    return !!getAuthToken();
  },
};

export const dashboardApi = {
  async getStats(): Promise<ApiResponse<any>> {
    return apiCall('/dashboard/stats');
  },

  async getInteractions(): Promise<ApiResponse<any>> {
    return apiCall('/dashboard/interactions');
  },

  async getActivities(): Promise<ApiResponse<any>> {
    return apiCall('/dashboard/activities');
  },
};

export const emotionsApi = {
  async getWeeklyAnalysis(): Promise<ApiResponse<any>> {
    return apiCall('/emotions/weekly');
  },

  async analyzeText(text: string): Promise<ApiResponse<any>> {
    return apiCall('/emotions/analyze', {
      method: 'POST',
      body: JSON.stringify({ text }),
    });
  },
};

export const chatApi = {
  async sendMessage(message: string): Promise<ApiResponse<any>> {
    return apiCall('/chat/message', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  },
};

export const skillsApi = {
  async getSkills(): Promise<ApiResponse<any>> {
    return apiCall('/skills');
  },

  async createSibling(data: any): Promise<ApiResponse<any>> {
    return apiCall('/skills/create-sibling', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};

export const settingsApi = {
  async getSettings(): Promise<ApiResponse<any>> {
    return apiCall('/settings');
  },

  async updateSettings(settings: any): Promise<ApiResponse<any>> {
    return apiCall('/settings', {
      method: 'POST',
      body: JSON.stringify(settings),
    });
  },
};

// Real-time Data Hook
export const useRealTimeData = <T>(
  apiFunction: () => Promise<ApiResponse<T>>,
  interval: number = 30000
) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const response = await apiFunction();
      
      if (response.error) {
        setError(response.error);
      } else {
        setData(response.data || null);
        setError(null);
      }
      
      setLoading(false);
    };

    fetchData();
    const intervalId = setInterval(fetchData, interval);

    return () => clearInterval(intervalId);
  }, [apiFunction, interval]);

  return { data, loading, error, refetch: () => apiFunction() };
};

export default {
  authApi,
  dashboardApi,
  emotionsApi,
  chatApi,
  skillsApi,
  settingsApi,
  useRealTimeData,
}; 