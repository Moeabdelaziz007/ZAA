import { authApi, dashboardApi, emotionsApi, chatApi, skillsApi } from '../lib/api';

// Mock fetch globally
global.fetch = jest.fn();

const mockFetch = fetch as jest.MockedFunction<typeof fetch>;

describe('API Client Tests', () => {
  beforeEach(() => {
    mockFetch.mockClear();
    // Clear localStorage
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: jest.fn(),
        setItem: jest.fn(),
        removeItem: jest.fn(),
        clear: jest.fn(),
      },
      writable: true,
    });
  });

  describe('authApi', () => {
    test('login should return user data on success', async () => {
      const mockResponse = {
        access_token: 'test-token',
        user: {
          id: '1',
          username: 'admin',
          name: 'Test Admin',
          email: 'admin@test.com',
          role: 'admin'
        }
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      } as Response);

      const result = await authApi.login('admin', 'admin123');

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/auth/login',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ username: 'admin', password: 'admin123' }),
        })
      );

      expect(result.data).toEqual(mockResponse);
      expect(result.error).toBeUndefined();
    });

    test('login should return error on failure', async () => {
      const mockError = { error: 'Invalid credentials' };

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => mockError,
      } as Response);

      const result = await authApi.login('wrong', 'password');

      expect(result.data).toBeUndefined();
      expect(result.error).toBe('Invalid credentials');
    });

    test('getProfile should return user profile', async () => {
      const mockProfile = {
        user: {
          id: '1',
          username: 'admin',
          name: 'Test Admin',
          email: 'admin@test.com',
          role: 'admin'
        }
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockProfile,
      } as Response);

      const result = await authApi.getProfile();

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/auth/profile',
        expect.objectContaining({
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
        })
      );

      expect(result.data).toEqual(mockProfile);
    });

    test('isAuthenticated should return true when token exists', () => {
      (window.localStorage.getItem as jest.Mock).mockReturnValue('test-token');
      expect(authApi.isAuthenticated()).toBe(true);
    });

    test('isAuthenticated should return false when no token', () => {
      (window.localStorage.getItem as jest.Mock).mockReturnValue(null);
      expect(authApi.isAuthenticated()).toBe(false);
    });
  });

  describe('dashboardApi', () => {
    test('getStats should return dashboard statistics', async () => {
      const mockStats = {
        total_interactions: 1247,
        active_users: 89,
        happiness_level: 92,
        response_time: '0.3s',
        uptime: '15 days',
        skills_count: 4
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockStats,
      } as Response);

      const result = await dashboardApi.getStats();

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/dashboard/stats',
        expect.any(Object)
      );

      expect(result.data).toEqual(mockStats);
    });

    test('getInteractions should return interaction data', async () => {
      const mockData = {
        data: [
          { time: '09:00', تفاعلات: 12 },
          { time: '12:00', تفاعلات: 25 },
        ]
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockData,
      } as Response);

      const result = await dashboardApi.getInteractions();

      expect(result.data).toEqual(mockData);
    });
  });

  describe('emotionsApi', () => {
    test('getWeeklyData should return emotion data', async () => {
      const mockData = {
        data: [
          { name: 'الاثنين', سعادة: 80, قلق: 20, حياد: 30 },
          { name: 'الثلاثاء', سعادة: 65, قلق: 35, حياد: 25 },
        ]
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockData,
      } as Response);

      const result = await emotionsApi.getWeeklyData();

      expect(result.data).toEqual(mockData);
    });

    test('analyzeText should return emotion analysis', async () => {
      const mockAnalysis = {
        emotion: 'سعادة',
        confidence: 0.85,
        analysis: { status: 'success' }
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockAnalysis,
      } as Response);

      const result = await emotionsApi.analyzeText('أشعر بالسعادة');

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/emotions/analyze',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ text: 'أشعر بالسعادة' }),
        })
      );

      expect(result.data).toEqual(mockAnalysis);
    });
  });

  describe('chatApi', () => {
    test('sendMessage should return AI response', async () => {
      const mockResponse = {
        response: 'مرحباً! كيف يمكنني مساعدتك؟',
        mood: 'محايد',
        personality: {},
        timestamp: '2024-01-01T00:00:00.000Z'
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      } as Response);

      const result = await chatApi.sendMessage('مرحباً');

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/chat/message',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ message: 'مرحباً' }),
        })
      );

      expect(result.data).toEqual(mockResponse);
    });
  });

  describe('skillsApi', () => {
    test('getSkills should return skills data', async () => {
      const mockSkills = {
        skills: [
          { name: 'مستشعر التعاطف', status: 'نشط', performance: 95 },
          { name: 'الصداقة الرقمية', status: 'نشط', performance: 88 },
        ],
        performance: [
          { skill: 'التعاطف', فعالية: 95 },
          { skill: 'الصداقة الرقمية', فعالية: 88 },
        ]
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockSkills,
      } as Response);

      const result = await skillsApi.getSkills();

      expect(result.data).toEqual(mockSkills);
    });

    test('createSibling should return creation result', async () => {
      const mockResult = {
        success: true,
        sibling: { id: 'sibling_1', name: 'Digital Brother' },
        message: 'تم إنشاء الأخ الرقمي بنجاح!'
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResult,
      } as Response);

      const result = await skillsApi.createSibling({ specialty: 'programming' });

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:5000/api/skills/create-sibling',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ traits: { specialty: 'programming' } }),
        })
      );

      expect(result.data).toEqual(mockResult);
    });
  });

  describe('Error Handling', () => {
    test('should handle network errors', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network error'));

      const result = await authApi.login('admin', 'admin123');

      expect(result.error).toBe('فشل في الاتصال بالخادم');
      expect(result.data).toBeUndefined();
    });

    test('should handle 401 unauthorized errors', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => ({ error: 'Token expired' }),
      } as Response);

      // Mock window.location.href
      Object.defineProperty(window, 'location', {
        value: { href: '' },
        writable: true,
      });

      const result = await dashboardApi.getStats();

      expect(result.error).toBe('Token expired');
    });

    test('should handle server errors', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({ error: 'Internal server error' }),
      } as Response);

      const result = await dashboardApi.getStats();

      expect(result.error).toBe('Internal server error');
    });
  });
}); 