import React from 'react';
import { SignInButton, SignUpButton, UserButton, SignedIn, SignedOut, useUser } from '@clerk/clerk-react';
import styles from './UserMenu.module.css';

interface UserMenuProps {
  onSignInClick?: () => void;
  showSignUp?: boolean;
}

/**
 * UserMenu component using Clerk authentication
 *
 * Displays:
 * - Sign In / Sign Up buttons when user is not authenticated
 * - User avatar and profile menu when authenticated
 *
 * Styled with Dark Blue + Yellow theme per Constitution v4.0.0
 */
export function UserMenu({ showSignUp = true }: UserMenuProps) {
  const { user, isLoaded } = useUser();

  // Show nothing while loading to prevent layout shift
  if (!isLoaded) {
    return (
      <div className={styles.container}>
        <div className={styles.skeleton} />
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <SignedOut>
        <div className={styles.authButtons}>
          <SignInButton mode="modal">
            <button className={styles.signInButton}>
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
                <polyline points="10 17 15 12 10 7" />
                <line x1="15" y1="12" x2="3" y2="12" />
              </svg>
              <span>Sign In</span>
            </button>
          </SignInButton>

          {showSignUp && (
            <SignUpButton mode="modal">
              <button className={styles.signUpButton}>
                <svg
                  width="18"
                  height="18"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                  <circle cx="8.5" cy="7" r="4" />
                  <line x1="20" y1="8" x2="20" y2="14" />
                  <line x1="23" y1="11" x2="17" y2="11" />
                </svg>
                <span>Sign Up</span>
              </button>
            </SignUpButton>
          )}
        </div>
      </SignedOut>

      <SignedIn>
        <div className={styles.userProfile}>
          <UserButton
            appearance={{
              elements: {
                avatarBox: styles.clerkAvatar,
                userButtonTrigger: styles.userButtonTrigger,
                userButtonPopoverCard: styles.userButtonPopover,
                userButtonPopoverActionButton: styles.popoverActionButton,
                userButtonPopoverActionButtonText: styles.popoverActionText,
                userButtonPopoverFooter: styles.popoverFooter,
              },
            }}
            afterSignOutUrl="/"
          />
          {user && (
            <span className={styles.userName}>
              {user.firstName || user.username || 'User'}
            </span>
          )}
        </div>
      </SignedIn>
    </div>
  );
}

export default UserMenu;
