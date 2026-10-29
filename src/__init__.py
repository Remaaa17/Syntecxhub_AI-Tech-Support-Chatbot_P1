"""
Tech Support Chatbot - Core Package
"""

from .chatbot_engine import ChatbotEngine
from .intent_matcher import IntentMatcher
from .knowledge_base import KnowledgeBase
from .sentiment_analyzer import SentimentAnalyzer
from .context_manager import ContextManager
from .language_handler import LanguageHandler
from .voice_handler import VoiceHandler
from .learning_system import LearningSystem
from .analytics_engine import AnalyticsEngine
from .export_manager import ExportManager
from .ai_fallback import AIFallback

__all__ = [
    'ChatbotEngine',
    'IntentMatcher',
    'KnowledgeBase',
    'SentimentAnalyzer',
    'ContextManager',
    'LanguageHandler',
    'VoiceHandler',
    'LearningSystem',
    'AnalyticsEngine',
    'ExportManager',
    'AIFallback'
]

__version__ = '1.0.0'
