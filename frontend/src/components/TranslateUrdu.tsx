import React, { useState, useCallback } from 'react';
import API_BASE_URL from '@site/src/config/api';

interface TranslateUrduProps {
  chapterId?: string;
}

const TranslateUrdu: React.FC<TranslateUrduProps> = ({ chapterId }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [urduContent, setUrduContent] = useState<string | null>(null);
  const [showTranslation, setShowTranslation] = useState(false);

  // Get the chapter content from the page
  const getChapterContent = useCallback(() => {
    // Try multiple selectors that Docusaurus uses
    const selectors = [
      'article.markdown',
      '.theme-doc-markdown',
      'article[class*="docItemContainer"]',
      '.markdown',
      'article',
      '[class*="docItemCol"] .markdown',
      'main article',
      '.docMainContainer article'
    ];

    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element && element.textContent?.trim()) {
        // Get text content - increased limit for full chapters
        const text = element.textContent || '';
        console.log(`Found content using selector: ${selector}, length: ${text.length}`);
        // Limit to 50000 characters (approximately 10-15 pages of content)
        return text.substring(0, 50000);
      }
    }

    console.log('No content found with any selector');
    return '';
  }, []);

  const translateContent = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Wait a moment for content to render if needed
      let content = getChapterContent();

      // Retry after a short delay if no content found
      if (!content.trim()) {
        await new Promise(resolve => setTimeout(resolve, 500));
        content = getChapterContent();
      }

      if (!content.trim()) {
        setError('ترجمہ کے لیے مواد نہیں ملا۔ براہ کرم صفحہ مکمل لوڈ ہونے کا انتظار کریں اور دوبارہ کوشش کریں۔');
        setIsLoading(false);
        return;
      }

      console.log('Translating content, length:', content.length);

      const response = await fetch(`${API_BASE_URL}/translation/urdu`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: content,
          content_type: 'text',
          preserve_formatting: true,
        }),
      });

      console.log('Response status:', response.status);

      if (response.ok) {
        const data = await response.json();
        console.log('Translation received:', data);
        setUrduContent(data.urdu_content);
        setShowTranslation(true);
      } else {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        console.error('Translation error:', errorData);
        throw new Error(errorData.detail || 'Translation failed');
      }
    } catch (err) {
      console.error('Translation error:', err);
      setError(err instanceof Error ? err.message : 'ترجمہ ناکام ہوگیا۔ براہ کرم دوبارہ کوشش کریں۔');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTranslateClick = () => {
    if (showTranslation) {
      setShowTranslation(false);
    } else if (urduContent) {
      setShowTranslation(true);
    } else {
      translateContent();
    }
  };

  return (
    <div className="translate-urdu-wrapper">
      {/* Translate Button */}
      <button
        className={`translate-btn ${showTranslation ? 'active' : ''}`}
        onClick={handleTranslateClick}
        disabled={isLoading}
        aria-label={showTranslation ? "اصل انگریزی مواد دکھائیں" : "اردو میں ترجمہ کریں"}
        aria-expanded={showTranslation}
        aria-busy={isLoading}
      >
        {isLoading ? (
          <>
            <span className="spinner"></span>
            <span>اردو میں ترجمہ ہو رہا ہے... براہ کرم انتظار کریں</span>
          </>
        ) : showTranslation ? (
          <>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M3 12h18M3 6h18M3 18h18"/>
            </svg>
            <span>اصل مواد دکھائیں</span>
          </>
        ) : (
          <>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="m5 8 6 6M4 14l6-6 2-3M2 5h12M7 2h1M22 22l-5-10-5 10M14 18h6"/>
            </svg>
            <span>اردو میں ترجمہ کریں</span>
          </>
        )}
      </button>

      {/* Error Message */}
      {error && (
        <div className="error-msg" role="alert" aria-live="polite">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          {error}
        </div>
      )}

      {/* Urdu Translation Panel */}
      {showTranslation && urduContent && (
        <div className="urdu-panel" role="region" aria-label="اردو ترجمہ">
          <div className="urdu-header">
            <h3 id="urdu-translation-heading">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="m5 8 6 6M4 14l6-6 2-3M2 5h12M7 2h1"/>
              </svg>
              اردو ترجمہ
            </h3>
            <button
              className="close-btn"
              onClick={() => setShowTranslation(false)}
              aria-label="اردو ترجمہ پینل بند کریں"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          <div className="urdu-content" dir="rtl" lang="ur">
            {urduContent}
          </div>
        </div>
      )}

      <style>{`
        .translate-urdu-wrapper {
          margin: 1.5rem 0;
          padding: 0;
        }

        .translate-btn {
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1.5rem;
          background: linear-gradient(135deg, #ffd700, #ffa500);
          color: #1a1a2e;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          font-size: 0.95rem;
          font-weight: 500;
          transition: all 0.2s ease;
          box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        }

        .translate-btn:hover:not(:disabled) {
          transform: translateY(-1px);
          box-shadow: 0 0 40px rgba(255, 215, 0, 0.5);
        }

        .translate-btn.active {
          background: #252540;
          color: #ffd700;
          border: 1px solid #ffd700;
        }

        .translate-btn:disabled {
          opacity: 0.7;
          cursor: wait;
        }

        .btn-label {
          font-size: 0.8rem;
          opacity: 0.85;
        }

        .spinner {
          width: 18px;
          height: 18px;
          border: 2px solid rgba(26, 26, 46, 0.3);
          border-top-color: #1a1a2e;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        .error-msg {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-top: 1rem;
          padding: 0.75rem 1rem;
          background: rgba(239, 68, 68, 0.1);
          color: #ef4444;
          border: 1px solid rgba(239, 68, 68, 0.3);
          border-radius: 8px;
          font-size: 0.9rem;
        }

        .urdu-panel {
          margin-top: 1.5rem;
          background: #1a1a2e;
          border: 1px solid rgba(255, 215, 0, 0.3);
          border-radius: 12px;
          overflow: hidden;
        }

        .urdu-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem 1.25rem;
          background: #252540;
          color: white;
          border-bottom: 1px solid rgba(255, 215, 0, 0.1);
        }

        .urdu-header h3 {
          margin: 0;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 1.1rem;
          font-weight: 600;
          color: #ffd700;
        }

        .close-btn {
          background: rgba(255, 215, 0, 0.1);
          border: none;
          border-radius: 6px;
          padding: 0.375rem;
          cursor: pointer;
          color: #b0b0c0;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: background 0.2s, color 0.2s;
        }

        .close-btn:hover {
          background: rgba(255, 215, 0, 0.2);
          color: #ffd700;
        }

        .urdu-content {
          padding: 1.5rem;
          font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', 'Urdu Typesetting', serif;
          font-size: 1.2rem;
          line-height: 2.4;
          color: #e2e8f0;
          text-align: right;
          white-space: pre-wrap;
          background: #0f0f1a;
        }

        [data-theme='dark'] .urdu-panel {
          background: #1a1a2e;
          border-color: rgba(255, 215, 0, 0.3);
        }

        [data-theme='dark'] .urdu-content {
          color: #e5e7eb;
        }

        [data-theme='dark'] .error-msg {
          background: rgba(239, 68, 68, 0.1);
          color: #fca5a5;
        }

        @media (max-width: 768px) {
          .translate-btn {
            width: 100%;
            justify-content: center;
          }

          .btn-label {
            display: none;
          }

          .urdu-content {
            font-size: 1.1rem;
            padding: 1rem;
          }
        }
      `}</style>
    </div>
  );
};

export default TranslateUrdu;
