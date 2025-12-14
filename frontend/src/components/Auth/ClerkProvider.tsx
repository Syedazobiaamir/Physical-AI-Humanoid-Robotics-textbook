import React from 'react';
import { ClerkProvider as ClerkProviderBase, SignInButton, SignUpButton, UserButton, useUser, SignedIn, SignedOut } from '@clerk/clerk-react';

// Get Clerk publishable key from environment or config
const CLERK_PUBLISHABLE_KEY = typeof window !== 'undefined'
  ? (window as any).__CLERK_PUBLISHABLE_KEY__ || process.env.CLERK_PUBLISHABLE_KEY || ''
  : '';

interface ClerkProviderProps {
  children: React.ReactNode;
}

export function ClerkProvider({ children }: ClerkProviderProps) {
  // If no key is configured, render children without Clerk
  if (!CLERK_PUBLISHABLE_KEY) {
    console.warn('Clerk publishable key not configured. Auth features disabled.');
    return <>{children}</>;
  }

  return (
    <ClerkProviderBase publishableKey={CLERK_PUBLISHABLE_KEY}>
      {children}
    </ClerkProviderBase>
  );
}

// Re-export Clerk components for convenience
export { SignInButton, SignUpButton, UserButton, useUser, SignedIn, SignedOut };

export default ClerkProvider;
