import React, { useState, useEffect, useCallback } from 'react';

type SkillLevel = 'beginner' | 'intermediate' | 'advanced';

interface PersonalizeButtonProps {
  chapterId: string;
  onContentAdapted?: (adaptedContent: string) => void;
  initialSkillLevel?: SkillLevel;
}

interface PreferencesState {
  skillLevel: SkillLevel;
  isLoading: boolean;
  error: string | null;
}

const API_URL = 'http://localhost:8000';

const PersonalizeButton: React.FC<PersonalizeButtonProps> = ({
  chapterId,
  onContentAdapted,
  initialSkillLevel = 'intermediate',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [state, setState] = useState<PreferencesState>({
    skillLevel: initialSkillLevel,
    isLoading: false,
    error: null,
  });
  const [isAdapting, setIsAdapting] = useState(false);

  const getToken = useCallback(() => {
    return localStorage.getItem('physical_ai_access_token');
  }, []);

  const isAuthenticated = useCallback(() => {
    const token = getToken();
    if (!token) return false;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return Date.now() < payload.exp * 1000;
    } catch {
      return false;
    }
  }, [getToken]);

  // Fetch current preferences on mount
  useEffect(() => {
    if (isAuthenticated() && chapterId) {
      fetchPreferences();
    }
  }, [chapterId, isAuthenticated]);

  const fetchPreferences = async () => {
    const token = getToken();
    if (!token) return;

    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await fetch(
        `${API_URL}/api/v1/personalization/preferences/${chapterId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setState((prev) => ({
          ...prev,
          skillLevel: data.skill_level as SkillLevel,
          isLoading: false,
        }));
      } else if (response.status === 404) {
        // No preferences set yet, use default
        setState((prev) => ({ ...prev, isLoading: false }));
      } else {
        throw new Error('Failed to fetch preferences');
      }
    } catch (err) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: 'Failed to load preferences',
      }));
    }
  };

  const updatePreferences = async (newSkillLevel: SkillLevel) => {
    const token = getToken();
    if (!token) {
      setState((prev) => ({ ...prev, error: 'Please sign in to personalize content' }));
      return;
    }

    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await fetch(
        `${API_URL}/api/v1/personalization/preferences/${chapterId}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            skill_level: newSkillLevel,
            customizations: {},
          }),
        }
      );

      if (response.ok) {
        setState((prev) => ({
          ...prev,
          skillLevel: newSkillLevel,
          isLoading: false,
        }));
      } else {
        throw new Error('Failed to update preferences');
      }
    } catch (err) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: 'Failed to update preferences',
      }));
    }
  };

  const adaptContent = async () => {
    const token = getToken();
    if (!token) {
      setState((prev) => ({ ...prev, error: 'Please sign in to personalize content' }));
      return;
    }

    setIsAdapting(true);
    setState((prev) => ({ ...prev, error: null }));

    try {
      const response = await fetch(`${API_URL}/api/v1/personalization/adapt-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          chapter_id: chapterId,
          skill_level: state.skillLevel,
          content_format: 'mdx',
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (onContentAdapted) {
          onContentAdapted(data.adapted_content);
        }
        setIsOpen(false);
      } else {
        throw new Error('Failed to adapt content');
      }
    } catch (err) {
      setState((prev) => ({
        ...prev,
        error: 'Failed to adapt content. Please try again.',
      }));
    } finally {
      setIsAdapting(false);
    }
  };

  const handleSkillChange = (level: SkillLevel) => {
    updatePreferences(level);
  };

  const skillLevelInfo: Record<SkillLevel, { label: string; description: string; icon: string }> = {
    beginner: {
      label: 'Beginner',
      description: 'New to the topic. Include extra explanations and step-by-step guidance.',
      icon: '🌱',
    },
    intermediate: {
      label: 'Intermediate',
      description: 'Familiar with basics. Focus on practical applications and deeper concepts.',
      icon: '🌿',
    },
    advanced: {
      label: 'Advanced',
      description: 'Experienced practitioner. Show advanced topics and cutting-edge research.',
      icon: '🌳',
    },
  };

  return (
    <>
      <button
        className="personalize-button"
        onClick={() => setIsOpen(!isOpen)}
        title="Personalize content for your skill level"
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
          <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
          <line x1="12" y1="19" x2="12" y2="22" />
        </svg>
        <span>Personalize</span>
        <span className="skill-badge">{skillLevelInfo[state.skillLevel].icon}</span>
      </button>

      {isOpen && (
        <div className="personalize-modal-overlay" onClick={() => setIsOpen(false)}>
          <div className="personalize-modal" onClick={(e) => e.stopPropagation()}>
            <div className="personalize-header">
              <h3>Personalize Content</h3>
              <button className="close-btn" onClick={() => setIsOpen(false)}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>

            <div className="personalize-body">
              {!isAuthenticated() && (
                <div className="auth-notice">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                  </svg>
                  <p>Sign in to save your preferences across sessions.</p>
                </div>
              )}

              <p className="description">
                Select your skill level to adapt this chapter's content to your experience.
              </p>

              <div className="skill-options">
                {(Object.keys(skillLevelInfo) as SkillLevel[]).map((level) => (
                  <button
                    key={level}
                    className={`skill-option ${state.skillLevel === level ? 'selected' : ''}`}
                    onClick={() => handleSkillChange(level)}
                    disabled={state.isLoading}
                  >
                    <span className="skill-icon">{skillLevelInfo[level].icon}</span>
                    <div className="skill-info">
                      <span className="skill-label">{skillLevelInfo[level].label}</span>
                      <span className="skill-description">{skillLevelInfo[level].description}</span>
                    </div>
                    {state.skillLevel === level && (
                      <svg className="check-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <polyline points="20 6 9 17 4 12"></polyline>
                      </svg>
                    )}
                  </button>
                ))}
              </div>

              {state.error && (
                <div className="error-message">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                  </svg>
                  {state.error}
                </div>
              )}
            </div>

            <div className="personalize-footer">
              <button
                className="adapt-button"
                onClick={adaptContent}
                disabled={isAdapting || state.isLoading || !isAuthenticated()}
              >
                {isAdapting ? (
                  <>
                    <span className="spinner"></span>
                    Adapting...
                  </>
                ) : (
                  <>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" />
                      <path d="M21 3v5h-5" />
                      <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" />
                      <path d="M8 16H3v5" />
                    </svg>
                    Apply Personalization
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      <style>{`
        .personalize-button {
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.5rem 1rem;
          background: var(--ifm-color-primary-light, #3ba55d);
          color: white;
          border: none;
          border-radius: 20px;
          cursor: pointer;
          font-size: 0.875rem;
          font-weight: 500;
          transition: all 0.2s;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .personalize-button:hover {
          background: var(--ifm-color-primary, #2e8555);
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .skill-badge {
          font-size: 1rem;
        }

        .personalize-modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
          padding: 1rem;
        }

        .personalize-modal {
          background: var(--ifm-background-color, #fff);
          border-radius: 16px;
          width: 100%;
          max-width: 480px;
          box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
          overflow: hidden;
        }

        .personalize-header {
          padding: 1.25rem 1.5rem;
          border-bottom: 1px solid var(--ifm-color-emphasis-200, #eee);
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .personalize-header h3 {
          margin: 0;
          font-size: 1.25rem;
          color: var(--ifm-font-color-base, #333);
        }

        .close-btn {
          background: transparent;
          border: none;
          cursor: pointer;
          padding: 0.25rem;
          color: var(--ifm-color-emphasis-500, #888);
          transition: color 0.2s;
        }

        .close-btn:hover {
          color: var(--ifm-font-color-base, #333);
        }

        .personalize-body {
          padding: 1.5rem;
        }

        .auth-notice {
          display: flex;
          align-items: flex-start;
          gap: 0.75rem;
          padding: 1rem;
          background: #fff3cd;
          border-radius: 8px;
          margin-bottom: 1rem;
          color: #856404;
        }

        .auth-notice svg {
          flex-shrink: 0;
          margin-top: 0.125rem;
        }

        .auth-notice p {
          margin: 0;
          font-size: 0.875rem;
        }

        .description {
          color: var(--ifm-color-emphasis-600, #666);
          font-size: 0.9rem;
          margin: 0 0 1.25rem 0;
        }

        .skill-options {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .skill-option {
          display: flex;
          align-items: flex-start;
          gap: 1rem;
          padding: 1rem;
          background: var(--ifm-color-emphasis-100, #f5f5f5);
          border: 2px solid transparent;
          border-radius: 12px;
          cursor: pointer;
          text-align: left;
          transition: all 0.2s;
        }

        .skill-option:hover:not(:disabled) {
          background: var(--ifm-color-emphasis-200, #eee);
        }

        .skill-option.selected {
          border-color: var(--ifm-color-primary, #2e8555);
          background: rgba(46, 133, 85, 0.05);
        }

        .skill-option:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .skill-icon {
          font-size: 1.5rem;
          line-height: 1;
        }

        .skill-info {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        .skill-label {
          font-weight: 600;
          color: var(--ifm-font-color-base, #333);
        }

        .skill-description {
          font-size: 0.8rem;
          color: var(--ifm-color-emphasis-600, #666);
        }

        .check-icon {
          color: var(--ifm-color-primary, #2e8555);
          flex-shrink: 0;
        }

        .error-message {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-top: 1rem;
          padding: 0.75rem;
          background: #f8d7da;
          color: #842029;
          border-radius: 8px;
          font-size: 0.875rem;
        }

        .personalize-footer {
          padding: 1rem 1.5rem;
          border-top: 1px solid var(--ifm-color-emphasis-200, #eee);
          background: var(--ifm-color-emphasis-100, #f9f9f9);
        }

        .adapt-button {
          width: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          padding: 0.875rem 1.5rem;
          background: var(--ifm-color-primary, #2e8555);
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
        }

        .adapt-button:hover:not(:disabled) {
          background: var(--ifm-color-primary-dark, #257347);
        }

        .adapt-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
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

        @media (max-width: 768px) {
          .personalize-modal {
            max-width: 100%;
          }

          .skill-option {
            padding: 0.875rem;
          }
        }
      `}</style>
    </>
  );
};

export default PersonalizeButton;
