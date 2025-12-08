/**
 * API Configuration
 *
 * Centralized API URL configuration for the frontend.
 * In Docusaurus/browser environment, we can't use process.env directly,
 * so we use a constant that can be configured during build.
 */

// Default API URL for development
// For production, this should be updated to the production API URL
export const API_BASE_URL = 'http://localhost:8000';

// API v1 endpoint
export const API_V1_URL = `${API_BASE_URL}/api/v1`;

// Helper function to get full API URL
export function getApiUrl(path: string): string {
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${API_V1_URL}${cleanPath}`;
}

export default {
  API_BASE_URL,
  API_V1_URL,
  getApiUrl,
};
