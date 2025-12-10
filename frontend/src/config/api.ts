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

import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

// Local development URL
const DEVELOPMENT_API_URL = 'http://localhost:8000/api/v1';

// Determine if we're in production (on Vercel or other hosts)
const isProduction = typeof window !== 'undefined' &&
  !window.location.hostname.includes('localhost') &&
  !window.location.hostname.includes('127.0.0.1');

// Get API URL from Docusaurus config (set via env var or hardcoded)
// This is evaluated at build time
let configApiUrl = '';
try {
  // This will be set from docusaurus.config.ts customFields
  // Access it safely since this file might be loaded before Docusaurus context
  if (typeof window !== 'undefined' && (window as any).__DOCUSAURUS__) {
    configApiUrl = (window as any).__DOCUSAURUS__?.siteConfig?.customFields?.apiBaseUrl || '';
  }
} catch {
  // Ignore errors during SSR or before Docusaurus is ready
}

// Get the API base URL
// Priority: 1) Docusaurus config, 2) Development URL
export const API_BASE_URL = (() => {
  // In production, use configured URL
  if (isProduction && configApiUrl) {
    return configApiUrl;
  }
  return DEVELOPMENT_API_URL;
})();

// Hook to get API URL within React components (preferred method)
export function useApiUrl(): string {
  try {
    const { siteConfig } = useDocusaurusContext();
    const apiUrl = siteConfig?.customFields?.apiBaseUrl as string;
    if (isProduction && apiUrl) {
      return apiUrl;
    }
  } catch {
    // Outside of React context or Docusaurus not ready
  }
  return DEVELOPMENT_API_URL;
}

// Helper to construct full API URLs
export const apiUrl = (path: string): string => {
  const base = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${base}${cleanPath}`;
};

export default API_BASE_URL;
