import React, { useState, useRef, useEffect } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  sources?: string[];
  timestamp: Date;
}

interface ChatWidgetProps {
  chapterId?: string;
  initialOpen?: boolean;
  position?: 'bottom-right' | 'bottom-left';
}

const ChatWidget: React.FC<ChatWidgetProps> = ({
  chapterId,
  initialOpen = false,
  position = 'bottom-right',
}) => {
  const [isOpen, setIsOpen] = useState(initialOpen);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen) {
      checkHealth();
      inputRef.current?.focus();
    }
  }, [isOpen]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const checkHealth = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/rag/health');
      if (response.ok) {
        const data = await response.json();
        setIsHealthy(data.status === 'healthy');
      } else {
        setIsHealthy(false);
      }
    } catch (err) {
      setIsHealthy(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
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
          query: userMessage.content,
          context_mode: 'general',
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
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } else {
        throw new Error('Failed to get response');
      }
    } catch (err) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'system',
        content: 'Sorry, I encountered an error. Please make sure the backend server is running and try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const positionStyles = position === 'bottom-right'
    ? { right: '2rem' }
    : { left: '2rem' };

  return (
    <>
      {/* Toggle Button */}
      <button
        className="chat-widget-toggle"
        onClick={() => setIsOpen(!isOpen)}
        style={positionStyles}
        title={isOpen ? 'Close chat' : 'Ask AI Assistant'}
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
        {!isOpen && messages.length > 0 && (
          <span className="chat-badge">{messages.length}</span>
        )}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-widget-window" style={positionStyles}>
          {/* Header */}
          <div className="chat-widget-header">
            <div className="chat-widget-title">
              <span>AI Assistant</span>
              {isHealthy !== null && (
                <span className={`health-indicator ${isHealthy ? 'healthy' : 'unhealthy'}`}>
                  {isHealthy ? 'Online' : 'Offline'}
                </span>
              )}
            </div>
            <div className="chat-widget-actions">
              <button onClick={clearChat} title="Clear chat" className="chat-action-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="m19 6-.867 12.142A2 2 0 0116.138 20H7.862a2 2 0 01-1.995-1.858L5 6m5 0V4a1 1 0 011-1h2a1 1 0 011 1v2"></path>
                </svg>
              </button>
              <button onClick={() => setIsOpen(false)} title="Close" className="chat-action-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="chat-widget-messages">
            {messages.length === 0 && (
              <div className="chat-widget-welcome">
                <div className="welcome-icon">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"></path>
                    <line x1="12" y1="17" x2="12.01" y2="17"></line>
                  </svg>
                </div>
                <h4>How can I help you?</h4>
                <p>Ask me anything about Physical AI and Humanoid Robotics.</p>
                <div className="welcome-suggestions">
                  <button onClick={() => setInput('Explain the basics of ROS2')}>
                    Explain ROS2 basics
                  </button>
                  <button onClick={() => setInput('What is SLAM?')}>
                    What is SLAM?
                  </button>
                  <button onClick={() => setInput('How does a PID controller work?')}>
                    PID controller
                  </button>
                </div>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`chat-widget-message ${message.role}`}
              >
                <div className="message-content">
                  {message.content}
                </div>
                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <span className="sources-label">Sources:</span>
                    {message.sources.map((source, idx) => (
                      <span key={idx} className="source-tag">{source}</span>
                    ))}
                  </div>
                )}
                <div className="message-time">{formatTime(message.timestamp)}</div>
              </div>
            ))}

            {isLoading && (
              <div className="chat-widget-message assistant loading">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="chat-widget-input">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your question..."
              rows={1}
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
              className="send-button"
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
        .chat-widget-toggle {
          position: fixed;
          bottom: 2rem;
          width: 56px;
          height: 56px;
          border-radius: 50%;
          background: var(--ifm-color-primary, #2e8555);
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

        .chat-widget-toggle:hover {
          transform: scale(1.05);
          box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
        }

        .chat-badge {
          position: absolute;
          top: -4px;
          right: -4px;
          background: #dc3545;
          color: white;
          font-size: 12px;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .chat-widget-window {
          position: fixed;
          bottom: 6rem;
          width: 380px;
          max-height: 550px;
          background: var(--ifm-background-color, #fff);
          border: 1px solid var(--ifm-color-emphasis-300, #ddd);
          border-radius: 12px;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
          z-index: 999;
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }

        @media (max-width: 768px) {
          .chat-widget-window {
            width: calc(100% - 2rem);
            right: 1rem !important;
            left: 1rem !important;
            bottom: 5rem;
            max-height: 60vh;
          }
        }

        .chat-widget-header {
          padding: 0.875rem 1rem;
          background: var(--ifm-color-primary, #2e8555);
          color: white;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .chat-widget-title {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-weight: 600;
        }

        .health-indicator {
          font-size: 0.7rem;
          padding: 0.15rem 0.4rem;
          border-radius: 10px;
          font-weight: 400;
        }

        .health-indicator.healthy {
          background: rgba(255, 255, 255, 0.2);
        }

        .health-indicator.unhealthy {
          background: rgba(220, 53, 69, 0.5);
        }

        .chat-widget-actions {
          display: flex;
          gap: 0.5rem;
        }

        .chat-action-btn {
          background: transparent;
          border: none;
          color: white;
          cursor: pointer;
          padding: 0.25rem;
          opacity: 0.8;
          transition: opacity 0.2s;
        }

        .chat-action-btn:hover {
          opacity: 1;
        }

        .chat-widget-messages {
          flex: 1;
          overflow-y: auto;
          padding: 1rem;
          min-height: 250px;
          max-height: 350px;
        }

        .chat-widget-welcome {
          text-align: center;
          padding: 1.5rem 0.5rem;
          color: var(--ifm-color-emphasis-600, #666);
        }

        .welcome-icon {
          margin-bottom: 1rem;
          color: var(--ifm-color-primary, #2e8555);
        }

        .chat-widget-welcome h4 {
          margin: 0 0 0.5rem 0;
          color: var(--ifm-font-color-base, #333);
        }

        .chat-widget-welcome p {
          margin: 0 0 1rem 0;
          font-size: 0.9rem;
        }

        .welcome-suggestions {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          justify-content: center;
        }

        .welcome-suggestions button {
          background: var(--ifm-color-emphasis-100, #f5f5f5);
          border: 1px solid var(--ifm-color-emphasis-200, #eee);
          padding: 0.4rem 0.75rem;
          border-radius: 15px;
          font-size: 0.8rem;
          cursor: pointer;
          transition: background 0.2s;
        }

        .welcome-suggestions button:hover {
          background: var(--ifm-color-emphasis-200, #eee);
        }

        .chat-widget-message {
          margin-bottom: 0.75rem;
          max-width: 85%;
        }

        .chat-widget-message.user {
          margin-left: auto;
        }

        .chat-widget-message.assistant,
        .chat-widget-message.system {
          margin-right: auto;
        }

        .message-content {
          padding: 0.625rem 0.875rem;
          border-radius: 12px;
          font-size: 0.9rem;
          line-height: 1.4;
          white-space: pre-wrap;
          word-wrap: break-word;
        }

        .chat-widget-message.user .message-content {
          background: var(--ifm-color-primary, #2e8555);
          color: white;
          border-bottom-right-radius: 4px;
        }

        .chat-widget-message.assistant .message-content {
          background: var(--ifm-color-emphasis-100, #f5f5f5);
          border-bottom-left-radius: 4px;
        }

        .chat-widget-message.system .message-content {
          background: #fff3cd;
          color: #856404;
          font-size: 0.85rem;
        }

        .message-sources {
          margin-top: 0.5rem;
          font-size: 0.75rem;
          display: flex;
          flex-wrap: wrap;
          gap: 0.25rem;
          align-items: center;
        }

        .sources-label {
          color: var(--ifm-color-emphasis-500, #888);
        }

        .source-tag {
          background: var(--ifm-color-emphasis-200, #eee);
          padding: 0.15rem 0.4rem;
          border-radius: 4px;
          color: var(--ifm-color-emphasis-700, #555);
        }

        .message-time {
          font-size: 0.7rem;
          color: var(--ifm-color-emphasis-400, #999);
          margin-top: 0.25rem;
          text-align: right;
        }

        .chat-widget-message.assistant .message-time,
        .chat-widget-message.system .message-time {
          text-align: left;
        }

        .typing-indicator {
          display: flex;
          gap: 4px;
          padding: 0.625rem 0.875rem;
        }

        .typing-indicator span {
          width: 8px;
          height: 8px;
          background: var(--ifm-color-emphasis-400, #999);
          border-radius: 50%;
          animation: bounce 1.4s infinite ease-in-out both;
        }

        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }

        .chat-widget-input {
          padding: 0.75rem;
          border-top: 1px solid var(--ifm-color-emphasis-200, #eee);
          display: flex;
          gap: 0.5rem;
          align-items: flex-end;
        }

        .chat-widget-input textarea {
          flex: 1;
          padding: 0.625rem 0.875rem;
          border: 1px solid var(--ifm-color-emphasis-300, #ddd);
          border-radius: 20px;
          resize: none;
          font-family: inherit;
          font-size: 0.9rem;
          max-height: 100px;
          background: var(--ifm-background-color, #fff);
          color: var(--ifm-font-color-base, #333);
        }

        .chat-widget-input textarea:focus {
          outline: none;
          border-color: var(--ifm-color-primary, #2e8555);
        }

        .send-button {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background: var(--ifm-color-primary, #2e8555);
          color: white;
          border: none;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: opacity 0.2s;
        }

        .send-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .send-button:hover:not(:disabled) {
          opacity: 0.9;
        }
      `}</style>
    </>
  );
};

export default ChatWidget;
