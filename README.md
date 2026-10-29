# AI Tech Support Assistant - Syntecxhub Week 2 Project

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0-green.svg)
![AI](https://img.shields.io/badge/AI-Powered-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**Syntecxhub AI Internship - Week 2 Project**

## Project Overview

An intelligent Tech Support Assistant chatbot that helps users troubleshoot technical issues, provides IT solutions, answers programming questions, and offers software guidance. Features include web interface, sentiment analysis, multi-language support, voice interaction, conversation memory, and analytics dashboard.

## Features

### Core Features
- **Rule-Based Pattern Matching** - Fast intent recognition
- **Knowledge Base** - Domain-specific Q&A system
- **Context Memory** - Remembers conversation history
- **Interactive Console** - Command-line interface
- **Conversation Logging** - Full chat history tracking

### Advanced Features
- **Beautiful Web UI** - ChatGPT-style modern interface
- **Sentiment Analysis** - Detects user emotions in real-time
- **Multi-Language Support** - English + Arabic with auto-translation
- **Voice Input/Output** - Speech recognition and text-to-speech
- **Learning System** - Improves responses from user feedback
- **AI-Powered Fallback** - Uses free LLM API for unknown queries
- **Analytics Dashboard** - Visual conversation insights
- **Export Functionality** - Save chats as PDF or JSON

## Technology Stack

### Backend
- **Python 3.8+** - Core language
- **Flask** - Web framework
- **NLTK & TextBlob** - NLP processing
- **Transformers** - AI models
- **SpeechRecognition** - Voice input
- **pyttsx3 & gTTS** - Text-to-speech

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript (ES6+)** - Interactivity
- **Chart.js** - Analytics visualization
- **Web Speech API** - Voice interface

### AI & NLP
- **Pattern Matching** - Intent recognition
- **Sentiment Analysis** - Emotion detection
- **Language Detection** - Auto language identification
- **Translation** - Multi-language support

## Installation

### Step 1: Clone or Download

```bash
cd Syntecxhup_Week2
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon'); nltk.download('stopwords')"
```

### Step 4: Run the Application

**Web Interface:**
```bash
python app.py
```
Then open: http://localhost:5000

**Console Interface:**
```bash
python console_bot.py
```

## Project Structure

```
Syntecxhup_Week2/
├── app.py                      # Flask web application
├── console_bot.py              # Command-line interface
├── requirements.txt            # Dependencies
├── README.md                   # This file
├── src/
│   ├── chatbot_engine.py      # Core chatbot logic
│   ├── intent_matcher.py      # Pattern matching engine
│   ├── knowledge_base.py      # Q&A database
│   ├── sentiment_analyzer.py  # Emotion detection
│   ├── context_manager.py     # Conversation memory
│   ├── language_handler.py    # Multi-language support
│   ├── voice_handler.py       # Speech I/O
│   ├── learning_system.py     # Feedback learning
│   ├── analytics_engine.py    # Statistics & insights
│   └── export_manager.py      # PDF/JSON export
├── static/
│   ├── css/
│   │   └── style.css          # UI styling
│   └── js/
│       └── chat.js            # Frontend logic
├── templates/
│   └── index.html             # Web interface
├── data/
│   ├── intents.json           # Intent patterns
│   ├── knowledge_base.json    # Q&A database
│   └── conversations.json     # Chat history
├── logs/
│   └── chat_history.log       # Conversation logs
├── models/
│   └── learned_responses.json # ML improvements
├── tests/
│   └── test_chatbot.py        # Unit tests
└── docs/
    ├── ARCHITECTURE.md        # System design
    └── API_REFERENCE.md       # API documentation
```

## Usage Guide

### Web Interface

1. **Start Conversation**
   - Open http://localhost:5000
   - Type your message in the input box
   - Press Enter or click Send

2. **Voice Input**
   - Click the microphone icon
   - Speak your message
   - Bot will respond with voice

3. **Change Language**
   - Select English or Arabic from dropdown
   - Messages auto-translate

4. **View Analytics**
   - Click "Analytics" button
   - See conversation statistics
   - View sentiment trends

5. **Export Chat**
   - Click "Export" button
   - Choose PDF or JSON format
   - Download conversation history

### Console Interface

```
> Hello
Bot: Hi! How can I help you today?

> What's the weather?
Bot: I can help with information, but I don't have real-time weather data.

> /help
Available commands:
  /help     - Show this help
  /clear    - Clear conversation
  /export   - Export chat history
  /stats    - Show statistics
  /quit     - Exit chatbot
```

## Features Explained

### 1. Intent Recognition
The bot recognizes multiple intents:
- Greetings (hello, hi, hey)
- Farewells (bye, goodbye, see you)
- Help requests (help, assist, support)
- Questions (what, when, where, how)
- Small talk (weather, jokes, compliments)

### 2. Sentiment Analysis
Detects user emotions:
- Positive (happy, excited)
- Negative (angry, sad)
- Neutral (informational)

Adjusts responses based on detected emotion.

### 3. Context Memory
Remembers:
- Previous messages
- User preferences
- Topic continuity
- Session information

### 4. Multi-Language Support
- Auto-detects input language
- Translates to preferred language
- Supports English and Arabic
- Easy to add more languages

### 5. Voice Interaction
**Input:** Uses Web Speech API / SpeechRecognition
**Output:** Uses text-to-speech engines (gTTS/pyttsx3)

### 6. Learning System
- Collects user feedback
- Improves responses over time
- Adapts to user preferences
- Stores learned patterns

### 7. Analytics Dashboard
Visualizes:
- Message count over time
- Sentiment distribution
- Most common intents
- Response accuracy
- Session duration

### 8. AI Fallback
When rule-based matching fails:
- Uses free LLM API (Hugging Face)
- Generates contextual responses
- Maintains conversation flow
- Falls back gracefully

## Configuration

### Environment Variables (.env)

```
FLASK_ENV=development
SECRET_KEY=your-secret-key
LLM_API_KEY=your-huggingface-api-key
ENABLE_VOICE=true
DEFAULT_LANGUAGE=en
LOG_LEVEL=INFO
```

### Customization

**Add New Intents:** Edit `data/intents.json`
```json
{
  "intent": "weather",
  "patterns": ["what's the weather", "is it raining"],
  "responses": ["I don't have real-time weather data."]
}
```

**Add Knowledge:** Edit `data/knowledge_base.json`
```json
{
  "question": "What is AI?",
  "answer": "AI is Artificial Intelligence...",
  "keywords": ["ai", "artificial intelligence"]
}
```

## Testing

Run unit tests:
```bash
python -m pytest tests/
```

Run integration tests:
```bash
python tests/test_chatbot.py
```

## Performance

- **Response Time:** < 100ms (rule-based)
- **AI Fallback:** < 2s (API dependent)
- **Voice Recognition:** < 1s
- **Memory Usage:** ~200 MB
- **Concurrent Users:** 100+ (with proper scaling)

## Future Enhancements

- [ ] Deep learning models (BERT, GPT)
- [ ] More languages (French, Spanish, German)
- [ ] Mobile app (React Native)
- [ ] Video chat support
- [ ] Integration with Slack/Discord
- [ ] Custom training interface
- [ ] Advanced analytics with ML
- [ ] Personalization engine

## Security

- Input sanitization
- XSS protection
- Rate limiting
- Secure session management
- Privacy-focused logging

## License

This project is created as part of Syntecxhub AI Internship Program.

## Author

**Eng. Reem Osama**
- Syntecxhub AI Internship - Week 2
- Project: Advanced AI Chatbot

## Contact

For questions or feedback about this project:
- Email: reemosamasaid2004@gmail.com
- Phone: 01070100321

---

Star this repository if you find it helpful!
