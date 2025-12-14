import React from 'react';
import Content from '@theme-original/Navbar/Content';
import type ContentType from '@theme/Navbar/Content';
import type {WrapperProps} from '@docusaurus/types';
import BrowserOnly from '@docusaurus/BrowserOnly';
import styles from './styles.module.css';

type Props = WrapperProps<typeof ContentType>;

// Clerk Auth Buttons - loaded dynamically
function ClerkAuthButtons() {
  const [ClerkComponents, setClerkComponents] = React.useState<{
    ClerkProvider: React.ComponentType<any>;
    SignedIn: React.ComponentType<any>;
    SignedOut: React.ComponentType<any>;
    SignInButton: React.ComponentType<any>;
    SignUpButton: React.ComponentType<any>;
    UserButton: React.ComponentType<any>;
  } | null>(null);

  React.useEffect(() => {
    import('@clerk/clerk-react').then((clerk) => {
      setClerkComponents({
        ClerkProvider: clerk.ClerkProvider,
        SignedIn: clerk.SignedIn,
        SignedOut: clerk.SignedOut,
        SignInButton: clerk.SignInButton,
        SignUpButton: clerk.SignUpButton,
        UserButton: clerk.UserButton,
      });
    });
  }, []);

  if (!ClerkComponents) {
    return (
      <div className={styles.authPlaceholder}>
        <span className={styles.signInPlaceholder}>Loading...</span>
      </div>
    );
  }

  const { ClerkProvider, SignedIn, SignedOut, SignInButton, SignUpButton, UserButton } = ClerkComponents;

  // Get Clerk key from window or fallback
  const clerkKey = (window as any).__CLERK_PUBLISHABLE_KEY__ ||
                   (window as any).CLERK_PUBLISHABLE_KEY ||
                   '';

  if (!clerkKey) {
    return (
      <div className={styles.authButtons}>
        <span className={styles.authDisabled}>Auth not configured</span>
      </div>
    );
  }

  return (
    <ClerkProvider publishableKey={clerkKey}>
      <div className={styles.authButtons}>
        <SignedOut>
          <SignInButton mode="modal">
            <button className={styles.signInBtn}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
                <polyline points="10 17 15 12 10 7" />
                <line x1="15" y1="12" x2="3" y2="12" />
              </svg>
              Sign In
            </button>
          </SignInButton>
          <SignUpButton mode="modal">
            <button className={styles.signUpBtn}>
              Sign Up
            </button>
          </SignUpButton>
        </SignedOut>
        <SignedIn>
          <UserButton
            afterSignOutUrl="/"
            appearance={{
              elements: {
                avatarBox: {
                  width: 36,
                  height: 36,
                }
              }
            }}
          />
        </SignedIn>
      </div>
    </ClerkProvider>
  );
}

export default function ContentWrapper(props: Props): JSX.Element {
  return (
    <>
      <Content {...props} />
      <BrowserOnly fallback={<div className={styles.authPlaceholder} />}>
        {() => <ClerkAuthButtons />}
      </BrowserOnly>
    </>
  );
}
