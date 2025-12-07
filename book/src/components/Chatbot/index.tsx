import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';

interface ChatMessage {
  sender: 'user' | 'ai';
  text: string;
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [selectedText, setSelectedText] = useState<string | null>(null); // New state for selected text
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Generate a unique session ID for the user
  const [sessionId, setSessionId] = useState<string>('');

  useEffect(() => {
    // Generate a new session ID when the component mounts
    setSessionId(`session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`);

    // Event listener for text selection
    const handleMouseUp = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().length > 0) {
        setSelectedText(selection.toString());
      } else {
        setSelectedText(null);
      }
    };

    window.addEventListener('mouseup', handleMouseUp);
    return () => {
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (inputMessage.trim() === '' && !selectedText) return; // Allow sending selected text alone

    const userQuery = inputMessage.trim() === '' ? (selectedText || 'Ask about selected text') : inputMessage;

    const newUserMessage: ChatMessage = { sender: 'user', text: userQuery };
    setMessages((prevMessages) => [...prevMessages, newUserMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Use environment variable for backend URL, fallback to localhost for development
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'; 
      const response = await fetch(`${backendUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: userQuery, 
          session_id: sessionId,
          selected_text: selectedText // Include selected text in the payload
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const newAiMessage: ChatMessage = { sender: 'ai', text: data.response };
      setMessages((prevMessages) => [...prevMessages, newAiMessage]);
      setSelectedText(null); // Clear selected text after sending
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: ChatMessage = { sender: 'ai', text: 'Oops! Something went wrong. Please try again.' };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      <div className={styles.chatHeader}>Book Chatbot</div>
      <div className={styles.chatMessages}>
        {messages.map((msg, index) => (
          <div key={index} className={`${styles.chatMessage} ${styles[msg.sender]}`}>
            {msg.text}
          </div>
        ))}
        {isLoading && (
          <div className={`${styles.chatMessage} ${styles.ai}`}>
            <div className={styles.loadingDots}>
              <span>.</span><span>.</span><span>.</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className={styles.chatInputContainer}>
        <input
          type="text"
          className={styles.chatInput}
          placeholder="Ask me about the book..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
        />
        <button className={styles.sendButton} onClick={sendMessage} disabled={isLoading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
