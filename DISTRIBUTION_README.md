# AI Tech Support Chatbot - Distribution Package

## 📦 What's Included

This is a clean distribution package containing all the essential files for the AI Tech Support Chatbot project.

**⚠️ API Key NOT Included** - You need to add your own Groq API key (see setup instructions below)

---

## 📁 Package Contents

### Core Files
- ✅ `app.py` - Flask web application
- ✅ `console_bot.py` - Console interface
- ✅ `requirements.txt` - Python dependencies
- ✅ `run.bat` - Windows startup script

### Source Code (src/)
- ✅ 11 Python modules (4,500+ lines of code)
- AI fallback, sentiment analysis, context management, etc.

### Data
- ✅ `knowledge_base.json` - 15+ tech support Q&A entries

### Web Interface
- ✅ `templates/index.html` - Modern dashboard UI
- ✅ `static/css/style.css` - Professional styling
- ✅ `static/js/chat.js` - Frontend JavaScript

### Documentation
- ✅ `README.md` - Main documentation
- ✅ `TEST_GUIDE.md` - Testing instructions
- ✅ `QUICK_TEST.md` - Quick start guide
- ✅ `docs/` - Architecture and presentation docs

---

## 🚀 Quick Setup

### 1. Extract ZIP
Extract all files to your desired location.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
- Flask
- Flask-CORS
- python-dotenv
- requests
- nltk

### 3. Create .env File
Create a file named `.env` in the root directory:

```env
# Environment Configuration for Tech Support Chatbot

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=tech-support-chatbot-secret-key-2024

# Groq AI API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Features
ENABLE_VOICE=true
DEFAULT_LANGUAGE=en
LOG_LEVEL=INFO
```

### 4. Get Groq API Key
1. Visit: https://console.groq.com/
2. Sign up for free account
3. Create API key
4. Paste into `.env` file

### 5. Download NLTK Data (First Run)
```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

### 6. Run the Application

**Windows:**
```bash
run.bat
```

**Or manually:**
```bash
python app.py
```

### 7. Open Browser
Navigate to: http://localhost:5000

---

## 🎯 Features

✅ **AI-Powered Responses** - Groq API with GPT-OSS-120B  
✅ **Sentiment Analysis** - Real-time emotion detection  
✅ **Multi-Language** - English and Arabic support  
✅ **Context Memory** - Remembers conversation history  
✅ **Voice Input** - Speech recognition support  
✅ **Analytics Dashboard** - Visual charts and statistics  
✅ **Conversation Export** - JSON, Text, PDF formats  
✅ **Learning System** - Improves from feedback  

---

## 📊 Project Statistics

- **Lines of Code**: 4,500+
- **Core Modules**: 11
- **Knowledge Entries**: 15+
- **Response Time**: <100ms (knowledge base)
- **AI Response Time**: 2-4 seconds (AI fallback)

---

## 🎨 Color Scheme

- **Primary Blue**: #1736F5
- **Accent Yellow**: #FFC709
- **Neutral Gray**: #808080
- **Light Gray**: #DEDEDE

---

## 🧪 Testing

### Quick Test Questions

**Knowledge Base (Fast):**
1. "What is RAM?"
2. "My WiFi is not working"
3. "Computer is running slow"

**AI Fallback (Requires API key):**
1. "What is Docker?"
2. "Explain Kubernetes"
3. "How does GraphQL work?"

See `TEST_GUIDE.md` for comprehensive testing instructions.

---

## 📁 Project Structure

```
AI_Tech_Support_Chatbot/
├── app.py                      # Flask web server
├── console_bot.py              # CLI interface
├── requirements.txt            # Dependencies
├── .env.example               # Config template
├── src/                       # Source code
│   ├── chatbot_engine.py     # Main engine
│   ├── ai_fallback.py        # Groq AI integration
│   ├── knowledge_base.py     # Q&A database
│   ├── sentiment_analyzer.py # Emotion detection
│   ├── context_manager.py    # Memory system
│   └── ... (6 more modules)
├── data/                      # Data files
│   └── knowledge_base.json
├── templates/                 # HTML templates
│   └── index.html
├── static/                    # CSS & JS
│   ├── css/style.css
│   └── js/chat.js
├── docs/                      # Documentation
└── logs/                      # Log files

```

---

## 🔧 Configuration

### .env Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | development |
| `SECRET_KEY` | Flask secret key | (generated) |
| `GROQ_API_KEY` | Groq API key | **REQUIRED** |
| `ENABLE_VOICE` | Voice input | true |
| `DEFAULT_LANGUAGE` | UI language | en |
| `LOG_LEVEL` | Logging level | INFO |

---

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "AI fallback not working"
**Solution**: Check GROQ_API_KEY in .env file

### Issue: "NLTK data not found"
**Solution**: Download NLTK data
```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

### Issue: "Port 5000 already in use"
**Solution**: Change port in app.py or stop other Flask apps

---

## 📚 Documentation Files

- **README.md** - Main project documentation
- **TEST_GUIDE.md** - 15+ test questions with expected results
- **QUICK_TEST.md** - Quick start testing guide
- **FIXES_SUMMARY.md** - Recent bug fixes and improvements
- **AI_PLAIN_TEXT_UPDATE.md** - AI formatting enhancements
- **docs/ARCHITECTURE.md** - System architecture
- **docs/PRESENTATION_SCRIPT.md** - Presentation guide

---

## 👤 Developer Information

**Developer**: Eng. Reem Osama  
**Email**: reemosamasaid2004@gmail.com  
**Phone**: 01070100321  
**GitHub**: https://github.com/Remaaa17  
**Project**: Syntecxhub AI Internship - Week 2

**Repository**: https://github.com/Remaaa17/Syntecxhub_AI-Tech-Support-Chatbot_P1

---

## 📝 License

Educational Project - Syntecxhub AI Internship

---

## 🆘 Support

For issues or questions:
1. Check documentation files
2. Review TEST_GUIDE.md
3. Contact developer (see above)

---

## ✅ Checklist for New Users

- [ ] Extract ZIP file
- [ ] Install Python 3.8+
- [ ] Run `pip install -r requirements.txt`
- [ ] Create `.env` file with GROQ_API_KEY
- [ ] Download NLTK data
- [ ] Run `python app.py`
- [ ] Open http://localhost:5000
- [ ] Test with "What is RAM?"
- [ ] Test AI with "What is Docker?"

---

**🎉 Ready to use! Enjoy your AI Tech Support Chatbot!**

For detailed setup and usage, see the included README.md file.
