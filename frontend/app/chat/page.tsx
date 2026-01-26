'use client';

import React, { useState, useRef } from 'react';

const ChatPage = () => {
  const [messages, setMessages] = useState<{ id: number; text: string; sender: 'user' | 'ai' }[]>([
    { id: 1, text: 'Hello! I\'m your AI task assistant. How can I help you manage your tasks today?', sender: 'ai' }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputText.trim()) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      text: inputText,
      sender: 'user' as const
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // In a real implementation, this would call the AI agent API
      // For now, we'll simulate a response
      setTimeout(() => {
        const aiMessage = {
          id: messages.length + 2,
          text: `I've processed your request: "${inputText}". In a real implementation, I would connect to the AI agent to create, update, or manage your tasks based on your natural language input.`,
          sender: 'ai' as const
        };

        setMessages(prev => [...prev, aiMessage]);
        setIsLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error sending message:', error);
      setIsLoading(false);

      const errorMessage = {
        id: messages.length + 2,
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'ai' as const
      };

      setMessages(prev => [...prev, errorMessage]);
    }
  };

  return (
    <div className="chat-page">
      <div className="card">
        <div className="card-header">
          <h1 className="card-title d-flex align-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            AI Task Assistant
          </h1>
          <p className="text-muted mb-0">Natural language task management with AI</p>
        </div>

        <div className="chat-container">
          <div className="chat-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender}`}
              >
                <div className="d-flex align-center gap-2">
                  {message.sender === 'ai' && (
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginTop: '0.25rem' }}>
                      <path d="M12 8V4H8"/>
                      <circle cx="16" cy="4" r="1"/>
                      <path d="M12 2v4h4"/>
                      <path d="m22 13-1.23-1.23a1.46 1.46 0 0 0-2.37.39c-.06.23-.09.47-.09.72v1.72a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h12c.25 0 .49.03.72.09a1.46 1.46 0 0 1 .39 2.37L13 13"/>
                    </svg>
                  )}
                  {message.sender === 'user' && (
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginTop: '0.25rem' }}>
                      <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                  )}
                  <div className="message-text">{message.text}</div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message ai">
                <div className="d-flex align-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginTop: '0.25rem' }}>
                    <path d="M12 8V4H8"/>
                    <circle cx="16" cy="4" r="1"/>
                    <path d="M12 2v4h4"/>
                    <path d="m22 13-1.23-1.23a1.46 1.46 0 0 0-2.37.39c-.06.23-.09.47-.09.72v1.72a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h12c.25 0 .49.03.72.09a1.46 1.46 0 0 1 .39 2.37L13 13"/>
                  </svg>
                  <div className="message-text d-flex align-center gap-2">
                    <div className="spinner" style={{ width: '14px', height: '14px' }}></div>
                    Thinking...
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="chat-input-form">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Type your task request (e.g., 'Add meeting with team tomorrow at 10am')..."
              className="form-control"
              disabled={isLoading}
            />
            <button type="submit" className="btn btn-primary" disabled={isLoading}>
              {isLoading ? (
                <>
                  <div className="spinner" style={{ width: '16px', height: '16px' }}></div>
                  Sending...
                </>
              ) : (
                <>
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="m22 2-7 20-4-9-9-4Z"/>
                  </svg>
                  Send
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;