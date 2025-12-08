/**
 * Authentication service for JWT handling and OAuth flow
 */

const API_URL = 'http://localhost:8000';

// Token storage keys
const ACCESS_TOKEN_KEY = 'physical_ai_access_token';
const REFRESH_TOKEN_KEY = 'physical_ai_refresh_token';
const USER_KEY = 'physical_ai_user';

/**
 * Store tokens in localStorage
 */
export const storeTokens = (accessToken, refreshToken) => {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  if (refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }
};

/**
 * Store user data in localStorage
 */
export const storeUser = (user) => {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
};

/**
 * Get access token from storage
 */
export const getAccessToken = () => {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
};

/**
 * Get refresh token from storage
 */
export const getRefreshToken = () => {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

/**
 * Get stored user data
 */
export const getStoredUser = () => {
  const userData = localStorage.getItem(USER_KEY);
  return userData ? JSON.parse(userData) : null;
};

/**
 * Clear all auth data from storage
 */
export const clearAuth = () => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  const token = getAccessToken();
  if (!token) return false;

  // Check if token is expired by decoding it
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const expirationTime = payload.exp * 1000;
    return Date.now() < expirationTime;
  } catch {
    return false;
  }
};

/**
 * Check if access token is about to expire (within 5 minutes)
 */
export const isTokenExpiringSoon = () => {
  const token = getAccessToken();
  if (!token) return true;

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const expirationTime = payload.exp * 1000;
    const fiveMinutes = 5 * 60 * 1000;
    return Date.now() > expirationTime - fiveMinutes;
  } catch {
    return true;
  }
};

/**
 * Initiate OAuth login flow
 * @param {string} provider - OAuth provider ('google' or 'github')
 * @param {string} redirectUri - URI to redirect to after OAuth
 * @returns {Promise<string>} OAuth authorization URL
 */
export const initiateOAuthLogin = async (provider, redirectUri) => {
  const response = await fetch(`${API_URL}/api/v1/auth/login/oauth`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      provider,
      redirect_uri: redirectUri,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to initiate OAuth login');
  }

  const data = await response.json();
  return data.auth_url;
};

/**
 * Handle OAuth callback
 * @param {string} code - Authorization code from OAuth provider
 * @param {string} provider - OAuth provider
 * @param {string} redirectUri - Original redirect URI
 * @returns {Promise<Object>} User data and tokens
 */
export const handleOAuthCallback = async (code, provider, redirectUri) => {
  const response = await fetch(`${API_URL}/api/v1/auth/login/callback`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      code,
      provider,
      redirect_uri: redirectUri,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Authentication failed');
  }

  const data = await response.json();

  // Store tokens and user
  storeTokens(data.access_token, data.refresh_token);
  storeUser(data.user);

  return data;
};

/**
 * Refresh access token using refresh token
 * @returns {Promise<string>} New access token
 */
export const refreshAccessToken = async () => {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  const response = await fetch(`${API_URL}/api/v1/auth/refresh`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      refresh_token: refreshToken,
    }),
  });

  if (!response.ok) {
    // Clear auth data if refresh fails
    clearAuth();
    throw new Error('Token refresh failed');
  }

  const data = await response.json();
  storeTokens(data.access_token, refreshToken);

  return data.access_token;
};

/**
 * Make authenticated API request with automatic token refresh
 * @param {string} url - API endpoint URL
 * @param {Object} options - Fetch options
 * @returns {Promise<Response>} Fetch response
 */
export const authenticatedFetch = async (url, options = {}) => {
  // Check if token needs refresh
  if (isTokenExpiringSoon()) {
    try {
      await refreshAccessToken();
    } catch {
      // If refresh fails, continue with current token
      // The request might fail, which is expected
    }
  }

  const token = getAccessToken();

  const headers = {
    ...options.headers,
    ...(token && { Authorization: `Bearer ${token}` }),
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  // If unauthorized, try to refresh token and retry once
  if (response.status === 401) {
    try {
      await refreshAccessToken();
      const newToken = getAccessToken();

      return fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          Authorization: `Bearer ${newToken}`,
        },
      });
    } catch {
      // Refresh failed, return original response
      return response;
    }
  }

  return response;
};

/**
 * Logout user by clearing all auth data
 */
export const logout = () => {
  clearAuth();
  // Optionally redirect to home page
  if (typeof window !== 'undefined') {
    window.location.href = '/';
  }
};

/**
 * Get current user from token payload
 * @returns {Object|null} User payload or null
 */
export const getCurrentUser = () => {
  const token = getAccessToken();
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return {
      id: payload.sub,
      email: payload.email,
      name: payload.name,
      role: payload.role,
    };
  } catch {
    return null;
  }
};

export default {
  storeTokens,
  storeUser,
  getAccessToken,
  getRefreshToken,
  getStoredUser,
  clearAuth,
  isAuthenticated,
  isTokenExpiringSoon,
  initiateOAuthLogin,
  handleOAuthCallback,
  refreshAccessToken,
  authenticatedFetch,
  logout,
  getCurrentUser,
};
