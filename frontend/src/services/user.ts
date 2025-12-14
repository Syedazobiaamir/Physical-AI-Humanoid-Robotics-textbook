/**
 * User API Client Service
 * Handles user profile management and personalization settings
 */

import { API_BASE_URL } from '@site/src/config/api';

// Types
export interface UserProfile {
  id: string;
  email: string;
  name: string | null;
  skillLevel: 'beginner' | 'intermediate' | 'advanced';
  background: 'software' | 'hardware' | 'both' | 'neither';
  languagePreference: 'en' | 'ur';
  learningGoals: string[];
  createdAt: string;
  updatedAt: string;
}

export interface UpdateProfileData {
  name?: string;
  skillLevel?: UserProfile['skillLevel'];
  background?: UserProfile['background'];
  languagePreference?: UserProfile['languagePreference'];
  learningGoals?: string[];
}

export interface UserProgress {
  chaptersCompleted: string[];
  quizScores: Record<string, number>;
  lastAccessed: string;
  totalTimeSpent: number;
}

// Helper to get auth token
const getAuthToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('auth_token');
};

// Helper for authenticated fetch
const authenticatedFetch = async (
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> => {
  const token = getAuthToken();

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  return response;
};

/**
 * User API Client
 */
export const userApi = {
  /**
   * Get current user's profile
   */
  async getProfile(): Promise<UserProfile | null> {
    try {
      const response = await authenticatedFetch('/personalization/profile');

      if (!response.ok) {
        if (response.status === 401) {
          return null; // Not authenticated
        }
        throw new Error('Failed to fetch profile');
      }

      const data = await response.json();

      // Map backend snake_case to frontend camelCase
      return {
        id: data.id,
        email: data.email,
        name: data.name,
        skillLevel: data.skill_level || 'beginner',
        background: data.background || 'neither',
        languagePreference: data.language_preference || 'en',
        learningGoals: data.learning_goals || [],
        createdAt: data.created_at,
        updatedAt: data.updated_at,
      };
    } catch (error) {
      console.error('Error fetching profile:', error);
      return null;
    }
  },

  /**
   * Update user profile
   */
  async updateProfile(data: UpdateProfileData): Promise<UserProfile | null> {
    try {
      // Map to backend format
      const payload: Record<string, unknown> = {};
      if (data.name !== undefined) payload.name = data.name;
      if (data.skillLevel !== undefined) payload.skill_level = data.skillLevel;
      if (data.background !== undefined) payload.background = data.background;
      if (data.languagePreference !== undefined)
        payload.language_preference = data.languagePreference;
      if (data.learningGoals !== undefined)
        payload.learning_goals = data.learningGoals;

      const response = await authenticatedFetch('/personalization/profile', {
        method: 'PATCH',
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Failed to update profile');
      }

      return await this.getProfile();
    } catch (error) {
      console.error('Error updating profile:', error);
      return null;
    }
  },

  /**
   * Create initial profile (during onboarding)
   */
  async createProfile(data: UpdateProfileData): Promise<UserProfile | null> {
    try {
      const payload = {
        skill_level: data.skillLevel,
        background: data.background,
        language_preference: data.languagePreference,
        learning_goals: data.learningGoals,
      };

      const response = await authenticatedFetch('/personalization/profile', {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Failed to create profile');
      }

      return await this.getProfile();
    } catch (error) {
      console.error('Error creating profile:', error);
      return null;
    }
  },

  /**
   * Get user's learning progress
   */
  async getProgress(): Promise<UserProgress | null> {
    try {
      const response = await authenticatedFetch('/progress');

      if (!response.ok) {
        if (response.status === 401) return null;
        throw new Error('Failed to fetch progress');
      }

      const data = await response.json();

      return {
        chaptersCompleted: data.chapters_completed || [],
        quizScores: data.quiz_scores || {},
        lastAccessed: data.last_accessed,
        totalTimeSpent: data.total_time_spent || 0,
      };
    } catch (error) {
      console.error('Error fetching progress:', error);
      return null;
    }
  },

  /**
   * Mark a chapter as completed
   */
  async markChapterComplete(chapterId: string): Promise<boolean> {
    try {
      const response = await authenticatedFetch('/progress/chapter', {
        method: 'POST',
        body: JSON.stringify({ chapter_id: chapterId }),
      });

      return response.ok;
    } catch (error) {
      console.error('Error marking chapter complete:', error);
      return false;
    }
  },

  /**
   * Submit quiz score
   */
  async submitQuizScore(
    chapterId: string,
    score: number,
    totalQuestions: number
  ): Promise<boolean> {
    try {
      const response = await authenticatedFetch('/progress/quiz', {
        method: 'POST',
        body: JSON.stringify({
          chapter_id: chapterId,
          score,
          total_questions: totalQuestions,
        }),
      });

      return response.ok;
    } catch (error) {
      console.error('Error submitting quiz score:', error);
      return false;
    }
  },

  /**
   * Delete user account
   */
  async deleteAccount(): Promise<boolean> {
    try {
      const response = await authenticatedFetch('/auth/account', {
        method: 'DELETE',
      });

      if (response.ok) {
        localStorage.removeItem('auth_token');
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error deleting account:', error);
      return false;
    }
  },
};

export default userApi;
