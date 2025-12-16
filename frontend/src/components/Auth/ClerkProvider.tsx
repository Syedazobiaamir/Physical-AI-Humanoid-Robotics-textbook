import React from 'react';
import { ClerkProvider as ClerkProviderBase, SignInButton, SignUpButton, UserButton, useUser, SignedIn, SignedOut } from '@clerk/clerk-react';

// Clerk appearance configuration with Dark Blue + Yellow theme
const clerkAppearance = {
  baseTheme: undefined,
  variables: {
    colorPrimary: '#ffd700',
    colorBackground: '#1a1a2e',
    colorInputBackground: '#252540',
    colorInputText: '#ffffff',
    colorText: '#ffffff',
    colorTextSecondary: '#b0b0c0',
    colorDanger: '#ef4444',
    colorSuccess: '#22c55e',
    colorWarning: '#f59e0b',
    borderRadius: '8px',
    fontFamily: 'Inter, system-ui, sans-serif',
  },
  elements: {
    // Card and modal styling
    card: {
      backgroundColor: '#1a1a2e',
      border: '1px solid rgba(255, 215, 0, 0.2)',
      boxShadow: '0 20px 40px rgba(0, 0, 0, 0.4)',
    },
    modalContent: {
      backgroundColor: '#1a1a2e',
    },
    modalCloseButton: {
      color: '#b0b0c0',
      '&:hover': {
        color: '#ffd700',
      },
    },
    // Form elements
    formButtonPrimary: {
      background: 'linear-gradient(135deg, #ffd700 0%, #ffa500 100%)',
      color: '#1a1a2e',
      fontWeight: '600',
      '&:hover': {
        background: 'linear-gradient(135deg, #ffe44d 0%, #ffb347 100%)',
      },
    },
    formFieldInput: {
      backgroundColor: '#252540',
      borderColor: 'rgba(255, 215, 0, 0.2)',
      color: '#ffffff',
      '&:focus': {
        borderColor: '#ffd700',
        boxShadow: '0 0 0 2px rgba(255, 215, 0, 0.2)',
      },
    },
    formFieldLabel: {
      color: '#b0b0c0',
    },
    // Social buttons
    socialButtonsBlockButton: {
      backgroundColor: '#252540',
      borderColor: 'rgba(255, 215, 0, 0.2)',
      color: '#ffffff',
      '&:hover': {
        backgroundColor: 'rgba(255, 215, 0, 0.1)',
        borderColor: '#ffd700',
      },
    },
    // Header and footer
    headerTitle: {
      color: '#ffffff',
    },
    headerSubtitle: {
      color: '#b0b0c0',
    },
    footerActionLink: {
      color: '#ffd700',
      '&:hover': {
        color: '#ffe44d',
      },
    },
    // Divider
    dividerLine: {
      backgroundColor: 'rgba(255, 215, 0, 0.1)',
    },
    dividerText: {
      color: '#7a7a90',
    },
    // User button popover
    userButtonPopoverCard: {
      backgroundColor: '#1a1a2e',
      border: '1px solid rgba(255, 215, 0, 0.2)',
    },
    userButtonPopoverActionButton: {
      color: '#ffffff',
      '&:hover': {
        backgroundColor: 'rgba(255, 215, 0, 0.1)',
      },
    },
    // Avatar
    avatarBox: {
      border: '2px solid #ffd700',
    },
  },
};

// Get Clerk publishable key from environment
// For Docusaurus, we use a custom config approach
const getClerkKey = (): string => {
  // Check for window-injected key first (from docusaurus.config.ts)
  if (typeof window !== 'undefined' && (window as any).__CLERK_PUBLISHABLE_KEY__) {
    return (window as any).__CLERK_PUBLISHABLE_KEY__;
  }

  // Check environment variables
  if (typeof process !== 'undefined' && process.env) {
    return process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY ||
           process.env.CLERK_PUBLISHABLE_KEY ||
           process.env.REACT_APP_CLERK_PUBLISHABLE_KEY ||
           '';
  }

  return '';
};

interface ClerkProviderProps {
  children: React.ReactNode;
}

export function ClerkProvider({ children }: ClerkProviderProps) {
  const publishableKey = getClerkKey();

  // If no key is configured, render children without Clerk
  if (!publishableKey) {
    console.warn('Clerk publishable key not configured. Auth features disabled.');
    return <>{children}</>;
  }

  return (
    <ClerkProviderBase
      publishableKey={publishableKey}
      appearance={clerkAppearance}
      afterSignOutUrl="/"
    >
      {children}
    </ClerkProviderBase>
  );
}

// Re-export Clerk components for convenience
export { SignInButton, SignUpButton, UserButton, useUser, SignedIn, SignedOut };

export default ClerkProvider;
