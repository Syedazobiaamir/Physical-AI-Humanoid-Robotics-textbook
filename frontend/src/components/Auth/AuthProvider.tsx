import React, { useState, useEffect, useCallback, ReactNode } from 'react';
import { AuthContext, User } from './AuthContext';
import API_BASE_URL from '@site/src/config/api';

const TOKEN_KEY = 'physical_ai_access_token';
const REFRESH_TOKEN_KEY = 'physical_ai_refresh_token';
const USER_KEY = 'physical_ai_user';

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Check if token is valid
  const isTokenValid = useCallback((token: string): boolean => {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return Date.now() < payload.exp * 1000;
    } catch {
      return false;
    }
  }, []);

  // Initialize auth state from localStorage
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem(TOKEN_KEY);
      const storedUser = localStorage.getItem(USER_KEY);

      if (token && storedUser) {
        if (isTokenValid(token)) {
          setUser(JSON.parse(storedUser));
        } else {
          // Try to refresh token
          const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
          if (refreshToken) {
            try {
              await refreshAccessToken(refreshToken);
            } catch {
              // Clear invalid tokens
              localStorage.removeItem(TOKEN_KEY);
              localStorage.removeItem(REFRESH_TOKEN_KEY);
              localStorage.removeItem(USER_KEY);
            }
          }
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, [isTokenValid]);

  // Refresh access token
  const refreshAccessToken = async (refreshToken: string) => {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem(TOKEN_KEY, data.access_token);
      return data.access_token;
    }
    throw new Error('Failed to refresh token');
  };

  // Initiate OAuth login
  const login = async (provider: 'google' | 'github') => {
    setIsLoading(true);
    setError(null);

    try {
      const redirectUri = `${window.location.origin}/auth/callback`;

      const response = await fetch(`${API_BASE_URL}/auth/login/oauth`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider,
          redirect_uri: redirectUri,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        // Store provider for callback
        sessionStorage.setItem('oauth_provider', provider);
        sessionStorage.setItem('oauth_redirect_uri', redirectUri);
        // Redirect to OAuth provider
        window.location.href = data.auth_url;
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail?.message || 'Failed to initiate login');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
      setIsLoading(false);
    }
  };

  // Handle OAuth callback
  const handleOAuthCallback = async (code: string, provider: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const redirectUri = sessionStorage.getItem('oauth_redirect_uri') ||
        `${window.location.origin}/auth/callback`;

      const response = await fetch(`${API_BASE_URL}/auth/login/callback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code,
          provider,
          redirect_uri: redirectUri,
        }),
      });

      if (response.ok) {
        const data = await response.json();

        // Store tokens and user
        localStorage.setItem(TOKEN_KEY, data.access_token);
        localStorage.setItem(REFRESH_TOKEN_KEY, data.refresh_token);
        localStorage.setItem(USER_KEY, JSON.stringify(data.user));

        setUser(data.user);

        // Clean up session storage
        sessionStorage.removeItem('oauth_provider');
        sessionStorage.removeItem('oauth_redirect_uri');
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail?.message || 'Authentication failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Authentication failed');
    } finally {
      setIsLoading(false);
    }
  };

  // Logout
  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    setUser(null);
    setError(null);
  }, []);

  // Update user profile
  const updateProfile = async (updates: Partial<User>) => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token || !user) {
      throw new Error('Not authenticated');
    }

    // For now, just update locally (backend endpoint would be needed for full implementation)
    const updatedUser = { ...user, ...updates };
    localStorage.setItem(USER_KEY, JSON.stringify(updatedUser));
    setUser(updatedUser);
  };

  // Clear error
  const clearError = () => setError(null);

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    error,
    login,
    logout,
    handleOAuthCallback,
    updateProfile,
    clearError,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
