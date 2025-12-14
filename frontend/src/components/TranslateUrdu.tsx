import React, { useState, useCallback, useEffect } from 'react';
import API_BASE_URL from '@site/src/config/api';

interface TranslateUrduProps {
  chapterId?: string;
}

const TranslateUrdu: React.FC<TranslateUrduProps> = ({ chapterId }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [urduContent, setUrduContent] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);

  // Get the chapter content from the page
  const getChapterContent = useCallback(() => {
    const articleElement = document.querySelector('article.markdown');
    if (articleElement) {
      return articleElement.textContent || '';
    }
    return '';
  }, []);

  const translateContent = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const content = getChapterContent();
      if (!content.trim()) {
        setError('No content found to translate');
        setIsLoading(false);
        return;
      }

      const response = await fetch(`${API_BASE_URL}/translation/urdu`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: content.substring(0, 10000), // Limit content size
          content_type: 'markdown',
          preserve_formatting: true,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setUrduContent(data.urdu_content);
        setIsExpanded(true);
      } else {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Translation failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to translate. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTranslateClick = () => {
    if (urduContent && isExpanded) {
      setIsExpanded(false);
    } else if (urduContent) {
      setIsExpanded(true);
    } else {
      translateContent();
    }
  };

  const handleRefresh = () => {
    translateContent();
  };

  const copyToClipboard = async () => {
    if (urduContent) {
      try {
        await navigator.clipboard.writeText(urduContent);
      } catch {
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
            <span className="urdu-label">Translate to Urdu</span>
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
              اردو ترجمہ (Urdu Translation)
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
          position: fixed;
          bottom: 100px;
          right: 24px;
          z-index: 999;
        }

        .translate-urdu-button {
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1.25rem;
          background: linear-gradient(135deg, #047857, #065f46);
          color: white;
          border: none;
          border-radius: 24px;
          cursor: pointer;
          font-size: 0.9rem;
          font-weight: 500;
          transition: all 0.3s ease;
          box-shadow: 0 4px 15px rgba(4, 120, 87, 0.4);
        }

        .translate-urdu-button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(4, 120, 87, 0.5);
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
          opacity: 0.9;
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
          position: fixed;
          bottom: 160px;
          right: 24px;
          width: 400px;
          max-width: calc(100vw - 48px);
          max-height: 60vh;
          background: var(--ifm-background-color, #fff);
          border: 1px solid var(--ifm-color-emphasis-200, #e5e5e5);
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
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

        .urdu-panel-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem 1.25rem;
          background: linear-gradient(135deg, #047857, #065f46);
          color: white;
        }

        .urdu-panel-header h4 {
          margin: 0;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 1rem;
          font-weight: 600;
        }

        .urdu-panel-actions {
          display: flex;
          gap: 0.5rem;
        }

        .action-btn {
          background: rgba(255, 255, 255, 0.2);
          border: none;
          border-radius: 8px;
          padding: 0.5rem;
          cursor: pointer;
          color: white;
          transition: background 0.2s;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .action-btn:hover:not(:disabled) {
          background: rgba(255, 255, 255, 0.3);
        }

        .action-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .urdu-content {
          padding: 1.5rem;
          font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', serif;
          font-size: 1.1rem;
          line-height: 2.2;
          color: var(--ifm-font-color-base, #333);
          text-align: right;
          white-space: pre-wrap;
          max-height: calc(60vh - 60px);
          overflow-y: auto;
        }

        .error-message {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-top: 0.75rem;
          padding: 0.75rem 1rem;
          background: #fee2e2;
          color: #dc2626;
          border-radius: 12px;
          font-size: 0.875rem;
          position: fixed;
          bottom: 160px;
          right: 24px;
        }

        @media (max-width: 768px) {
          .translate-urdu-container {
            bottom: 90px;
            right: 16px;
          }

          .translate-urdu-button {
            padding: 0.625rem 1rem;
            font-size: 0.85rem;
          }

          .urdu-label {
            display: none;
          }

          .urdu-content-panel {
            bottom: 150px;
            right: 16px;
            width: calc(100vw - 32px);
          }
        }

        [data-theme='dark'] .urdu-content-panel {
          background: var(--ifm-background-color);
          border-color: rgba(255, 255, 255, 0.1);
        }

        [data-theme='dark'] .urdu-content {
          color: var(--ifm-font-color-base);
        }

        [data-theme='dark'] .error-message {
          background: rgba(220, 38, 38, 0.2);
          color: #fca5a5;
        }
      `}</style>
    </div>
  );
};

export default TranslateUrdu;
