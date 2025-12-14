import React, { useEffect, ReactNode } from 'react';

interface ChatSelectionProps {
  children?: ReactNode;
  chapterId?: string;
}

/**
 * ChatSelection component - Handles text selection and dispatches events to ChatBot
 * Wraps chapter content and enables text selection for chat queries.
 * The actual chat UI is handled by the ChatBot component.
 */
const ChatSelection: React.FC<ChatSelectionProps> = ({ children, chapterId }) => {
  useEffect(() => {
    let selectionTimeout: NodeJS.Timeout | null = null;

    const handleMouseUp = () => {
      // Clear any existing timeout
      if (selectionTimeout) {
        clearTimeout(selectionTimeout);
      }

      // Small delay to ensure selection is complete
      selectionTimeout = setTimeout(() => {
        const selection = window.getSelection();
        const selectedText = selection?.toString().trim();

        if (selectedText && selectedText.length > 3) {
          // Dispatch custom event that ChatBot listens for
          const event = new CustomEvent('chatbot-selection-query', {
            detail: {
              text: selectedText,
              chapterId: chapterId
            }
          });
          window.dispatchEvent(event);
        }
      }, 300);
    };

    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
      if (selectionTimeout) {
        clearTimeout(selectionTimeout);
      }
    };
  }, [chapterId]);

  // If no children, just attach the event listener globally (used as side-effect component)
  // If children provided, wrap them in a div
  if (!children) {
    return null;
  }
  return <div className="chat-selection-wrapper">{children}</div>;
};

export default ChatSelection;
