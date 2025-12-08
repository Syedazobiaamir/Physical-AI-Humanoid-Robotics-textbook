import React, { useState } from 'react';
import { useAuth } from './AuthContext';

interface SignInProps {
  isOpen: boolean;
  onClose: () => void;
  onSignUpClick?: () => void;
}

export function SignIn({ isOpen, onClose, onSignUpClick }: SignInProps) {
  const { login, isLoading, error, clearError } = useAuth();
  const [selectedProvider, setSelectedProvider] = useState<'google' | 'github' | null>(null);

  if (!isOpen) return null;

  const handleLogin = async (provider: 'google' | 'github') => {
    setSelectedProvider(provider);
    await login(provider);
  };

  const handleClose = () => {
    clearError();
    onClose();
  };

  return (
    <div className="signin-overlay" onClick={handleClose}>
      <div className="signin-modal" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={handleClose} aria-label="Close">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        <div className="signin-header">
          <div className="logo-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 6v6l4 2" />
            </svg>
          </div>
          <h2>Welcome Back</h2>
          <p>Sign in to access personalized learning features</p>
        </div>

        {error && (
          <div className="error-banner">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            <span>{error}</span>
          </div>
        )}

        <div className="signin-buttons">
          <button
            className="oauth-btn google-btn"
            onClick={() => handleLogin('google')}
            disabled={isLoading}
          >
            {isLoading && selectedProvider === 'google' ? (
              <span className="spinner" />
            ) : (
              <svg width="20" height="20" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
            )}
            <span>Continue with Google</span>
          </button>

          <button
            className="oauth-btn github-btn"
            onClick={() => handleLogin('github')}
            disabled={isLoading}
          >
            {isLoading && selectedProvider === 'github' ? (
              <span className="spinner" />
            ) : (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
              </svg>
            )}
            <span>Continue with GitHub</span>
          </button>
        </div>

        <div className="signin-footer">
          <p>
            New to Physical AI Textbook?{' '}
            <button className="link-btn" onClick={onSignUpClick}>
              Learn more
            </button>
          </p>
        </div>
      </div>

      <style>{`
        .signin-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.6);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
          padding: 1rem;
          backdrop-filter: blur(4px);
        }

        .signin-modal {
          background: var(--ifm-background-color, #fff);
          border-radius: 20px;
          width: 100%;
          max-width: 400px;
          padding: 2rem;
          position: relative;
          box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
          animation: slideUp 0.3s ease-out;
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .close-btn {
          position: absolute;
          top: 1rem;
          right: 1rem;
          background: transparent;
          border: none;
          cursor: pointer;
          padding: 0.5rem;
          color: var(--ifm-color-emphasis-500, #888);
          transition: color 0.2s;
          border-radius: 8px;
        }

        .close-btn:hover {
          color: var(--ifm-font-color-base, #333);
          background: var(--ifm-color-emphasis-100, #f5f5f5);
        }

        .signin-header {
          text-align: center;
          margin-bottom: 1.5rem;
        }

        .logo-icon {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 64px;
          height: 64px;
          background: linear-gradient(135deg, var(--ifm-color-primary, #2e8555), var(--ifm-color-primary-dark, #257347));
          border-radius: 16px;
          color: white;
          margin-bottom: 1rem;
        }

        .signin-header h2 {
          margin: 0 0 0.5rem 0;
          font-size: 1.5rem;
          color: var(--ifm-font-color-base, #333);
        }

        .signin-header p {
          margin: 0;
          color: var(--ifm-color-emphasis-600, #666);
          font-size: 0.9rem;
        }

        .error-banner {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 0.875rem 1rem;
          background: #fee2e2;
          border: 1px solid #fecaca;
          border-radius: 10px;
          color: #dc2626;
          margin-bottom: 1.5rem;
          font-size: 0.875rem;
        }

        .signin-buttons {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .oauth-btn {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.75rem;
          width: 100%;
          padding: 0.875rem 1.25rem;
          border-radius: 10px;
          font-size: 0.95rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
          border: 2px solid transparent;
        }

        .oauth-btn:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }

        .google-btn {
          background: #fff;
          border-color: var(--ifm-color-emphasis-300, #ddd);
          color: var(--ifm-font-color-base, #333);
        }

        .google-btn:hover:not(:disabled) {
          background: var(--ifm-color-emphasis-100, #f9f9f9);
          border-color: var(--ifm-color-emphasis-400, #ccc);
        }

        .github-btn {
          background: #24292f;
          color: #fff;
        }

        .github-btn:hover:not(:disabled) {
          background: #32383f;
        }

        .spinner {
          width: 20px;
          height: 20px;
          border: 2px solid currentColor;
          border-top-color: transparent;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        .signin-footer {
          margin-top: 1.5rem;
          text-align: center;
          padding-top: 1.5rem;
          border-top: 1px solid var(--ifm-color-emphasis-200, #eee);
        }

        .signin-footer p {
          margin: 0;
          color: var(--ifm-color-emphasis-600, #666);
          font-size: 0.875rem;
        }

        .link-btn {
          background: none;
          border: none;
          color: var(--ifm-color-primary, #2e8555);
          cursor: pointer;
          font-weight: 500;
          padding: 0;
        }

        .link-btn:hover {
          text-decoration: underline;
        }

        @media (max-width: 480px) {
          .signin-modal {
            padding: 1.5rem;
          }
        }
      `}</style>
    </div>
  );
}

export default SignIn;
