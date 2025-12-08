import React, { useState, useRef, useEffect, ReactNode } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
}

interface ChatSelectionProps {
  chapterId: string;
  children: ReactNode;
}

const ChatSelection: React.FC<ChatSelectionProps> = ({ chapterId, children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [selectedText, setSelectedText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [contextMode, setContextMode] = useState<'selection' | 'general'>('general');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Add selection listener to content area
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim()) {
        setSelectedText(selection.toString().trim());
        setContextMode('selection');
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/rag/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: input,
          context_mode: contextMode,
          selected_text: contextMode === 'selection' ? selectedText : undefined,
          chapter_id: chapterId,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.answer,
          sources: data.sources,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } else {
        // Handle error with fallback response
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: getFallbackResponse(input, selectedText, contextMode),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (err) {
      // Fallback for offline mode
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: getFallbackResponse(input, selectedText, contextMode),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } finally {
      setIsLoading(false);
      setSelectedText('');
      setContextMode('general');
    }
  };

  const getFallbackResponse = (
    query: string,
    selected: string,
    mode: 'selection' | 'general'
  ): string => {
    if (mode === 'selection' && selected) {
      return `I understand you're asking about: "${selected.substring(0, 100)}${selected.length > 100 ? '...' : ''}"\n\nIn the context of ${chapterId}, this relates to the concepts covered in this chapter. For a detailed explanation, please ensure the backend RAG service is running.\n\n**Tip:** The RAG chatbot provides AI-powered answers based on the textbook content. Start the backend server to enable full functionality.`;
    }

    return `Thank you for your question about "${query}".\n\nTo get AI-powered answers based on the textbook content, please ensure the backend RAG service is running at http://localhost:8000.\n\n**Getting Started:**\n1. Navigate to the backend directory\n2. Run \`python -m uvicorn src.main:app --reload\`\n3. Try asking your question again`;
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearSelection = () => {
    setSelectedText('');
    setContextMode('general');
  };

  return (
    <div className="chat-selection-wrapper">
      <div ref={contentRef} className="chapter-content">
        {children}
      </div>

      {/* Floating chat button */}
      <button
        className="chat-toggle-btn"
        onClick={() => setIsOpen(!isOpen)}
        title="Ask AI Assistant"
      >
        {isOpen ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
        )}
      </button>

      {/* Chat widget */}
      {isOpen && (
        <div className="chat-widget">
          <div className="chat-header">
            <span>AI Assistant</span>
            <span className="chat-chapter-context">Chapter: {chapterId}</span>
          </div>

          {selectedText && (
            <div className="chat-selection-context">
              <div className="selection-label">
                <span>Selected text:</span>
                <button onClick={clearSelection} className="clear-selection-btn">
                  Clear
                </button>
              </div>
              <div className="selection-text">
                "{selectedText.substring(0, 150)}
                {selectedText.length > 150 ? '...' : ''}"
              </div>
            </div>
          )}

          <div className="chat-messages">
            {messages.length === 0 && (
              <div className="chat-welcome">
                <h4>Welcome to the AI Assistant!</h4>
                <p>
                  Ask questions about this chapter or select text in the content
                  above to get contextual explanations.
                </p>
                <div className="chat-suggestions">
                  <strong>Try asking:</strong>
                  <ul>
                    <li>Explain the main concepts in this chapter</li>
                    <li>What are the key learning objectives?</li>
                    <li>Give me a summary of the lab tasks</li>
                  </ul>
                </div>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`chat-message ${message.role === 'user' ? 'user' : 'assistant'}`}
              >
                <div className="message-content">{message.content}</div>
                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <strong>Sources:</strong>
                    <ul>
                      {message.sources.map((source, index) => (
                        <li key={index}>{source}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="chat-message assistant">
                <div className="message-loading">
                  <span className="loading-dot"></span>
                  <span className="loading-dot"></span>
                  <span className="loading-dot"></span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-container">
            <textarea
              className="chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={
                selectedText
                  ? 'Ask about the selected text...'
                  : 'Ask a question about this chapter...'
              }
              rows={2}
            />
            <button
              className="chat-send-btn"
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
        </div>
      )}

      <style>{`
        .chat-selection-wrapper {
          position: relative;
        }

        .chapter-content {
          /* Content inherits normal styling */
        }

        .chat-toggle-btn {
          position: fixed;
          bottom: 2rem;
          right: 2rem;
          width: 56px;
          height: 56px;
          border-radius: 50%;
          background: var(--ifm-color-primary);
          color: white;
          border: none;
          cursor: pointer;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
          z-index: 1000;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: transform 0.2s, box-shadow 0.2s;
        }

        .chat-toggle-btn:hover {
          transform: scale(1.05);
          box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
        }

        .chat-widget {
          position: fixed;
          bottom: 6rem;
          right: 2rem;
          width: 400px;
          max-height: 600px;
          background: var(--ifm-background-color);
          border: 1px solid var(--ifm-color-emphasis-300);
          border-radius: 12px;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
          z-index: 999;
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }

        @media (max-width: 768px) {
          .chat-widget {
            width: calc(100% - 2rem);
            right: 1rem;
            bottom: 5rem;
            max-height: 70vh;
          }
        }

        .chat-header {
          padding: 1rem;
          background: var(--ifm-color-primary);
          color: white;
          font-weight: 600;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .chat-chapter-context {
          font-size: 0.8rem;
          opacity: 0.9;
        }

        .chat-selection-context {
          padding: 0.75rem 1rem;
          background: var(--ifm-color-emphasis-100);
          border-bottom: 1px solid var(--ifm-color-emphasis-200);
        }

        .selection-label {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.5rem;
          font-size: 0.85rem;
          color: var(--ifm-color-emphasis-600);
        }

        .clear-selection-btn {
          background: none;
          border: none;
          color: var(--ifm-color-primary);
          cursor: pointer;
          font-size: 0.85rem;
        }

        .selection-text {
          font-size: 0.9rem;
          font-style: italic;
          color: var(--ifm-font-color-base);
        }

        .chat-messages {
          flex: 1;
          overflow-y: auto;
          padding: 1rem;
          min-height: 200px;
          max-height: 400px;
        }

        .chat-welcome {
          color: var(--ifm-color-emphasis-600);
        }

        .chat-welcome h4 {
          margin: 0 0 0.5rem 0;
          color: var(--ifm-font-color-base);
        }

        .chat-welcome p {
          margin-bottom: 1rem;
        }

        .chat-suggestions {
          background: var(--ifm-color-emphasis-100);
          padding: 0.75rem;
          border-radius: 6px;
          font-size: 0.9rem;
        }

        .chat-suggestions ul {
          margin: 0.5rem 0 0 1rem;
          padding: 0;
        }

        .chat-suggestions li {
          margin-bottom: 0.25rem;
        }

        .chat-message {
          margin-bottom: 1rem;
          padding: 0.75rem 1rem;
          border-radius: 8px;
          max-width: 85%;
        }

        .chat-message.user {
          background: var(--ifm-color-primary);
          color: white;
          margin-left: auto;
        }

        .chat-message.assistant {
          background: var(--ifm-color-emphasis-100);
          margin-right: auto;
        }

        .message-content {
          white-space: pre-wrap;
          word-wrap: break-word;
        }

        .message-sources {
          margin-top: 0.75rem;
          padding-top: 0.75rem;
          border-top: 1px solid var(--ifm-color-emphasis-200);
          font-size: 0.85rem;
        }

        .message-sources ul {
          margin: 0.25rem 0 0 1rem;
          padding: 0;
        }

        .message-loading {
          display: flex;
          gap: 4px;
        }

        .loading-dot {
          width: 8px;
          height: 8px;
          background: var(--ifm-color-emphasis-400);
          border-radius: 50%;
          animation: bounce 1.4s infinite ease-in-out both;
        }

        .loading-dot:nth-child(1) {
          animation-delay: -0.32s;
        }

        .loading-dot:nth-child(2) {
          animation-delay: -0.16s;
        }

        @keyframes bounce {
          0%, 80%, 100% {
            transform: scale(0);
          }
          40% {
            transform: scale(1);
          }
        }

        .chat-input-container {
          padding: 1rem;
          border-top: 1px solid var(--ifm-color-emphasis-200);
          display: flex;
          gap: 0.5rem;
        }

        .chat-input {
          flex: 1;
          padding: 0.75rem;
          border: 1px solid var(--ifm-color-emphasis-300);
          border-radius: 6px;
          resize: none;
          font-family: inherit;
          font-size: 0.95rem;
          background: var(--ifm-background-color);
          color: var(--ifm-font-color-base);
        }

        .chat-input:focus {
          outline: none;
          border-color: var(--ifm-color-primary);
        }

        .chat-send-btn {
          padding: 0.75rem;
          background: var(--ifm-color-primary);
          color: white;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: opacity 0.2s;
        }

        .chat-send-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .chat-send-btn:hover:not(:disabled) {
          opacity: 0.9;
        }
      `}</style>
    </div>
  );
};

export default ChatSelection;
