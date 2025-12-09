import React, { useState, useRef, useEffect, useCallback } from 'react';
import styles from './ChatBot.module.css';
import { API_BASE_URL } from '@site/src/config/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  timestamp: Date;
}

interface ChatBotProps {
  chapterId?: string;
  apiBaseUrl?: string;
}

export default function ChatBot({
  chapterId,
  apiBaseUrl = API_BASE_URL
}: ChatBotProps): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const [contextMode, setContextMode] = useState<'selection' | 'general'>('general');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Listen for text selection events from ChatSelection component
  useEffect(() => {
    const handleSelectionQuery = (event: CustomEvent<{ text: string }>) => {
      setSelectedText(event.detail.text);
      setContextMode('selection');
      setIsOpen(true);
    };

    window.addEventListener('chatbot-selection-query', handleSelectionQuery as EventListener);
    return () => {
      window.removeEventListener('chatbot-selection-query', handleSelectionQuery as EventListener);
    };
  }, []);

  const generateId = () => Math.random().toString(36).substring(2, 9);

  const sendMessage = useCallback(async () => {
    const query = inputValue.trim();
    if (!query && !selectedText) return;

    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content: selectedText
        ? `[Selected text]: "${selectedText}"\n\nQuestion: ${query || 'Explain this'}`
        : query,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch(`${apiBaseUrl}/rag/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query || 'Explain this selected text',
          context_mode: contextMode,
          selected_text: selectedText || undefined,
          // Don't filter by chapter_id to allow searching across all chapters
          // chapter_id: chapterId || undefined,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: generateId(),
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: generateId(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
      console.error('ChatBot error:', error);
    } finally {
      setIsLoading(false);
      setSelectedText(null);
      setContextMode('general');
    }
  }, [inputValue, selectedText, contextMode, chapterId, apiBaseUrl]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearSelection = () => {
    setSelectedText(null);
    setContextMode('general');
  };

  const clearChat = () => {
    setMessages([]);
    setSelectedText(null);
    setContextMode('general');
  };

  return (
    <>
      {/* Floating toggle button */}
      <button
        className={`${styles.toggleButton} ${isOpen ? styles.hidden : ''}`}
        onClick={() => setIsOpen(true)}
        aria-label="Open chat"
      >
        <ChatIcon />
      </button>

      {/* Chat widget */}
      <div className={`${styles.widget} ${isOpen ? styles.open : ''}`}>
        {/* Header */}
        <div className={styles.header}>
          <div className={styles.headerTitle}>
            <BotIcon />
            <span>AI Assistant</span>
          </div>
          <div className={styles.headerActions}>
            <button
              className={styles.headerButton}
              onClick={clearChat}
              aria-label="Clear chat"
              title="Clear chat"
            >
              <TrashIcon />
            </button>
            <button
              className={styles.headerButton}
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              <CloseIcon />
            </button>
          </div>
        </div>

        {/* Messages area */}
        <div className={styles.messages}>
          {messages.length === 0 && (
            <div className={styles.welcome}>
              <BotIcon />
              <h3>How can I help you?</h3>
              <p>Ask questions about the chapter content, or select text on the page for focused explanations.</p>
              <div className={styles.suggestions}>
                <button onClick={() => setInputValue('What is ROS2?')}>
                  What is ROS2?
                </button>
                <button onClick={() => setInputValue('Explain nodes and topics')}>
                  Explain nodes and topics
                </button>
                <button onClick={() => setInputValue('How do I set up Gazebo?')}>
                  How do I set up Gazebo?
                </button>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`${styles.message} ${styles[message.role]}`}
            >
              <div className={styles.messageContent}>
                {message.content}
              </div>
              {message.sources && message.sources.length > 0 && (
                <div className={styles.sources}>
                  <span className={styles.sourcesLabel}>Sources:</span>
                  {message.sources.map((source, idx) => (
                    <span key={idx} className={styles.source}>{source}</span>
                  ))}
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className={`${styles.message} ${styles.assistant}`}>
              <div className={styles.typing}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Selected text indicator */}
        {selectedText && (
          <div className={styles.selectionIndicator}>
            <span className={styles.selectionLabel}>Selected text:</span>
            <span className={styles.selectionText}>
              {selectedText.length > 50
                ? `${selectedText.substring(0, 50)}...`
                : selectedText}
            </span>
            <button onClick={clearSelection} className={styles.clearSelection}>
              <CloseIcon />
            </button>
          </div>
        )}

        {/* Input area */}
        <div className={styles.inputArea}>
          <textarea
            ref={inputRef}
            className={styles.input}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={selectedText ? "Ask about the selected text..." : "Ask a question..."}
            rows={1}
            disabled={isLoading}
          />
          <button
            className={styles.sendButton}
            onClick={sendMessage}
            disabled={isLoading || (!inputValue.trim() && !selectedText)}
            aria-label="Send message"
          >
            <SendIcon />
          </button>
        </div>
      </div>
    </>
  );
}

// Icon components
function ChatIcon() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  );
}

function BotIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="11" width="18" height="10" rx="2" />
      <circle cx="12" cy="5" r="2" />
      <path d="M12 7v4" />
      <line x1="8" y1="16" x2="8" y2="16" />
      <line x1="16" y1="16" x2="16" y2="16" />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  );
}

function TrashIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="3,6 5,6 21,6" />
      <path d="M19,6v14a2,2 0 0,1-2,2H7a2,2 0 0,1-2-2V6m3,0V4a2,2 0 0,1,2-2h4a2,2 0 0,1,2,2v2" />
    </svg>
  );
}

function SendIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="22" y1="2" x2="11" y2="13" />
      <polygon points="22,2 15,22 11,13 2,9" />
    </svg>
  );
}
