import React from 'react';
import Content from '@theme-original/Navbar/Content';
import type ContentType from '@theme/Navbar/Content';
import type {WrapperProps} from '@docusaurus/types';
import BrowserOnly from '@docusaurus/BrowserOnly';
import styles from './styles.module.css';

type Props = WrapperProps<typeof ContentType>;

// Lazy load the auth components only in browser
function AuthButtons() {
  const [AuthProvider, setAuthProvider] = React.useState<React.ComponentType<any> | null>(null);
  const [UserMenu, setUserMenu] = React.useState<React.ComponentType<any> | null>(null);
  const [SignIn, setSignIn] = React.useState<React.ComponentType<any> | null>(null);
  const [isSignInOpen, setIsSignInOpen] = React.useState(false);

  React.useEffect(() => {
    Promise.all([
      import('@site/src/components/Auth/AuthProvider'),
      import('@site/src/components/Auth/UserMenu'),
      import('@site/src/components/Auth/SignIn'),
    ]).then(([authProviderModule, userMenuModule, signInModule]) => {
      setAuthProvider(() => authProviderModule.default);
      setUserMenu(() => userMenuModule.default);
      setSignIn(() => signInModule.default);
    });
  }, []);

  if (!AuthProvider || !UserMenu || !SignIn) {
    return (
      <div className={styles.authPlaceholder}>
        <span className={styles.signInPlaceholder}>Sign In</span>
      </div>
    );
  }

  return (
    <AuthProvider>
      <UserMenu onSignInClick={() => setIsSignInOpen(true)} />
      <SignIn
        isOpen={isSignInOpen}
        onClose={() => setIsSignInOpen(false)}
      />
    </AuthProvider>
  );
}

export default function ContentWrapper(props: Props): JSX.Element {
  return (
    <>
      <Content {...props} />
      <div className={styles.authButtons}>
        <BrowserOnly fallback={<div className={styles.authPlaceholder} />}>
          {() => <AuthButtons />}
        </BrowserOnly>
      </div>
    </>
  );
}
