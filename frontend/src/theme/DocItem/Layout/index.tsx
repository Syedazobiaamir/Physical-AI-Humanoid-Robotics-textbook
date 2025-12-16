import React from 'react';
import Layout from '@theme-original/DocItem/Layout';
import type LayoutType from '@theme/DocItem/Layout';
import type { WrapperProps } from '@docusaurus/types';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { useDoc } from '@docusaurus/plugin-content-docs/client';

type Props = WrapperProps<typeof LayoutType>;

// Lazy load components
const TranslateUrdu = React.lazy(() => import('@site/src/components/TranslateUrdu'));
const ChatBot = React.lazy(() => import('@site/src/components/ChatBot'));
const ChatSelection = React.lazy(() => import('@site/src/components/ChatSelection'));

function ChapterTools({ chapterId }: { chapterId: string }) {
  return (
    <React.Suspense fallback={<div style={{ height: '60px' }} />}>
      <div className="chapter-tools" style={{ marginBottom: '1.5rem' }}>
        <TranslateUrdu chapterId={chapterId} />
      </div>
      <ChatSelection />
      <ChatBot chapterId={chapterId} />
    </React.Suspense>
  );
}

export default function LayoutWrapper(props: Props): JSX.Element {
  const { metadata } = useDoc();
  const fullId = metadata?.id || '';
  const chapterId = fullId.includes('/') ? fullId.split('/').pop() || '' : fullId;

  return (
    <>
      {/* Inject TranslateUrdu button at the TOP of the page */}
      <BrowserOnly fallback={null}>
        {() => (
          <div style={{
            maxWidth: 'var(--ifm-container-width-xl)',
            margin: '0 auto',
            padding: '1rem 1rem 0 1rem'
          }}>
            <React.Suspense fallback={null}>
              <TranslateUrdu chapterId={chapterId} />
            </React.Suspense>
          </div>
        )}
      </BrowserOnly>

      {/* Original Layout */}
      <Layout {...props} />

      {/* ChatBot and Selection (floating) */}
      <BrowserOnly fallback={null}>
        {() => (
          <React.Suspense fallback={null}>
            <ChatSelection />
            <ChatBot chapterId={chapterId} />
          </React.Suspense>
        )}
      </BrowserOnly>
    </>
  );
}
