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

export interface LoginResponse {
  access_token: string;
  user: User;
}

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  message?: string;
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

// Helper Functions
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

const getAuthHeaders = (): HeadersInit => {
  const token = getAuthToken();
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
  };
};

// Generic API call function with error handling
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
      // Handle JWT expiration
      if (response.status === 401) {
        removeAuthToken();
        if (typeof window !== 'undefined') {
          window.location.href = '/auth';
        }
      }
      return { error: data.error || 'حدث خطأ غير متوقع' };
    }

    return { data };
  } catch (error) {
    console.error('API call failed:', error);
    return { error: 'فشل في الاتصال بالخادم' };
  }
};

// Authentication API
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

// Dashboard API
export const dashboardApi = {
  async getStats(): Promise<ApiResponse<DashboardStats>> {
    return apiCall<DashboardStats>('/dashboard/stats');
  },

  async getInteractions(): Promise<ApiResponse<{ data: any[] }>> {
    return apiCall<{ data: any[] }>('/dashboard/interactions');
  },

  async getActivities(): Promise<ApiResponse<{ activities: any[] }>> {
    return apiCall<{ activities: any[] }>('/dashboard/activities');
  },
};

// Emotions API
export const emotionsApi = {
  async getWeeklyData(): Promise<ApiResponse<{ data: EmotionData[] }>> {
    return apiCall<{ data: EmotionData[] }>('/emotions/weekly');
  },

  async analyzeText(text: string): Promise<ApiResponse<{
    emotion: string;
    confidence: number;
    analysis: any;
  }>> {
    return apiCall('/emotions/analyze', {
      method: 'POST',
      body: JSON.stringify({ text }),
    });
  },
};

// Chat API
export const chatApi = {
  async sendMessage(message: string): Promise<ApiResponse<ChatMessage>> {
    return apiCall<ChatMessage>('/chat/message', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  },
};

// Skills API
export const skillsApi = {
  async getSkills(): Promise<ApiResponse<{
    skills: SkillData[];
    performance: any[];
  }>> {
    return apiCall('/skills');
  },

  async createSibling(traits: any = {}): Promise<ApiResponse<{
    success: boolean;
    sibling: any;
    message: string;
  }>> {
    return apiCall('/skills/create-sibling', {
      method: 'POST',
      body: JSON.stringify({ traits }),
    });
  },
};

// Settings API
export const settingsApi = {
  async getSettings(): Promise<ApiResponse<{ settings: any }>> {
    return apiCall('/settings');
  },

  async updateSettings(settings: any): Promise<ApiResponse<{
    success: boolean;
    message: string;
  }>> {
    return apiCall('/settings', {
      method: 'POST',
      body: JSON.stringify(settings),
    });
  },
};

// Health Check API
export const healthApi = {
  async check(): Promise<ApiResponse<{
    status: string;
    timestamp: string;
    service: string;
    version: string;
  }>> {
    return apiCall('/health');
  },
};

// Utility functions for error handling
export const handleApiError = (error: string): string => {
  // Common error messages translation
  const errorMap: { [key: string]: string } = {
    'Network Error': 'خطأ في الشبكة',
    'Unauthorized': 'غير مصرح',
    'Forbidden': 'ممنوع',
    'Not Found': 'غير موجود',
    'Internal Server Error': 'خطأ داخلي في الخادم',
  };

  return errorMap[error] || error;
};

// Real-time data fetching with auto-refresh
export const useRealTimeData = <T>(
  apiFunction: () => Promise<ApiResponse<T>>,
  interval: number = 30000 // 30 seconds
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

  const refetch = async () => {
    const response = await apiFunction();
    if (response.error) {
      setError(response.error);
    } else {
      setData(response.data || null);
      setError(null);
    }
  };

  return { data, loading, error, refetch };
};

export default {
  authApi,
  dashboardApi,
  emotionsApi,
  chatApi,
  skillsApi,
  settingsApi,
  healthApi,
  handleApiError,
  useRealTimeData,
}; 