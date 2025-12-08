import { createContext, useContext } from 'react';

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'student' | 'author' | 'admin';
  avatar_url?: string;
  software_background?: 'beginner' | 'intermediate' | 'advanced';
  hardware_background?: 'beginner' | 'intermediate' | 'advanced';
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (provider: 'google' | 'github') => Promise<void>;
  logout: () => void;
  handleOAuthCallback: (code: string, provider: string) => Promise<void>;
  updateProfile: (updates: Partial<User>) => Promise<void>;
  clearError: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthContext;
