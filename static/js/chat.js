// Tech Support Chatbot - Frontend JavaScript

const API_BASE = '/api';
let userId = 'user_' + Math.random().toString(36).substr(2, 9);
let isRecording = false;
let conversationData = {
    messages: [],
    sentiments: { positive: 0, negative: 0, neutral: 0 },
    intents: {},
    totalMessages: 0,
    resolvedIssues: 0
};
let charts = {};

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
    setupNavigation();
    messageInput.focus();
    initializeCharts();
});

// Navigation Setup
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.getAttribute('data-page');
            
            // Update active state
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Switch view
            switchView(page);
        });
    });
}

function switchView(viewName) {
    console.log('Switching to view:', viewName);
    
    // Map page names to view IDs
    const viewMap = {
        'chat': 'chatView',
        'analytics': 'analyticsView',
        'history': 'historyView',
        'settings': 'settingsView'
    };
    
    // Get the actual view ID
    const viewId = viewMap[viewName] || viewName;
    
    // Hide all views
    const allViews = ['chatView', 'analyticsView', 'historyView', 'settingsView'];
    allViews.forEach(view => {
        const element = document.getElementById(view);
        if (element) {
            element.classList.add('hidden');
            console.log('Hiding:', view);
        }
    });
    
    // Show selected view
    const selectedView = document.getElementById(viewId);
    if (selectedView) {
        selectedView.classList.remove('hidden');
        console.log('Showing view:', viewId);
        
        // Load view-specific content with delay for rendering
        setTimeout(() => {
            if (viewId === 'analyticsView') {
                console.log('Loading analytics...');
                loadAnalytics();
            } else if (viewId === 'historyView') {
                console.log('Loading history...');
                loadHistory();
            }
        }, 100);
    } else {
        console.error('View not found:', viewId);
    }
}

// Event Listeners
function setupEventListeners() {
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keydown', handleKeyPress);
    voiceBtn.addEventListener('click', toggleVoiceInput);
    clearBtn.addEventListener('click', clearChat);
    analyticsBtn.addEventListener('click', () => {
        switchView('analyticsView');
        // Update nav active state
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        const analyticsNavLink = document.querySelector('[data-page="analytics"]');
        if (analyticsNavLink) {
            analyticsNavLink.classList.add('active');
        }
    });
    exportBtn.addEventListener('click', showExport);
    
    // Also setup analytics button in nav
    const analyticsNavBtn = document.getElementById('analyticsNavBtn');
    if (analyticsNavBtn) {
        analyticsNavBtn.addEventListener('click', (e) => {
            e.preventDefault();
            switchView('analyticsView');
        });
    }
    
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

// Send Message with improved accuracy
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
            // Update conversation data
            conversationData.totalMessages += 2;
            const sentimentLabel = data.sentiment?.label || 'neutral';
            conversationData.sentiments[sentimentLabel]++;
            
            const intent = data.intent || 'unknown';
            conversationData.intents[intent] = (conversationData.intents[intent] || 0) + 1;
            
            if (data.confidence > 0.7) {
                conversationData.resolvedIssues++;
            }
            
            // Store message
            conversationData.messages.push({
                user: message,
                bot: data.response,
                sentiment: data.sentiment,
                intent: data.intent,
                confidence: data.confidence,
                source: data.source,
                timestamp: new Date().toISOString()
            });
            
            // Add bot response
            addMessage(data.response, 'bot', {
                sentiment: data.sentiment,
                intent: data.intent,
                confidence: data.confidence,
                source: data.source
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

// Add Message to Chat with metadata
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
        
        // Sentiment badge
        const sentimentLabel = metadata.sentiment.label || 'neutral';
        const sentimentBadge = document.createElement('span');
        sentimentBadge.className = `meta-badge sentiment-${sentimentLabel}`;
        sentimentBadge.textContent = sentimentLabel.toUpperCase();
        metaDiv.appendChild(sentimentBadge);
        
        // Intent badge
        if (metadata.intent && metadata.intent !== 'unknown') {
            const intentBadge = document.createElement('span');
            intentBadge.className = 'meta-badge';
            intentBadge.textContent = `Intent: ${metadata.intent.replace('_', ' ')}`;
            metaDiv.appendChild(intentBadge);
        }
        
        // Confidence badge
        if (metadata.confidence) {
            const confidenceBadge = document.createElement('span');
            confidenceBadge.className = 'meta-badge';
            const confPercent = Math.round(metadata.confidence * 100);
            confidenceBadge.textContent = `${confPercent}% confidence`;
            metaDiv.appendChild(confidenceBadge);
        }
        
        contentDiv.appendChild(metaDiv);
    }
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function formatMessageText(text) {
    // Use basic text formatting (no markdown rendering for AI responses)
    return formatBasicText(text);
}

function formatBasicText(text) {
    // Basic text formatting with clean appearance
    let formatted = text;
    
    // Convert newlines to <br>
    formatted = formatted.replace(/\n/g, '<br>');
    
    // Convert numbered lists (but keep them clean)
    formatted = formatted.replace(/^(\d+)\.\s/gm, '<br>$1. ');
    
    // Convert bullet points  
    formatted = formatted.replace(/^[-•]\s/gm, '<br>• ');
    
    // Clean up any markdown symbols that might slip through
    // Remove bold markers **text** but keep the text
    formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    
    // Remove italic markers *text* but keep the text
    formatted = formatted.replace(/\*(.+?)\*/g, '<em>$1</em>');
    
    // Remove header markers # but keep the text as bold
    formatted = formatted.replace(/^#{1,6}\s+(.+)$/gm, '<strong>$1</strong><br>');
    
    // Remove table pipes and format as clean lines
    formatted = formatted.replace(/\|/g, ' ');
    
    // Remove horizontal rules
    formatted = formatted.replace(/^[-=]{3,}$/gm, '<br>');
    
    // Inline code `code` - keep simple
    formatted = formatted.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    
    // Clean up multiple consecutive <br> tags
    formatted = formatted.replace(/(<br>\s*){3,}/g, '<br><br>');
    
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

// Analytics Dashboard Functions
function initializeCharts() {
    // Initialize Chart.js defaults
    if (typeof Chart !== 'undefined') {
        Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
        Chart.defaults.color = '#808080';
    }
}

function loadAnalytics() {
    updateAnalyticsStats();
    createSentimentChart();
    createIssuesChart();
    createTimelineChart();
}

function updateAnalyticsStats() {
    document.getElementById('totalMessages').textContent = conversationData.totalMessages;
    document.getElementById('resolvedIssues').textContent = conversationData.resolvedIssues;
    
    // Calculate average sentiment
    const total = conversationData.sentiments.positive + conversationData.sentiments.negative + conversationData.sentiments.neutral;
    let avgSentiment = 'Neutral';
    if (total > 0) {
        if (conversationData.sentiments.positive > conversationData.sentiments.negative) {
            avgSentiment = 'Positive';
        } else if (conversationData.sentiments.negative > conversationData.sentiments.positive) {
            avgSentiment = 'Negative';
        }
    }
    document.getElementById('avgSentiment').textContent = avgSentiment;
}

function createSentimentChart() {
    const ctx = document.getElementById('sentimentChart');
    if (!ctx) {
        console.error('sentimentChart canvas not found');
        return;
    }
    
    console.log('Creating sentiment chart...');
    
    if (charts.sentiment) {
        charts.sentiment.destroy();
    }
    
    charts.sentiment = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Negative', 'Neutral'],
            datasets: [{
                data: [
                    conversationData.sentiments.positive || 1,
                    conversationData.sentiments.negative || 0,
                    conversationData.sentiments.neutral || 0
                ],
                backgroundColor: ['#10b981', '#ef4444', '#808080'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: { size: 12 }
                    }
                }
            }
        }
    });
    
    console.log('Sentiment chart created');
}

function createIssuesChart() {
    const ctx = document.getElementById('issuesChart');
    if (!ctx) {
        console.error('issuesChart canvas not found');
        return;
    }
    
    console.log('Creating issues chart...');
    
    if (charts.issues) {
        charts.issues.destroy();
    }
    
    const intents = Object.entries(conversationData.intents)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);
    
    // If no intents, show placeholder
    const labels = intents.length > 0 ? intents.map(i => i[0].replace('_', ' ')) : ['No data'];
    const data = intents.length > 0 ? intents.map(i => i[1]) : [1];
    
    charts.issues = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Count',
                data: data,
                backgroundColor: '#1736F5',
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1 }
                }
            }
        }
    });
    
    console.log('Issues chart created');
}

function createTimelineChart() {
    const ctx = document.getElementById('timelineChart');
    if (!ctx) {
        console.error('timelineChart canvas not found');
        return;
    }
    
    console.log('Creating timeline chart...');
    
    if (charts.timeline) {
        charts.timeline.destroy();
    }
    
    // Group messages by time (last 10 messages or placeholder)
    const messages = conversationData.messages.length > 0 
        ? conversationData.messages.slice(-10) 
        : [{user: 'Start', timestamp: new Date().toISOString()}];
    
    const timeLabels = messages.map((msg, idx) => `${idx + 1}`);
    const timeData = messages.map(() => 1);
    
    charts.timeline = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [{
                label: 'Messages',
                data: timeData,
                borderColor: '#1736F5',
                backgroundColor: 'rgba(23, 54, 245, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1 }
                }
            }
        }
    });
    
    console.log('Timeline chart created');
}

function refreshAnalytics() {
    loadAnalytics();
    showToast('Analytics refreshed', 'success');
}

// History Functions
function loadHistory() {
    const historyList = document.getElementById('historyList');
    if (!historyList) return;
    
    if (conversationData.messages.length === 0) {
        historyList.innerHTML = `
            <div class="empty-state">
                <svg width="80" height="80" viewBox="0 0 24 24" fill="#DEDEDE">
                    <path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z"/>
                </svg>
                <h3>No History Yet</h3>
                <p>Start a conversation and your history will appear here</p>
            </div>
        `;
        return;
    }
    
    historyList.innerHTML = '';
    
    conversationData.messages.forEach((msg, idx) => {
        const date = new Date(msg.timestamp);
        const timeStr = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        
        // Sentiment color
        const sentimentLabel = msg.sentiment?.label || 'neutral';
        let sentimentColor = '#808080';
        if (sentimentLabel === 'positive') sentimentColor = '#10b981';
        if (sentimentLabel === 'negative') sentimentColor = '#ef4444';
        
        historyItem.innerHTML = `
            <div class="history-item-header">
                <div class="history-meta">
                    <span class="history-number">#${idx + 1}</span>
                    <span class="history-date">${dateStr}</span>
                    <span class="history-time">${timeStr}</span>
                </div>
                <span class="history-badge" style="background: ${sentimentColor}20; color: ${sentimentColor};">
                    ${sentimentLabel}
                </span>
            </div>
            <div class="history-content">
                <div class="history-question">
                    <strong>You:</strong> ${escapeHtml(msg.user)}
                </div>
                <div class="history-answer">
                    <strong>Assistant:</strong> ${escapeHtml(msg.bot.substring(0, 150))}${msg.bot.length > 150 ? '...' : ''}
                </div>
                <div class="history-details">
                    <span class="detail-badge">Intent: ${msg.intent || 'unknown'}</span>
                    <span class="detail-badge">Confidence: ${Math.round((msg.confidence || 0) * 100)}%</span>
                    <span class="detail-badge">Source: ${msg.source || 'unknown'}</span>
                </div>
            </div>
        `;
        
        // Click to view full conversation
        historyItem.addEventListener('click', () => {
            showConversationDetail(msg, idx + 1);
        });
        
        historyList.appendChild(historyItem);
    });
}

function showConversationDetail(msg, number) {
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>Conversation #${number}</h2>
                <button class="modal-close" onclick="this.closest('.modal').remove()">&times;</button>
            </div>
            <div class="modal-body">
                <div class="conversation-detail">
                    <div class="detail-section">
                        <h4>Your Question:</h4>
                        <p>${escapeHtml(msg.user)}</p>
                    </div>
                    <div class="detail-section">
                        <h4>Assistant's Response:</h4>
                        <p>${escapeHtml(msg.bot)}</p>
                    </div>
                    <div class="detail-section">
                        <h4>Metadata:</h4>
                        <ul>
                            <li><strong>Timestamp:</strong> ${new Date(msg.timestamp).toLocaleString()}</li>
                            <li><strong>Sentiment:</strong> ${msg.sentiment?.label || 'N/A'}</li>
                            <li><strong>Intent:</strong> ${msg.intent || 'N/A'}</li>
                            <li><strong>Confidence:</strong> ${Math.round((msg.confidence || 0) * 100)}%</li>
                            <li><strong>Source:</strong> ${msg.source || 'N/A'}</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    
    // Close on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function clearAllHistory() {
    if (!confirm('Clear all conversation history?')) return;
    
    conversationData.messages = [];
    conversationData.sentiments = { positive: 0, negative: 0, neutral: 0 };
    conversationData.intents = {};
    conversationData.totalMessages = 0;
    conversationData.resolvedIssues = 0;
    
    loadHistory();
    showToast('History cleared', 'success');
}

// Settings Functions
function saveSettings() {
    const language = document.getElementById('languageSetting').value;
    const sound = document.getElementById('soundSetting').checked;
    const voice = document.getElementById('voiceEnabled').checked;
    const context = document.getElementById('contextMemory').checked;
    const aiEnabled = document.getElementById('aiEnabled').checked;
    
    // Save to localStorage
    localStorage.setItem('settings', JSON.stringify({
        language,
        sound,
        voice,
        context,
        aiEnabled
    }));
    
    showToast('Settings saved successfully', 'success');
}
