import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '../hooks/use-auth';
import { authApi } from '../lib/api';

// Mock the API calls
jest.mock('../lib/api', () => ({
  authApi: {
    login: jest.fn(),
    getProfile: jest.fn(),
    logout: jest.fn(),
    isAuthenticated: jest.fn(),
  },
}));

describe('Authentication', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should login successfully', async () => {
    const mockUser = { id: 1, username: 'test', name: 'Test User' };
    (authApi.login as jest.Mock).mockResolvedValueOnce({ data: { user: mockUser } });

    render(
      <AuthProvider>
        <LoginForm />
      </AuthProvider>
    );

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'test' },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' },
    });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(authApi.login).toHaveBeenCalledWith('test', 'password123');
    });
  });

  test('should handle login errors', async () => {
    (authApi.login as jest.Mock).mockRejectedValueOnce(new Error('Invalid credentials'));

    render(
      <AuthProvider>
        <LoginForm />
      </AuthProvider>
    );

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'test' },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'wrong' },
    });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });
  });
}); 