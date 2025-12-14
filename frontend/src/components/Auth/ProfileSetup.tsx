import React, { useState } from 'react';
import styles from './ProfileSetup.module.css';
import { API_BASE_URL } from '@site/src/config/api';

export interface ProfileData {
  skillLevel: 'beginner' | 'intermediate' | 'advanced';
  background: 'software' | 'hardware' | 'both' | 'neither';
  languagePreference: 'en' | 'ur';
  learningGoals: string[];
}

interface ProfileSetupProps {
  onComplete: (profile: ProfileData) => void;
  onSkip?: () => void;
  isModal?: boolean;
}

const skillLevelOptions = [
  {
    value: 'beginner',
    label: 'Beginner',
    description: 'New to robotics and programming',
    icon: '🌱',
  },
  {
    value: 'intermediate',
    label: 'Intermediate',
    description: 'Some experience with ROS or robotics',
    icon: '🌿',
  },
  {
    value: 'advanced',
    label: 'Advanced',
    description: 'Professional or research experience',
    icon: '🌳',
  },
];

const backgroundOptions = [
  {
    value: 'software',
    label: 'Software',
    description: 'Programming, algorithms, AI/ML',
    icon: '💻',
  },
  {
    value: 'hardware',
    label: 'Hardware',
    description: 'Electronics, mechanics, sensors',
    icon: '🔧',
  },
  {
    value: 'both',
    label: 'Both',
    description: 'Full-stack robotics experience',
    icon: '🤖',
  },
  {
    value: 'neither',
    label: 'New to Both',
    description: 'Starting fresh in robotics',
    icon: '🎯',
  },
];

const learningGoalOptions = [
  { value: 'ros2', label: 'Master ROS2' },
  { value: 'simulation', label: 'Build Simulations' },
  { value: 'hardware', label: 'Work with Real Robots' },
  { value: 'ai', label: 'Robot AI & Learning' },
  { value: 'career', label: 'Career in Robotics' },
  { value: 'research', label: 'Academic Research' },
];

const ProfileSetup: React.FC<ProfileSetupProps> = ({
  onComplete,
  onSkip,
  isModal = false,
}) => {
  const [step, setStep] = useState(1);
  const [profile, setProfile] = useState<ProfileData>({
    skillLevel: 'beginner',
    background: 'neither',
    languagePreference: 'en',
    learningGoals: [],
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const totalSteps = 3;

  const handleSkillSelect = (level: ProfileData['skillLevel']) => {
    setProfile((prev) => ({ ...prev, skillLevel: level }));
  };

  const handleBackgroundSelect = (bg: ProfileData['background']) => {
    setProfile((prev) => ({ ...prev, background: bg }));
  };

  const handleGoalToggle = (goal: string) => {
    setProfile((prev) => ({
      ...prev,
      learningGoals: prev.learningGoals.includes(goal)
        ? prev.learningGoals.filter((g) => g !== goal)
        : [...prev.learningGoals, goal],
    }));
  };

  const handleLanguageSelect = (lang: ProfileData['languagePreference']) => {
    setProfile((prev) => ({ ...prev, languagePreference: lang }));
  };

  const handleNext = () => {
    if (step < totalSteps) {
      setStep(step + 1);
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setError(null);

    try {
      // Save profile to backend
      const token = localStorage.getItem('auth_token');
      if (token) {
        const response = await fetch(`${API_BASE_URL}/personalization/profile`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            skill_level: profile.skillLevel,
            background: profile.background,
            language_preference: profile.languagePreference,
            learning_goals: profile.learningGoals,
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to save profile');
        }
      }

      onComplete(profile);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save profile');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={`${styles.container} ${isModal ? styles.modal : ''}`}>
      <div className={styles.header}>
        <h2 className={styles.title}>Personalize Your Experience</h2>
        <p className={styles.subtitle}>
          Help us tailor the content to your needs
        </p>
        <div className={styles.progress}>
          {Array.from({ length: totalSteps }).map((_, i) => (
            <div
              key={i}
              className={`${styles.progressDot} ${
                i + 1 <= step ? styles.active : ''
              }`}
            />
          ))}
        </div>
      </div>

      <div className={styles.content}>
        {/* Step 1: Skill Level */}
        {step === 1 && (
          <div className={styles.step}>
            <h3 className={styles.stepTitle}>What's your experience level?</h3>
            <div className={styles.optionGrid}>
              {skillLevelOptions.map((option) => (
                <button
                  key={option.value}
                  className={`${styles.optionCard} ${
                    profile.skillLevel === option.value ? styles.selected : ''
                  }`}
                  onClick={() =>
                    handleSkillSelect(option.value as ProfileData['skillLevel'])
                  }
                >
                  <span className={styles.optionIcon}>{option.icon}</span>
                  <span className={styles.optionLabel}>{option.label}</span>
                  <span className={styles.optionDescription}>
                    {option.description}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Step 2: Background */}
        {step === 2 && (
          <div className={styles.step}>
            <h3 className={styles.stepTitle}>What's your background?</h3>
            <div className={styles.optionGrid}>
              {backgroundOptions.map((option) => (
                <button
                  key={option.value}
                  className={`${styles.optionCard} ${
                    profile.background === option.value ? styles.selected : ''
                  }`}
                  onClick={() =>
                    handleBackgroundSelect(
                      option.value as ProfileData['background']
                    )
                  }
                >
                  <span className={styles.optionIcon}>{option.icon}</span>
                  <span className={styles.optionLabel}>{option.label}</span>
                  <span className={styles.optionDescription}>
                    {option.description}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Step 3: Goals & Language */}
        {step === 3 && (
          <div className={styles.step}>
            <h3 className={styles.stepTitle}>Final touches</h3>

            <div className={styles.section}>
              <h4 className={styles.sectionTitle}>Learning Goals</h4>
              <p className={styles.sectionHint}>Select all that apply</p>
              <div className={styles.chipGrid}>
                {learningGoalOptions.map((goal) => (
                  <button
                    key={goal.value}
                    className={`${styles.chip} ${
                      profile.learningGoals.includes(goal.value)
                        ? styles.selected
                        : ''
                    }`}
                    onClick={() => handleGoalToggle(goal.value)}
                  >
                    {goal.label}
                  </button>
                ))}
              </div>
            </div>

            <div className={styles.section}>
              <h4 className={styles.sectionTitle}>Language Preference</h4>
              <div className={styles.languageOptions}>
                <button
                  className={`${styles.languageOption} ${
                    profile.languagePreference === 'en' ? styles.selected : ''
                  }`}
                  onClick={() => handleLanguageSelect('en')}
                >
                  <span className={styles.flag}>🇺🇸</span>
                  English
                </button>
                <button
                  className={`${styles.languageOption} ${
                    profile.languagePreference === 'ur' ? styles.selected : ''
                  }`}
                  onClick={() => handleLanguageSelect('ur')}
                >
                  <span className={styles.flag}>🇵🇰</span>
                  اردو (Urdu)
                </button>
              </div>
            </div>
          </div>
        )}

        {error && <div className={styles.error}>{error}</div>}
      </div>

      <div className={styles.footer}>
        {step > 1 && (
          <button className={styles.backButton} onClick={handleBack}>
            Back
          </button>
        )}

        {onSkip && step === 1 && (
          <button className={styles.skipButton} onClick={onSkip}>
            Skip for now
          </button>
        )}

        <div className={styles.spacer} />

        {step < totalSteps ? (
          <button className={styles.nextButton} onClick={handleNext}>
            Next
          </button>
        ) : (
          <button
            className={styles.submitButton}
            onClick={handleSubmit}
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Saving...' : 'Complete Setup'}
          </button>
        )}
      </div>
    </div>
  );
};

export default ProfileSetup;
