/**
 * Client module to inject Clerk publishable key
 * This runs on the client side before React renders
 */

import siteConfig from '@generated/docusaurus.config';

// Inject Clerk key into window for access by components
if (typeof window !== 'undefined') {
  const clerkKey = (siteConfig.customFields?.clerkPublishableKey as string) || '';
  if (clerkKey) {
    (window as any).__CLERK_PUBLISHABLE_KEY__ = clerkKey;
    console.log('Clerk initialized');
  }
}

export default function clerkInit() {
  // This function is called by Docusaurus client module system
  // The actual initialization happens above at module load time
}
