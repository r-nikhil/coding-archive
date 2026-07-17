---
layout: page
title:  
permalink: /chat/
---


<div id="chat-container">
  <div id="chat-header">
    <h2>Chat with Nikhil</h2>
    <p>Ask me about AI, investing, poker, or anything else!</p>
    <div id="health-status">
      <span id="health-icon">●</span>
      <span id="health-text">Checking...</span>
    </div>
  </div>

  <div id="chat-messages"></div>

  <div id="chat-input-container">
    <textarea id="chat-input" placeholder="Type your message..." rows="3"></textarea>
    <button id="send-button">Send</button>
  </div>

  <div id="loading" style="display: none;">
    <div class="typing-indicator">
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>
</div>

<style>
:root {
  --chat-primary: #0066cc;
  --chat-primary-hover: #0056b3;
  --chat-background: #ffffff;
  --chat-user-bg: var(--chat-primary);
  --chat-bot-bg: #f8f9fa;
  --chat-border: #333333;
  --chat-text: #333333;
  --chat-text-light: #ffffff;
  --chat-shadow: 5px 5px 0px 0px var(--chat-border);
}

#chat-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  border: 3px solid var(--chat-border);
  box-shadow: var(--chat-shadow);
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  background: var(--chat-background);
  min-height: 600px;
  display: flex;
  flex-direction: column;
}

#chat-header {
  background: var(--chat-border);
  color: var(--chat-text-light);
  padding: 1rem;
  border-bottom: 3px solid var(--chat-border);
}

#chat-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5em;
}

#chat-header p {
  margin: 0;
  font-size: 1em;
  opacity: 0.9;
}

#health-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  font-size: 0.9em;
}

#health-icon {
  font-size: 1.2em;
  color: #666;
}

#health-icon.healthy {
  color: #00ff00;
}

#health-icon.unhealthy {
  color: #ff0000;
}

#health-text {
  opacity: 0.9;
}

#chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  min-height: 400px;
  max-height: 500px;
}

.message {
  margin-bottom: 1rem;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.message.user {
  justify-content: flex-end;
}

.message-content {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--chat-border);
  box-shadow: 2px 2px 0px 0px var(--chat-border);
  border-radius: 0;
  word-wrap: break-word;
}

.message.user .message-content {
  background: var(--chat-user-bg);
  color: var(--chat-text-light);
}

.message.bot .message-content {
  background: var(--chat-bot-bg);
  color: var(--chat-text);
}

.message-avatar {
  width: 32px;
  height: 32px;
  border: 2px solid var(--chat-border);
  background: var(--chat-border);
  color: var(--chat-text-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.8em;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: var(--chat-user-bg);
}

.message.bot .message-avatar {
  background: var(--chat-bot-bg);
  color: var(--chat-text);
}

#chat-input-container {
  padding: 1rem;
  border-top: 3px solid var(--chat-border);
  display: flex;
  gap: 0.5rem;
  align-items: flex-end;
}

#chat-input {
  flex: 1;
  border: 2px solid var(--chat-border);
  padding: 0.75rem;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 1em;
  resize: vertical;
  min-height: 60px;
  background: var(--chat-background);
  color: var(--chat-text);
}

#chat-input:focus {
  outline: none;
  box-shadow: 2px 2px 0px 0px var(--chat-border);
}

#send-button {
  border: 2px solid var(--chat-border);
  background: var(--chat-primary);
  color: var(--chat-text-light);
  padding: 0.75rem 1.5rem;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 2px 2px 0px 0px var(--chat-border);
}

#send-button:hover:not(:disabled) {
  background: var(--chat-primary-hover);
  transform: translate(-1px, -1px);
  box-shadow: 3px 3px 0px 0px var(--chat-border);
}

#send-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  align-items: center;
  padding: 1rem;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  background: var(--chat-text);
  border-radius: 50%;
  display: inline-block;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.error-message {
  background: #ffebee;
  color: #c62828;
  border: 2px solid #c62828;
  padding: 0.75rem;
  margin: 0.5rem 0;
  box-shadow: 2px 2px 0px 0px #c62828;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  #chat-container {
    margin: 0 1rem;
    min-height: 500px;
  }

  .message-content {
    max-width: 85%;
  }

  #chat-input-container {
    flex-direction: column;
    gap: 0.75rem;
  }

  #send-button {
    align-self: stretch;
  }
}
</style>

<script>
class ChatInterface {
  constructor() {
    this.apiUrl = 'https://llm-chat-backend-nikhilr24.replit.app/api/chat';
    this.healthUrl = 'https://llm-chat-backend-nikhilr24.replit.app/api/health';
    this.messagesContainer = document.getElementById('chat-messages');
    this.chatInput = document.getElementById('chat-input');
    this.sendButton = document.getElementById('send-button');
    this.loadingIndicator = document.getElementById('loading');
    this.healthIcon = document.getElementById('health-icon');
    this.healthText = document.getElementById('health-text');

    this.init();
  }

  init() {
    this.sendButton.addEventListener('click', () => {
      console.log('Send button clicked');
      this.sendMessage();
    });
    
    this.chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        console.log('Enter key pressed');
        this.sendMessage();
      }
    });

    // Check backend health on load
    this.checkHealth();

    // Initial welcome message
    this.addMessage('bot', "Hey there! I'm Nikhil. Ask me anything about AI, poker, or my projects!");
  }

  async checkHealth() {
    try {
      console.log('Checking health at:', this.healthUrl);
      const response = await fetch(this.healthUrl, {
        method: 'GET'
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Health check response:', data);
        
        if (data.status === 'healthy') {
          this.updateHealthStatus(true, 'Backend Online');
        } else {
          this.updateHealthStatus(false, 'Backend Unhealthy');
        }
      } else {
        console.error('Health check failed:', response.status);
        this.updateHealthStatus(false, 'Backend Offline');
      }
    } catch (error) {
      console.error('Health check error:', error);
      this.updateHealthStatus(false, 'Backend Offline');
    }
  }

  updateHealthStatus(isHealthy, statusText) {
    this.healthIcon.className = isHealthy ? 'healthy' : 'unhealthy';
    this.healthText.textContent = statusText;
  }

  async sendMessage() {
    const message = this.chatInput.value.trim();
    if (!message) return;

    console.log('Sending message:', message);
    
    // Add user message to chat
    this.addMessage('user', message);
    this.chatInput.value = '';
    this.setLoading(true);

    try {
      console.log('Making request to:', this.apiUrl);
      
      const response = await fetch(this.apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          timestamp: new Date().toISOString()
        })
      });

      console.log('Response status:', response.status);
      console.log('Response ok:', response.ok);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Server error response:', errorText);
        throw new Error('Server error: ' + response.status + ' - ' + errorText);
      }

      const data = await response.json();
      console.log('Response data:', data);
      
      this.addMessage('bot', data.response || 'Sorry, I encountered an error processing your message.');

    } catch (error) {
      console.error('Chat error:', error);
      
      // More specific error messages
      if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
        this.addMessage('bot', 'Error: Cannot connect to backend server. The chat service may be down or the URL may be incorrect.');
      } else if (error.message.includes('Server error: 404')) {
        this.addMessage('bot', 'Error: Chat endpoint not found. Please check if the backend is running correctly.');
      } else if (error.message.includes('Server error: 500')) {
        this.addMessage('bot', 'Error: Backend server error. Please try again in a moment.');
      } else {
        this.addMessage('bot', 'Error: ' + error.message);
      }
    } finally {
      this.setLoading(false);
    }
  }

  addMessage(sender, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + sender;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? 'U' : 'N';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;

    if (sender === 'user') {
      messageDiv.appendChild(messageContent);
      messageDiv.appendChild(avatar);
    } else {
      messageDiv.appendChild(avatar);
      messageDiv.appendChild(messageContent);
    }

    this.messagesContainer.appendChild(messageDiv);
    this.scrollToBottom();
  }

  setLoading(isLoading) {
    this.sendButton.disabled = isLoading;
    this.chatInput.disabled = isLoading;
    this.loadingIndicator.style.display = isLoading ? 'block' : 'none';

    if (isLoading) {
      this.messagesContainer.appendChild(this.loadingIndicator);
      this.scrollToBottom();
    }
  }

  showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    this.messagesContainer.appendChild(errorDiv);
    this.scrollToBottom();
  }

  scrollToBottom() {
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }
}

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', function() {
  new ChatInterface();
});
</script>