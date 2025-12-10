import React, { useState, useEffect, useRef } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import BrowserOnly from '@docusaurus/BrowserOnly';
import config from '../../utils/config';
import './Chatbot.css';

const ChatbotContent = ({ backendUrl = config.BACKEND_URL }) => {
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState(null);

    const messagesEndRef = useRef(null);
    const { colorMode } = useColorMode();

    useEffect(() => {
      const savedSessionId = typeof window !== 'undefined'
        ? localStorage.getItem('chatbot_session_id')
        : null;

      if (savedSessionId) {
        setSessionId(savedSessionId);
      } else {
        const newSessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        if (typeof window !== 'undefined') {
          localStorage.setItem('chatbot_session_id', newSessionId);
        }
        setSessionId(newSessionId);
      }
    }, []);

    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
      scrollToBottom();
    }, [messages]);

    const handleSendMessage = async () => {
      if (!inputText.trim() || isLoading || !sessionId) return;

      const userMessage = {
        id: Date.now(),
        text: inputText,
        sender: 'user',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, userMessage]);
      setInputText('');
      setIsLoading(true);

      try {
        const selectedText = typeof window !== 'undefined'
          ? window.getSelection()?.toString().trim()
          : '';

        const response = await fetch(`${backendUrl}/api/v1/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: inputText,
            session_id: sessionId,
            context_text: selectedText || null
          }),
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);

        const data = await response.json();

        const botMessage = {
          id: Date.now() + 1,
          text: data.response,
          sender: 'bot',
          sources: data.sources || [],
          timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, botMessage]);
      } catch (error) {
        console.error('Error sending message:', error);
        const errorMessage = {
          id: Date.now() + 1,
          text: 'Sorry, I encountered an error processing your request. Please try again.',
          sender: 'bot',
          isError: true,
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    };

    const handleKeyPress = (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSendMessage();
      }
    };

    const clearChat = () => {
      setMessages([]);
    };

    if (!sessionId) return <div>Loading chatbot...</div>;

    return (
      <div className={`chatbot-container ${colorMode}`}>
        <div className="chatbot-header">
          <h3>🤖 Robotics Book Assistant</h3>
          <button className="clear-chat-btn" onClick={clearChat} title="Clear chat">
            🗑️
          </button>
        </div>

        <div className="chatbot-messages">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <p>Hello! I'm your Robotics Book Assistant.</p>
              <p>Ask me questions about the book content, or select text on the page for context-aware Q&A.</p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
              >
                <div className="message-content">
                  <div className="message-text">{message.text}</div>
                  {message.sources && message.sources.length > 0 && (
                    <div className="message-sources">
                      <small>Sources: {message.sources.map(s => s.title).join(', ')}</small>
                    </div>
                  )}
                  {message.isError && (
                    <div className="error-message">
                      <small>Please check your connection or try again.</small>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="message bot-message">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chatbot-input">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about the book..."
            rows="2"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isLoading}
          >
            Send
          </button>
        </div>
      </div>
    );
  };

const Chatbot = ({ backendUrl = config.BACKEND_URL }) => {
  return (
    <BrowserOnly>
      {() => <ChatbotContent backendUrl={backendUrl} />}
    </BrowserOnly>
  );
};

export default Chatbot;