// Tech Support Chatbot - Frontend JavaScript

const API_BASE = '/api';
let userId = 'user_' + Math.random().toString(36).substr(2, 9);
let isRecording = false;

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const voiceBtn = document.getElementById('voiceBtn');
const clearBtn = document.getElementById('clearBtn');
const analyticsBtn = document.getElementById('analyticsBtn');
const exportBtn = document.getElementById('exportBtn');
const analyticsModal = document.getElementById('analyticsModal');
const exportModal = document.getElementById('exportModal');
const toast = document.getElementById('toast');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    messageInput.focus();
});

// Event Listeners
function setupEventListeners() {
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keydown', handleKeyPress);
    voiceBtn.addEventListener('click', toggleVoiceInput);
    clearBtn.addEventListener('click', clearChat);
    analyticsBtn.addEventListener('click', showAnalytics);
    exportBtn.addEventListener('click', showExport);
    
    // Auto-resize textarea
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = messageInput.scrollHeight + 'px';
    });
}

function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

// Send Message
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                user_id: userId,
                language: 'en'
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        if (response.ok) {
            // Add bot response
            addMessage(data.response, 'bot', {
                sentiment: data.sentiment,
                intent: data.intent,
                confidence: data.confidence
            });
        } else {
            showToast('Error: ' + (data.error || 'Failed to get response'), 'error');
        }
        
    } catch (error) {
        removeTypingIndicator(typingId);
        showToast('Network error. Please try again.', 'error');
        console.error('Error:', error);
    }
}

// Add Message to Chat
function addMessage(text, sender, metadata = {}) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = `message-avatar ${sender}-avatar`;
    
    if (sender === 'bot') {
        avatarDiv.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
            </svg>
        `;
    } else {
        avatarDiv.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
        `;
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    
    // Format message text (handle line breaks, lists, etc.)
    textDiv.innerHTML = formatMessageText(text);
    
    contentDiv.appendChild(textDiv);
    
    // Add metadata for bot messages
    if (sender === 'bot' && metadata.sentiment) {
        const metaDiv = document.createElement('div');
        metaDiv.className = 'message-meta';
        
        const sentimentBadge = document.createElement('span');
        sentimentBadge.className = `sentiment-badge sentiment-${metadata.sentiment.label}`;
        sentimentBadge.textContent = metadata.sentiment.label;
        
        metaDiv.appendChild(sentimentBadge);
        
        if (metadata.intent) {
            const intentSpan = document.createElement('span');
            intentSpan.textContent = `Intent: ${metadata.intent}`;
            metaDiv.appendChild(intentSpan);
        }
        
        contentDiv.appendChild(metaDiv);
    }
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function formatMessageText(text) {
    // Convert newlines to <br>
    let formatted = text.replace(/\n/g, '<br>');
    
    // Convert numbered lists
    formatted = formatted.replace(/^(\d+)\.\s/gm, '<br>$1. ');
    
    // Convert bullet points
    formatted = formatted.replace(/^[-*]\s/gm, '<br>• ');
    
    return formatted;
}

// Typing Indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typing-indicator';
    
    typingDiv.innerHTML = `
        <div class="message-avatar bot-avatar">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
            </svg>
        </div>
        <div class="message-content">
            <div class="message-text">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
    
    return 'typing-indicator';
}

function removeTypingIndicator(id) {
    const indicator = document.getElementById(id);
    if (indicator) {
        indicator.remove();
    }
}

// Voice Input
function toggleVoiceInput() {
    if (!isRecording) {
        startVoiceRecording();
    } else {
        stopVoiceRecording();
    }
}

function startVoiceRecording() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        showToast('Speech recognition not supported in this browser', 'error');
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onstart = () => {
        isRecording = true;
        voiceBtn.classList.add('recording');
        showToast('Listening...', 'info');
    };
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        messageInput.value = transcript;
        messageInput.focus();
    };
    
    recognition.onerror = (event) => {
        showToast('Speech recognition error: ' + event.error, 'error');
        stopVoiceRecording();
    };
    
    recognition.onend = () => {
        stopVoiceRecording();
    };
    
    recognition.start();
    window.currentRecognition = recognition;
}

function stopVoiceRecording() {
    if (window.currentRecognition) {
        window.currentRecognition.stop();
    }
    isRecording = false;
    voiceBtn.classList.remove('recording');
}

// Clear Chat
async function clearChat() {
    if (!confirm('Clear conversation history?')) return;
    
    try {
        await fetch(`${API_BASE}/context/${userId}`, {
            method: 'DELETE'
        });
        
        chatMessages.innerHTML = '';
        showToast('Chat cleared', 'success');
        
    } catch (error) {
        showToast('Failed to clear chat', 'error');
    }
}

// Analytics
async function showAnalytics() {
    analyticsModal.classList.add('active');
    
    const content = document.getElementById('analyticsContent');
    content.innerHTML = '<div class="loading">Loading analytics...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/analytics/${userId}`);
        const data = await response.json();
        
        if (response.ok) {
            displayAnalytics(data);
        } else {
            content.innerHTML = '<p>Failed to load analytics</p>';
        }
    } catch (error) {
        content.innerHTML = '<p>Error loading analytics</p>';
    }
}

function displayAnalytics(data) {
    const content = document.getElementById('analyticsContent');
    
    let html = '<div class="analytics-grid">';
    
    // Stats cards
    if (data.conversation_stats) {
        const stats = data.conversation_stats;
        html += `
            <div class="stat-card">
                <div class="stat-value">${stats.total_messages || 0}</div>
                <div class="stat-label">Total Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${stats.sentiment_label || 'Neutral'}</div>
                <div class="stat-label">Avg Sentiment</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${stats.duration || '0m'}</div>
                <div class="stat-label">Duration</div>
            </div>
        `;
    }
    
    html += `
        <div class="stat-card">
            <div class="stat-value">${data.satisfaction_score || 0}</div>
            <div class="stat-label">Satisfaction Score</div>
        </div>
    </div>`;
    
    // Top intents
    if (data.intent_distribution) {
        html += '<h3>Top Issues</h3><ul>';
        const intents = Object.entries(data.intent_distribution)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);
        
        for (const [intent, count] of intents) {
            html += `<li>${intent}: ${count}</li>`;
        }
        html += '</ul>';
    }
    
    content.innerHTML = html;
}

function closeAnalytics() {
    analyticsModal.classList.remove('active');
}

// Export
function showExport() {
    exportModal.classList.add('active');
}

function closeExport() {
    exportModal.classList.remove('active');
}

async function exportChat(format) {
    try {
        const response = await fetch(`${API_BASE}/export/${userId}?format=${format}`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `chat_${userId}.${format}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            showToast('Conversation exported successfully', 'success');
            closeExport();
        } else {
            showToast('Export failed', 'error');
        }
    } catch (error) {
        showToast('Export error', 'error');
    }
}

// Toast Notifications
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = 'toast show ' + type;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Utility
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Close modals on outside click
window.onclick = (event) => {
    if (event.target === analyticsModal) {
        closeAnalytics();
    }
    if (event.target === exportModal) {
        closeExport();
    }
};
