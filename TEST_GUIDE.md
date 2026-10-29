# Tech Support Chatbot - Test Guide

## Test Questions

### 1. Hardware Questions
**Question**: "What is RAM?"
- **Expected**: Answer about Random Access Memory
- **Category**: hardware
- **Confidence**: High (>80%)

**Question**: "What is ROM?"
- **Expected**: Answer about Read-Only Memory (NOT RAM)
- **Category**: hardware
- **Confidence**: High (>80%)

**Question**: "What is the difference between SSD and HDD?"
- **Expected**: Answer explaining solid-state vs hard disk drives
- **Category**: hardware
- **Confidence**: High (>80%)

### 2. Network Questions
**Question**: "My WiFi is not working"
- **Expected**: Troubleshooting steps for WiFi issues
- **Category**: network
- **Confidence**: High (>80%)

**Question**: "What is an IP address?"
- **Expected**: Explanation of IP addresses with examples
- **Category**: network
- **Confidence**: High (>80%)

### 3. Installation Questions
**Question**: "How do I install Python?"
- **Expected**: Step-by-step Python installation guide
- **Category**: installation
- **Confidence**: High (>80%)

**Question**: "How to install Node.js?"
- **Expected**: Node.js installation instructions with npm
- **Category**: installation
- **Confidence**: High (>80%)

### 4. Performance Questions
**Question**: "Computer is running slow"
- **Expected**: Multiple solutions for improving performance
- **Category**: performance
- **Confidence**: High (>80%)

**Question**: "How to speed up my computer?"
- **Expected**: Tips for optimizing computer speed
- **Category**: performance
- **Confidence**: High (>80%)

### 5. Security Questions
**Question**: "I forgot my password"
- **Expected**: Password recovery steps
- **Category**: security
- **Confidence**: High (>80%)

**Question**: "How to secure my computer?"
- **Expected**: Security best practices
- **Category**: security
- **Confidence**: High (>80%)

### 6. AI Fallback Test (Unknown Topics)
**Question**: "What is Docker?"
- **Expected**: AI-generated explanation about Docker containers
- **Source**: ai_fallback
- **Note**: Should use Groq API with Qwen 2.5 Coder model

**Question**: "Explain microservices architecture"
- **Expected**: AI-generated explanation of microservices
- **Source**: ai_fallback
- **Note**: Should trigger AI when no exact match found

**Question**: "How do I use Kubernetes?"
- **Expected**: AI-generated Kubernetes guidance
- **Source**: ai_fallback
- **Note**: Advanced topic not in knowledge base

### 7. Greeting & General
**Question**: "Hello"
- **Expected**: Friendly greeting response
- **Intent**: greeting
- **Category**: general

**Question**: "Thank you"
- **Expected**: Acknowledgment response
- **Intent**: gratitude
- **Category**: general

## Feature Testing Checklist

### Chat Interface
- [ ] Send text messages
- [ ] Messages appear in chat area
- [ ] Bot responses show metadata (sentiment, intent, confidence)
- [ ] Typing indicator appears while waiting
- [ ] Clear chat button works
- [ ] Voice input button (if supported by browser)

### Analytics Tab
- [ ] Tab switches from Chat to Analytics
- [ ] Statistics cards show:
  - Total Messages count
  - Resolved Issues count
  - Average Sentiment
  - Average Response Time
- [ ] Sentiment Distribution chart (Doughnut)
- [ ] Top Issues chart (Bar)
- [ ] Messages Over Time chart (Line)
- [ ] Refresh button updates data

### History Tab
- [ ] Tab switches from Chat to History
- [ ] Shows list of all conversations
- [ ] Each conversation displays:
  - Number and timestamp
  - Sentiment badge
  - Question preview
  - Answer preview
  - Metadata (Intent, Confidence, Source)
- [ ] Click conversation to view full details
- [ ] Clear All button removes history

### Settings Tab
- [ ] Tab switches from Chat to Settings
- [ ] Language selection dropdown
- [ ] Toggle switches for:
  - Sound Effects
  - Voice Input
  - Context Memory
  - AI Fallback
- [ ] Project information displays:
  - Version
  - Developer info
  - Contact details
  - Features list
  - Tech stack badges
  - Project statistics
- [ ] Save button stores settings

### Export Functionality
- [ ] Export button opens modal
- [ ] Can export as JSON
- [ ] Can export as Text
- [ ] Can export as PDF
- [ ] Downloaded file contains conversation data

### Responsiveness
- [ ] Works on desktop (1920x1080)
- [ ] Works on tablet (768x1024)
- [ ] Works on mobile (375x667)
- [ ] Navigation collapses on small screens

## Expected Behavior

### Keyword Matching (Fixed)
- Uses word boundaries to prevent false matches
- "What is ROM?" should NOT return RAM answer
- "ram" in "program" should NOT trigger RAM answer
- Only exact word matches trigger responses

### AI Fallback
- Triggered when confidence < threshold (default 60%)
- Uses Groq API with Qwen 2.5 Coder 32B model
- System prompt configured for tech support
- Fallback should provide relevant answers for unknown topics

### Sentiment Analysis
- Positive: Happy, satisfied, grateful messages
- Negative: Frustrated, angry, upset messages
- Neutral: Informational, factual questions

### Context Memory
- Remembers previous messages in conversation
- Can reference earlier topics
- Improves answer relevance

## Test Results Template

```
Date: __________
Tester: __________

| Question | Expected Category | Actual Category | Confidence | Pass/Fail | Notes |
|----------|------------------|-----------------|------------|-----------|-------|
| What is RAM? | hardware | | | | |
| What is ROM? | hardware | | | | |
| My WiFi is not working | network | | | | |
| What is Docker? | ai_fallback | | | | |
| Hello | general | | | | |
```

## Known Issues
- None at this time

## Browser Support
- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support (voice may be limited)
- Mobile browsers: Full support

## API Keys Required
- Groq API Key: Must be set in `.env` file as `GROQ_API_KEY`
- Without API key: AI fallback will not work, but knowledge base works fine

## Performance Benchmarks
- Knowledge base search: < 10ms
- AI fallback response: 1-3 seconds
- Page load: < 1 second
- Chart rendering: < 500ms
