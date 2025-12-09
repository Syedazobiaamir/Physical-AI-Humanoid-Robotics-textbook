import React, { useEffect } from 'react';

/**
 * ChatSelection component - Handles text selection and dispatches events to ChatBot
 * This component only handles selection detection and event emission.
 * The actual chat UI is handled by the ChatBot component.
 */
const ChatSelection: React.FC = () => {
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
            detail: { text: selectedText }
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
  }, []);

  // This component doesn't render any UI - it only handles selection events
  return null;
};

export default ChatSelection;
