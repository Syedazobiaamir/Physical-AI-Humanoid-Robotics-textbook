/**
 * API Configuration
 *
 * This file manages the backend API URL configuration.
 *
 * For local development:
 *   - The default URL points to localhost:8000
 *
 * For production:
 *   - Set DOCUSAURUS_API_BASE_URL environment variable in Vercel dashboard
 *   - Or update PRODUCTION_API_URL below after deploying your backend
 *
 * Deployment options for backend:
 *   - Vercel: https://vercel.com (recommended - same platform as frontend)
 *   - Railway: https://railway.app (alternative)
 *   - Render: https://render.com (free tier available)
 *
 * To deploy backend on Vercel:
 *   1. Go to Vercel Dashboard > Add New Project
 *   2. Import your GitHub repo
 *   3. Set Root Directory to "backend"
 *   4. Deploy - Vercel will auto-detect FastAPI
 *   5. Copy the deployment URL (e.g., https://your-backend.vercel.app)
 *   6. In frontend Vercel project, add env var:
 *      DOCUSAURUS_API_BASE_URL = https://your-backend.vercel.app/api/v1
 *   7. Redeploy frontend
 */

// Production backend URL (for monorepo, use relative path)
const PRODUCTION_API_URL = 'https://backend-nine-omega-60.vercel.app/api/v1';

// Local development URL
const DEVELOPMENT_API_URL = 'http://localhost:8000/api/v1';

// Determine if we're in production (on Vercel or other hosts)
const isProduction = typeof window !== 'undefined' &&
  !window.location.hostname.includes('localhost') &&
  !window.location.hostname.includes('127.0.0.1');

// Get the API base URL
// In production, use the deployed Vercel backend; locally use localhost
export const API_BASE_URL = isProduction ? PRODUCTION_API_URL : DEVELOPMENT_API_URL;

// Hook to get API URL within React components (preferred method)
export function useApiUrl(): string {
  return API_BASE_URL;
}

// Helper to construct full API URLs
export const apiUrl = (path: string): string => {
  const base = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${base}${cleanPath}`;
};

export default API_BASE_URL;
