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
    <button id="send-button">SEND</button>
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
  --neo-black: #000000;
  --neo-white: #ffffff;
  --neo-yellow: #ffff00;
  --neo-pink: #ff00ff;
  --neo-cyan: #00ffff;
  --neo-green: #00ff00;
  --neo-red: #ff0000;
  --neo-blue: #0000ff;
  --neo-border: 4px;
  --neo-shadow: 8px 8px 0px;
}

* {
  box-sizing: border-box;
}

#chat-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  border: var(--neo-border) solid var(--neo-black);
  box-shadow: var(--neo-shadow) var(--neo-black);
  font-family: 'Courier New', 'Monaco', monospace;
  background: var(--neo-white);
  min-height: 600px;
  display: flex;
  flex-direction: column;
  font-weight: bold;
}

#chat-header {
  background: var(--neo-yellow);
  color: var(--neo-black);
  padding: 1.5rem;
  border-bottom: var(--neo-border) solid var(--neo-black);
  text-transform: uppercase;
}

#chat-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 900;
  letter-spacing: 2px;
}

#chat-header p {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: bold;
}

#health-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

#health-icon {
  font-size: 1.5rem;
  color: var(--neo-red);
  transition: color 0.3s ease;
}

#health-icon.healthy {
  color: var(--neo-green);
}

#health-icon.unhealthy {
  color: var(--neo-red);
}

#chat-messages {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  min-height: 400px;
  max-height: 500px;
  scroll-behavior: smooth;
  background: var(--neo-white);
}

.message {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  animation: slideIn 0.3s ease-out;
}

.message.user {
  justify-content: flex-end;
}

.message-content {
  max-width: 70%;
  padding: 1rem 1.5rem;
  border: var(--neo-border) solid var(--neo-black);
  box-shadow: 4px 4px 0px var(--neo-black);
  word-wrap: break-word;
  white-space: pre-wrap;
  line-height: 1.5;
  font-weight: bold;
  text-transform: none;
}

.message.user .message-content {
  background: var(--neo-pink);
  color: var(--neo-black);
}

.message.bot .message-content {
  background: var(--neo-cyan);
  color: var(--neo-black);
}

.message-avatar {
  width: 40px;
  height: 40px;
  border: var(--neo-border) solid var(--neo-black);
  background: var(--neo-black);
  color: var(--neo-white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 1.2rem;
  flex-shrink: 0;
  text-transform: uppercase;
}

.message.user .message-avatar {
  background: var(--neo-pink);
  color: var(--neo-black);
}

.message.bot .message-avatar {
  background: var(--neo-cyan);
  color: var(--neo-black);
}

#chat-input-container {
  padding: 1.5rem;
  border-top: var(--neo-border) solid var(--neo-black);
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  background: var(--neo-white);
}

#chat-input {
  flex: 1;
  border: var(--neo-border) solid var(--neo-black);
  padding: 1rem;
  font-family: 'Courier New', 'Monaco', monospace;
  font-size: 1rem;
  font-weight: bold;
  resize: vertical;
  min-height: 60px;
  max-height: 120px;
  background: var(--neo-white);
  color: var(--neo-black);
  box-shadow: 4px 4px 0px var(--neo-black);
  text-transform: none;
}

#chat-input:focus {
  outline: none;
  background: var(--neo-yellow);
  box-shadow: 6px 6px 0px var(--neo-black);
}

#chat-input::placeholder {
  color: #666;
  text-transform: uppercase;
  font-weight: bold;
}

#send-button {
  border: var(--neo-border) solid var(--neo-black);
  background: var(--neo-green);
  color: var(--neo-black);
  padding: 1rem 2rem;
  font-family: 'Courier New', 'Monaco', monospace;
  font-weight: 900;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 4px 4px 0px var(--neo-black);
  text-transform: uppercase;
  letter-spacing: 1px;
}

#send-button:hover:not(:disabled) {
  background: var(--neo-yellow);
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0px var(--neo-black);
}

#send-button:active {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0px var(--neo-black);
}

#send-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  background: #ccc;
}

.typing-indicator {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 1rem;
  background: var(--neo-cyan);
  border: var(--neo-border) solid var(--neo-black);
  box-shadow: 4px 4px 0px var(--neo-black);
  margin: 1rem;
}

.typing-indicator span {
  height: 12px;
  width: 12px;
  background: var(--neo-black);
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
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

@keyframes slideIn {
  from { 
    opacity: 0; 
    transform: translateX(20px);
  }
  to { 
    opacity: 1; 
    transform: translateX(0);
  }
}

.error-message {
  background: var(--neo-red);
  color: var(--neo-white);
  border: var(--neo-border) solid var(--neo-black);
  padding: 1rem;
  margin: 1rem;
  box-shadow: 4px 4px 0px var(--neo-black);
  font-weight: bold;
  text-transform: uppercase;
}

.success-message {
  background: var(--neo-green);
  color: var(--neo-black);
  border: var(--neo-border) solid var(--neo-black);
  padding: 1rem;
  margin: 1rem;
  box-shadow: 4px 4px 0px var(--neo-black);
  font-weight: bold;
  text-transform: uppercase;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  #chat-container {
    margin: 0 1rem;
    min-height: 500px;
  }

  #chat-header h2 {
    font-size: 1.5rem;
  }

  .message-content {
    max-width: 85%;
  }

  #chat-input-container {
    flex-direction: column;
    gap: 1rem;
  }

  #send-button {
    align-self: stretch;
  }
}

/* Scrollbar styling */
#chat-messages::-webkit-scrollbar {
  width: 12px;
}

#chat-messages::-webkit-scrollbar-track {
  background: var(--neo-white);
  border: 2px solid var(--neo-black);
}

#chat-messages::-webkit-scrollbar-thumb {
  background: var(--neo-black);
  border: 2px solid var(--neo-white);
}

#chat-messages::-webkit-scrollbar-thumb:hover {
  background: var(--neo-pink);
}
</style>

<script>
class ChatInterface {
  constructor() {
    this.apiUrl = 'https://llm-chat-backend-NikhilR24.replit.app/api/chat';
    this.healthUrl = 'https://llm-chat-backend-NikhilR24.replit.app/api/health';
    this.messagesContainer = document.getElementById('chat-messages');
    this.chatInput = document.getElementById('chat-input');
    this.sendButton = document.getElementById('send-button');
    this.loadingIndicator = document.getElementById('loading');
    this.healthIcon = document.getElementById('health-icon');
    this.healthText = document.getElementById('health-text');

    this.currentConversationId = null;
    this.isLoading = false;
    this.retryCount = 0;
    this.maxRetries = 3;

    this.init();
  }

  init() {
    this.setupEventListeners();
    this.checkHealth();
    this.addWelcomeMessage();
  }

  setupEventListeners() {
    this.sendButton.addEventListener('click', () => this.sendMessage());

    this.chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    this.chatInput.addEventListener('input', () => {
      this.validateInput();
      this.autoResizeTextarea();
    });
  }

  validateInput() {
    const message = this.chatInput.value.trim();
    const isValid = message.length > 0 && message.length <= 1000;
    this.sendButton.disabled = !isValid || this.isLoading;
  }

  autoResizeTextarea() {
    this.chatInput.style.height = 'auto';
    this.chatInput.style.height = Math.min(this.chatInput.scrollHeight, 120) + 'px';
  }

  async checkHealth() {
    try {
      const response = await fetch(this.healthUrl);
      if (response.ok) {
        const data = await response.json();
        const isHealthy = data.status === 'healthy';
        this.updateHealthStatus(isHealthy, isHealthy ? 'ONLINE' : 'UNHEALTHY');
      } else {
        this.updateHealthStatus(false, 'OFFLINE');
      }
    } catch (error) {
      console.error('Health check error:', error);
      this.updateHealthStatus(false, 'OFFLINE');
    }
  }

  updateHealthStatus(isHealthy, statusText) {
    this.healthIcon.className = isHealthy ? 'healthy' : 'unhealthy';
    this.healthText.textContent = statusText;
  }

  addWelcomeMessage() {
    const welcomeMessage = "HEY THERE! I'M NIKHIL. ASK ME ANYTHING ABOUT AI, POKER, OR MY PROJECTS!";
    this.addMessage('bot', welcomeMessage);
  }

  async sendMessage() {
    const message = this.chatInput.value.trim();
    if (!message || this.isLoading) return;

    this.addMessage('user', message);
    this.chatInput.value = '';
    this.setLoading(true);

    try {
      const response = await this.sendMessageWithRetry(message);
      this.addMessage('bot', response.response);

      if (response.conversation_id) {
        this.currentConversationId = response.conversation_id;
      }
    } catch (error) {
      console.error('Chat error:', error);
      this.handleChatError(error);
    } finally {
      this.setLoading(false);
    }
  }

  async sendMessageWithRetry(message, retryCount = 0) {
    try {
      const requestBody = {
        message: message,
        timestamp: new Date().toISOString()
      };

      if (this.currentConversationId) {
        requestBody.conversation_id = this.currentConversationId;
      }

      const response = await fetch(this.apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`HTTP ${response.status}: ${errorData.error || response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (retryCount < this.maxRetries) {
        await this.delay(1000 * Math.pow(2, retryCount));
        return this.sendMessageWithRetry(message, retryCount + 1);
      }
      throw error;
    }
  }

  handleChatError(error) {
    let errorMessage = 'AN UNEXPECTED ERROR OCCURRED. PLEASE TRY AGAIN.';

    if (error.message.includes('Failed to fetch')) {
      errorMessage = 'CANNOT CONNECT TO BACKEND SERVER. CHECK YOUR CONNECTION.';
    } else if (error.message.includes('HTTP 429')) {
      errorMessage = error.message.includes('rate limit') 
        ? 'RATE LIMIT EXCEEDED. WAIT A MOMENT BEFORE SENDING ANOTHER MESSAGE.'
        : 'YOU\'VE REACHED THE MAXIMUM NUMBER OF CHATS. EMAIL CONTACT@RNIKHIL.COM FOR MORE.';
    } else if (error.message.includes('HTTP 400')) {
      errorMessage = 'INVALID MESSAGE FORMAT. CHECK YOUR INPUT.';
    } else if (error.message.includes('HTTP 500')) {
      errorMessage = 'SERVER ERROR OCCURRED. TRY AGAIN IN A MOMENT.';
    }

    this.addMessage('bot', errorMessage);
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
    this.isLoading = isLoading;
    this.sendButton.disabled = isLoading;
    this.chatInput.disabled = isLoading;
    this.loadingIndicator.style.display = isLoading ? 'block' : 'none';
    this.sendButton.textContent = isLoading ? 'SENDING...' : 'SEND';

    if (isLoading) {
      this.messagesContainer.appendChild(this.loadingIndicator);
      this.scrollToBottom();
    }
  }

  scrollToBottom() {
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', function() {
  new ChatInterface();
});
</script>
