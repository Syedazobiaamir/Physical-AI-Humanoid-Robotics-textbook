import React, { ReactNode } from 'react';
import { useAuth } from './AuthContext';

interface ProtectedRouteProps {
  children: ReactNode;
  fallback?: ReactNode;
  requiredRole?: 'student' | 'author' | 'admin';
  onAuthRequired?: () => void;
}

export function ProtectedRoute({
  children,
  fallback,
  requiredRole,
  onAuthRequired,
}: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, user } = useAuth();

  if (isLoading) {
    return (
      <div className="protected-loading">
        <div className="loading-spinner" />
        <span>Loading...</span>

        <style>{`
          .protected-loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 3rem;
            gap: 1rem;
            color: var(--ifm-color-emphasis-600, #666);
          }

          .loading-spinner {
            width: 32px;
            height: 32px;
            border: 3px solid var(--ifm-color-emphasis-200, #eee);
            border-top-color: var(--ifm-color-primary, #2e8555);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
          }

          @keyframes spin {
            to { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  if (!isAuthenticated) {
    if (fallback) {
      return <>{fallback}</>;
    }

    return (
      <div className="auth-required">
        <div className="auth-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <rect width="18" height="11" x="3" y="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
          </svg>
        </div>
        <h3>Sign In Required</h3>
        <p>You need to be signed in to access this content.</p>
        <button className="signin-btn" onClick={onAuthRequired}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
            <polyline points="10 17 15 12 10 7" />
            <line x1="15" y1="12" x2="3" y2="12" />
          </svg>
          Sign In
        </button>

        <style>{`
          .auth-required {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 3rem;
            text-align: center;
            background: var(--ifm-color-emphasis-100, #f9f9f9);
            border-radius: 16px;
            margin: 1rem 0;
          }

          .auth-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 80px;
            height: 80px;
            background: var(--ifm-color-emphasis-200, #eee);
            border-radius: 50%;
            margin-bottom: 1.5rem;
            color: var(--ifm-color-emphasis-600, #666);
          }

          .auth-required h3 {
            margin: 0 0 0.5rem 0;
            font-size: 1.25rem;
            color: var(--ifm-font-color-base, #333);
          }

          .auth-required p {
            margin: 0 0 1.5rem 0;
            color: var(--ifm-color-emphasis-600, #666);
          }

          .signin-btn {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            background: var(--ifm-color-primary, #2e8555);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.95rem;
            font-weight: 500;
            transition: all 0.2s;
          }

          .signin-btn:hover {
            background: var(--ifm-color-primary-dark, #257347);
          }
        `}</style>
      </div>
    );
  }

  // Check role if required
  if (requiredRole && user) {
    const roleHierarchy = { student: 0, author: 1, admin: 2 };
    const userLevel = roleHierarchy[user.role] ?? 0;
    const requiredLevel = roleHierarchy[requiredRole] ?? 0;

    if (userLevel < requiredLevel) {
      return (
        <div className="role-required">
          <div className="role-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
          </div>
          <h3>Access Restricted</h3>
          <p>This content requires {requiredRole} access or higher.</p>

          <style>{`
            .role-required {
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: center;
              padding: 3rem;
              text-align: center;
              background: #fef3c7;
              border: 1px solid #fde68a;
              border-radius: 16px;
              margin: 1rem 0;
            }

            .role-icon {
              display: flex;
              align-items: center;
              justify-content: center;
              width: 80px;
              height: 80px;
              background: #fde68a;
              border-radius: 50%;
              margin-bottom: 1.5rem;
              color: #92400e;
            }

            .role-required h3 {
              margin: 0 0 0.5rem 0;
              font-size: 1.25rem;
              color: #92400e;
            }

            .role-required p {
              margin: 0;
              color: #a16207;
            }
          `}</style>
        </div>
      );
    }
  }

  return <>{children}</>;
}

export default ProtectedRoute;
