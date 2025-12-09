import React, { useState, useCallback } from 'react';
import API_BASE_URL from '@site/src/config/api';

interface TranslateUrduProps {
  chapterId: string;
  onTranslationComplete?: (urduContent: string) => void;
}

const TranslateUrdu: React.FC<TranslateUrduProps> = ({
  chapterId,
  onTranslationComplete,
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [urduContent, setUrduContent] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  const getToken = useCallback(() => {
    return localStorage.getItem('physical_ai_access_token');
  }, []);

  const fetchTranslation = async (forceRefresh: boolean = false) => {
    setIsLoading(true);
    setError(null);

    try {
      const token = getToken();
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const endpoint = forceRefresh
        ? `${API_BASE_URL}/translation/urdu/${chapterId}/refresh`
        : `${API_BASE_URL}/translation/urdu/${chapterId}`;

      const response = await fetch(endpoint, {
        method: forceRefresh ? 'POST' : 'GET',
        headers,
      });

      if (response.ok) {
        const data = await response.json();
        setUrduContent(data.urdu_content);
        setLastUpdated(data.last_updated);
        setIsExpanded(true);

        if (onTranslationComplete) {
          onTranslationComplete(data.urdu_content);
        }
      } else if (response.status === 404) {
        setError('Chapter not found');
      } else {
        throw new Error('Translation failed');
      }
    } catch (err) {
      setError('Failed to load Urdu translation. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTranslateClick = () => {
    if (urduContent && isExpanded) {
      // Toggle off
      setIsExpanded(false);
    } else if (urduContent) {
      // Show existing translation
      setIsExpanded(true);
    } else {
      // Fetch new translation
      fetchTranslation();
    }
  };

  const handleRefresh = () => {
    fetchTranslation(true);
  };

  const copyToClipboard = async () => {
    if (urduContent) {
      try {
        await navigator.clipboard.writeText(urduContent);
      } catch {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = urduContent;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
      }
    }
  };

  return (
    <div className="translate-urdu-container">
      <button
        className={`translate-urdu-button ${isExpanded ? 'active' : ''}`}
        onClick={handleTranslateClick}
        disabled={isLoading}
        title="Translate to Urdu"
      >
        {isLoading ? (
          <>
            <span className="spinner"></span>
            <span>Translating...</span>
          </>
        ) : (
          <>
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="m5 8 6 6" />
              <path d="m4 14 6-6 2-3" />
              <path d="M2 5h12" />
              <path d="M7 2h1" />
              <path d="m22 22-5-10-5 10" />
              <path d="M14 18h6" />
            </svg>
            <span>اردو</span>
            <span className="urdu-label">Urdu</span>
          </>
        )}
      </button>

      {isExpanded && urduContent && (
        <div className="urdu-content-panel">
          <div className="urdu-panel-header">
            <h4>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="m5 8 6 6" />
                <path d="m4 14 6-6 2-3" />
                <path d="M2 5h12" />
                <path d="M7 2h1" />
              </svg>
              اردو ترجمہ
            </h4>
            <div className="urdu-panel-actions">
              <button
                className="action-btn"
                onClick={copyToClipboard}
                title="Copy translation"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect width="14" height="14" x="8" y="8" rx="2" ry="2" />
                  <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />
                </svg>
              </button>
              <button
                className="action-btn"
                onClick={handleRefresh}
                disabled={isLoading}
                title="Refresh translation"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" />
                  <path d="M21 3v5h-5" />
                  <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" />
                  <path d="M8 16H3v5" />
                </svg>
              </button>
              <button
                className="action-btn close-btn"
                onClick={() => setIsExpanded(false)}
                title="Close"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
          </div>

          {lastUpdated && (
            <div className="translation-meta">
              Last updated: {new Date(lastUpdated).toLocaleDateString()}
            </div>
          )}

          <div className="urdu-content" dir="rtl" lang="ur">
            {urduContent}
          </div>
        </div>
      )}

      {error && (
        <div className="error-message">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          {error}
        </div>
      )}

      <style>{`
        .translate-urdu-container {
          position: relative;
          margin: 1rem 0;
        }

        .translate-urdu-button {
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.5rem 1rem;
          background: linear-gradient(135deg, #047857, #065f46);
          color: white;
          border: none;
          border-radius: 20px;
          cursor: pointer;
          font-size: 0.875rem;
          font-weight: 500;
          transition: all 0.2s;
          box-shadow: 0 2px 8px rgba(4, 120, 87, 0.3);
        }

        .translate-urdu-button:hover:not(:disabled) {
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(4, 120, 87, 0.4);
        }

        .translate-urdu-button.active {
          background: linear-gradient(135deg, #065f46, #047857);
        }

        .translate-urdu-button:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }

        .urdu-label {
          font-size: 0.75rem;
          opacity: 0.8;
        }

        .spinner {
          width: 16px;
          height: 16px;
          border: 2px solid rgba(255, 255, 255, 0.3);
          border-top-color: white;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }

        .urdu-content-panel {
          margin-top: 1rem;
          background: var(--ifm-background-color, #fff);
          border: 1px solid var(--ifm-color-emphasis-200, #e5e5e5);
          border-radius: 12px;
          overflow: hidden;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        .urdu-panel-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.875rem 1rem;
          background: linear-gradient(135deg, #047857, #065f46);
          color: white;
        }

        .urdu-panel-header h4 {
          margin: 0;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 1rem;
          font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', serif;
        }

        .urdu-panel-actions {
          display: flex;
          gap: 0.5rem;
        }

        .action-btn {
          background: rgba(255, 255, 255, 0.2);
          border: none;
          border-radius: 6px;
          padding: 0.375rem;
          cursor: pointer;
          color: white;
          transition: background 0.2s;
        }

        .action-btn:hover:not(:disabled) {
          background: rgba(255, 255, 255, 0.3);
        }

        .action-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .translation-meta {
          padding: 0.5rem 1rem;
          background: var(--ifm-color-emphasis-100, #f5f5f5);
          font-size: 0.75rem;
          color: var(--ifm-color-emphasis-600, #666);
          border-bottom: 1px solid var(--ifm-color-emphasis-200, #e5e5e5);
        }

        .urdu-content {
          padding: 1.5rem;
          font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', 'Urdu Typesetting', serif;
          font-size: 1.1rem;
          line-height: 2.2;
          color: var(--ifm-font-color-base, #333);
          text-align: right;
          white-space: pre-wrap;
        }

        .urdu-content code {
          direction: ltr;
          unicode-bidi: embed;
          font-family: monospace;
          background: var(--ifm-color-emphasis-100, #f5f5f5);
          padding: 0.125rem 0.375rem;
          border-radius: 4px;
        }

        .urdu-content pre {
          direction: ltr;
          text-align: left;
          background: var(--ifm-color-emphasis-100, #f5f5f5);
          padding: 1rem;
          border-radius: 8px;
          overflow-x: auto;
        }

        .error-message {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-top: 0.75rem;
          padding: 0.75rem;
          background: #f8d7da;
          color: #842029;
          border-radius: 8px;
          font-size: 0.875rem;
        }

        @media (max-width: 768px) {
          .urdu-content {
            padding: 1rem;
            font-size: 1rem;
            line-height: 2;
          }

          .urdu-panel-header {
            flex-direction: column;
            gap: 0.75rem;
          }
        }
      `}</style>
    </div>
  );
};

export default TranslateUrdu;
