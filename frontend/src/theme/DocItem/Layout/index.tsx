import React from 'react';
import Layout from '@theme-original/DocItem/Layout';
import type LayoutType from '@theme/DocItem/Layout';
import type { WrapperProps } from '@docusaurus/types';
import ChatBot from '@site/src/components/ChatBot';
import ChatSelection from '@site/src/components/ChatSelection';
import { useDoc } from '@docusaurus/plugin-content-docs/client';

type Props = WrapperProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): JSX.Element {
  const { metadata } = useDoc();
  // Extract just the filename from the full doc ID (e.g., "module-1/week-1-intro" -> "week-1-intro")
  const fullId = metadata?.id || '';
  const chapterId = fullId.includes('/') ? fullId.split('/').pop() : fullId;

  return (
    <>
      <Layout {...props} />
      <ChatSelection />
      <ChatBot chapterId={chapterId} />
    </>
  );
}
