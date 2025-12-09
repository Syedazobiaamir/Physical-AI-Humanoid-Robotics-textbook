/**
 * API Configuration
 *
 * This file manages the backend API URL configuration.
 *
 * For local development:
 *   - The default URL points to localhost:8000
 *
 * For production:
 *   - Update docusaurus.config.ts customFields.apiBaseUrl
 *   - Or deploy backend and update the URL here
 *
 * Deployment options for backend:
 *   - Railway: https://railway.app (recommended for quick setup)
 *   - Render: https://render.com (free tier available)
 *   - Fly.io: https://fly.io (generous free tier)
 */

// Production backend URL - UPDATE THIS after deploying your backend
// Example: 'https://your-backend-app.railway.app/api/v1'
const PRODUCTION_API_URL = '';

// Local development URL
const DEVELOPMENT_API_URL = 'http://localhost:8000/api/v1';

// Determine if we're in production (on Vercel or other hosts)
const isProduction = typeof window !== 'undefined' &&
  !window.location.hostname.includes('localhost') &&
  !window.location.hostname.includes('127.0.0.1');

// Get the API base URL
export const API_BASE_URL = isProduction && PRODUCTION_API_URL
  ? PRODUCTION_API_URL
  : DEVELOPMENT_API_URL;

// Helper to construct full API URLs
export const apiUrl = (path: string): string => {
  const base = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${base}${cleanPath}`;
};

export default API_BASE_URL;
