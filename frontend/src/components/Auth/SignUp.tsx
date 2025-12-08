import React, { useState } from 'react';
import { useAuth, User } from './AuthContext';

type SkillLevel = 'beginner' | 'intermediate' | 'advanced';

interface SignUpProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete?: () => void;
}

export function SignUp({ isOpen, onClose, onComplete }: SignUpProps) {
  const { user, updateProfile, isLoading } = useAuth();
  const [step, setStep] = useState<'welcome' | 'software' | 'hardware' | 'complete'>('welcome');
  const [softwareLevel, setSoftwareLevel] = useState<SkillLevel>('intermediate');
  const [hardwareLevel, setHardwareLevel] = useState<SkillLevel>('beginner');
  const [isSaving, setIsSaving] = useState(false);

  if (!isOpen) return null;

  const skillInfo: Record<SkillLevel, { label: string; description: string; icon: string }> = {
    beginner: {
      label: 'Beginner',
      description: 'New to this area, starting from scratch',
      icon: '🌱',
    },
    intermediate: {
      label: 'Intermediate',
      description: 'Some experience, familiar with basics',
      icon: '🌿',
    },
    advanced: {
      label: 'Advanced',
      description: 'Experienced, comfortable with complex topics',
      icon: '🌳',
    },
  };

  const handleComplete = async () => {
    setIsSaving(true);
    try {
      await updateProfile({
        software_background: softwareLevel,
        hardware_background: hardwareLevel,
      });
      setStep('complete');
      setTimeout(() => {
        onComplete?.();
        onClose();
      }, 2000);
    } catch (error) {
      console.error('Failed to save profile:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const renderSkillSelector = (
    currentLevel: SkillLevel,
    onChange: (level: SkillLevel) => void,
    title: string,
    description: string
  ) => (
    <div className="skill-selector">
      <h3>{title}</h3>
      <p className="skill-description">{description}</p>
      <div className="skill-options">
        {(Object.keys(skillInfo) as SkillLevel[]).map((level) => (
          <button
            key={level}
            className={`skill-option ${currentLevel === level ? 'selected' : ''}`}
            onClick={() => onChange(level)}
          >
            <span className="skill-icon">{skillInfo[level].icon}</span>
            <div className="skill-info">
              <span className="skill-label">{skillInfo[level].label}</span>
              <span className="skill-desc">{skillInfo[level].description}</span>
            </div>
            {currentLevel === level && (
              <svg className="check-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            )}
          </button>
        ))}
      </div>
    </div>
  );

  return (
    <div className="signup-overlay" onClick={onClose}>
      <div className="signup-modal" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose} aria-label="Close">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        {/* Progress indicator */}
        <div className="progress-bar">
          <div className={`progress-step ${step !== 'welcome' ? 'completed' : 'active'}`}>1</div>
          <div className={`progress-line ${['software', 'hardware', 'complete'].includes(step) ? 'active' : ''}`} />
          <div className={`progress-step ${['hardware', 'complete'].includes(step) ? 'completed' : step === 'software' ? 'active' : ''}`}>2</div>
          <div className={`progress-line ${['hardware', 'complete'].includes(step) ? 'active' : ''}`} />
          <div className={`progress-step ${step === 'complete' ? 'completed' : step === 'hardware' ? 'active' : ''}`}>3</div>
        </div>

        {step === 'welcome' && (
          <div className="step-content">
            <div className="welcome-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                <line x1="12" y1="19" x2="12" y2="22" />
              </svg>
            </div>
            <h2>Welcome, {user?.name?.split(' ')[0] || 'there'}!</h2>
            <p>Let's personalize your learning experience. We'll ask a few quick questions about your background.</p>
            <button className="primary-btn" onClick={() => setStep('software')}>
              Get Started
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        )}

        {step === 'software' && (
          <div className="step-content">
            {renderSkillSelector(
              softwareLevel,
              setSoftwareLevel,
              'Software Background',
              'How would you describe your programming and software development experience?'
            )}
            <div className="button-row">
              <button className="secondary-btn" onClick={() => setStep('welcome')}>
                Back
              </button>
              <button className="primary-btn" onClick={() => setStep('hardware')}>
                Continue
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>
        )}

        {step === 'hardware' && (
          <div className="step-content">
            {renderSkillSelector(
              hardwareLevel,
              setHardwareLevel,
              'Hardware Background',
              'How familiar are you with robotics hardware, electronics, and physical systems?'
            )}
            <div className="button-row">
              <button className="secondary-btn" onClick={() => setStep('software')}>
                Back
              </button>
              <button className="primary-btn" onClick={handleComplete} disabled={isSaving}>
                {isSaving ? (
                  <>
                    <span className="spinner" />
                    Saving...
                  </>
                ) : (
                  <>
                    Complete Setup
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {step === 'complete' && (
          <div className="step-content complete-step">
            <div className="success-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <polyline points="16 10 11 15 8 12" />
              </svg>
            </div>
            <h2>You're all set!</h2>
            <p>Your personalized learning experience awaits. Content will be adapted to your skill level.</p>
          </div>
        )}
      </div>

      <style>{`
        .signup-overlay {
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

        .signup-modal {
          background: var(--ifm-background-color, #fff);
          border-radius: 20px;
          width: 100%;
          max-width: 480px;
          padding: 2rem;
          position: relative;
          box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
          animation: slideUp 0.3s ease-out;
        }

        @keyframes slideUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
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
          border-radius: 8px;
        }

        .close-btn:hover {
          background: var(--ifm-color-emphasis-100, #f5f5f5);
        }

        .progress-bar {
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 2rem;
          padding: 0 2rem;
        }

        .progress-step {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          background: var(--ifm-color-emphasis-200, #eee);
          color: var(--ifm-color-emphasis-500, #888);
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 600;
          font-size: 0.875rem;
          transition: all 0.3s;
        }

        .progress-step.active {
          background: var(--ifm-color-primary, #2e8555);
          color: white;
        }

        .progress-step.completed {
          background: var(--ifm-color-primary, #2e8555);
          color: white;
        }

        .progress-line {
          flex: 1;
          height: 3px;
          background: var(--ifm-color-emphasis-200, #eee);
          margin: 0 0.5rem;
          transition: background 0.3s;
        }

        .progress-line.active {
          background: var(--ifm-color-primary, #2e8555);
        }

        .step-content {
          text-align: center;
        }

        .welcome-icon, .success-icon {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 80px;
          height: 80px;
          background: linear-gradient(135deg, var(--ifm-color-primary-light, #3ba55d), var(--ifm-color-primary, #2e8555));
          border-radius: 20px;
          color: white;
          margin-bottom: 1.5rem;
        }

        .complete-step .success-icon {
          background: linear-gradient(135deg, #10b981, #059669);
        }

        .step-content h2 {
          margin: 0 0 0.75rem 0;
          font-size: 1.5rem;
          color: var(--ifm-font-color-base, #333);
        }

        .step-content > p {
          margin: 0 0 1.5rem 0;
          color: var(--ifm-color-emphasis-600, #666);
          font-size: 0.95rem;
          line-height: 1.5;
        }

        .skill-selector h3 {
          margin: 0 0 0.5rem 0;
          font-size: 1.25rem;
          color: var(--ifm-font-color-base, #333);
        }

        .skill-description {
          margin: 0 0 1.25rem 0;
          color: var(--ifm-color-emphasis-600, #666);
          font-size: 0.9rem;
        }

        .skill-options {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
          margin-bottom: 1.5rem;
        }

        .skill-option {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 1rem;
          background: var(--ifm-color-emphasis-100, #f5f5f5);
          border: 2px solid transparent;
          border-radius: 12px;
          cursor: pointer;
          text-align: left;
          transition: all 0.2s;
        }

        .skill-option:hover {
          background: var(--ifm-color-emphasis-200, #eee);
        }

        .skill-option.selected {
          border-color: var(--ifm-color-primary, #2e8555);
          background: rgba(46, 133, 85, 0.05);
        }

        .skill-icon {
          font-size: 1.5rem;
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

        .skill-desc {
          font-size: 0.8rem;
          color: var(--ifm-color-emphasis-600, #666);
        }

        .check-icon {
          color: var(--ifm-color-primary, #2e8555);
        }

        .button-row {
          display: flex;
          gap: 0.75rem;
        }

        .primary-btn, .secondary-btn {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          padding: 0.875rem 1.25rem;
          border-radius: 10px;
          font-size: 0.95rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
        }

        .primary-btn {
          background: var(--ifm-color-primary, #2e8555);
          color: white;
          border: none;
        }

        .primary-btn:hover:not(:disabled) {
          background: var(--ifm-color-primary-dark, #257347);
        }

        .primary-btn:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }

        .secondary-btn {
          background: var(--ifm-color-emphasis-100, #f5f5f5);
          color: var(--ifm-font-color-base, #333);
          border: 1px solid var(--ifm-color-emphasis-300, #ddd);
        }

        .secondary-btn:hover {
          background: var(--ifm-color-emphasis-200, #eee);
        }

        .spinner {
          width: 18px;
          height: 18px;
          border: 2px solid rgba(255, 255, 255, 0.3);
          border-top-color: white;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        @media (max-width: 480px) {
          .signup-modal {
            padding: 1.5rem;
          }
          .button-row {
            flex-direction: column;
          }
        }
      `}</style>
    </div>
  );
}

export default SignUp;
