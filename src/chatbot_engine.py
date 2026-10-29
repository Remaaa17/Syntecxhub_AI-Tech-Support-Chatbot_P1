"""
Advanced Chatbot Engine
Coordinates all chatbot components and manages conversation flow
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from .intent_matcher import IntentMatcher
from .knowledge_base import KnowledgeBase
from .sentiment_analyzer import SentimentAnalyzer
from .context_manager import ContextManager
from .language_handler import LanguageHandler
from .learning_system import LearningSystem


class ChatbotEngine:
    """Main chatbot engine that coordinates all components"""
    
    def __init__(self):
        """Initialize chatbot with all components"""
        self.intent_matcher = IntentMatcher()
        self.knowledge_base = KnowledgeBase()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.context_manager = ContextManager()
        self.language_handler = LanguageHandler()
        self.learning_system = LearningSystem()
        
        self.conversation_count = 0
        self.start_time = datetime.now()
        
        print("[OK] Chatbot Engine initialized successfully")
    
    def process_message(self, user_message: str, user_id: str = "default", 
                       language: str = "en") -> Dict:
        """
        Process user message and generate response
        
        Args:
            user_message: User's input text
            user_id: Unique user identifier
            language: Preferred language (en/ar)
            
        Returns:
            Dictionary containing response and metadata
        """
        self.conversation_count += 1
        
        # Detect language if auto-detect enabled
        detected_lang = self.language_handler.detect_language(user_message)
        
        # Translate to English for processing if needed
        if detected_lang != 'en':
            message_en = self.language_handler.translate(
                user_message, 
                source=detected_lang, 
                target='en'
            )
        else:
            message_en = user_message
        
        # Analyze sentiment
        sentiment = self.sentiment_analyzer.analyze(message_en)
        
        # Update context
        self.context_manager.add_message(user_id, message_en, "user")
        
        # Match intent
        intent_result = self.intent_matcher.match(message_en)
        
        # Initialize response
        response_text = None
        response_source = "unknown"
        confidence = 0.0
        
        # Try different response strategies
        
        # 1. Check knowledge base
        if not response_text:
            kb_result = self.knowledge_base.search(message_en)
            if kb_result and kb_result['confidence'] > 0.7:
                response_text = kb_result['answer']
                response_source = "knowledge_base"
                confidence = kb_result['confidence']
        
        # 2. Use intent-based response
        if not response_text and intent_result['confidence'] > 0.6:
            response_text = intent_result['response']
            response_source = "intent_matcher"
            confidence = intent_result['confidence']
        
        # 3. Check learning system for similar past responses
        if not response_text:
            learned_response = self.learning_system.get_learned_response(message_en)
            if learned_response:
                response_text = learned_response['response']
                response_source = "learned"
                confidence = learned_response['confidence']
        
        # 4. Fallback to default response
        if not response_text:
            response_text = self._get_fallback_response(sentiment)
            response_source = "fallback"
            confidence = 0.3
        
        # Adapt response based on sentiment
        response_text = self._adapt_to_sentiment(response_text, sentiment)
        
        # Translate response back to user's language
        if language != 'en':
            response_translated = self.language_handler.translate(
                response_text,
                source='en',
                target=language
            )
        else:
            response_translated = response_text
        
        # Store in context
        self.context_manager.add_message(user_id, response_translated, "bot")
        
        # Prepare response data
        response_data = {
            'response': response_translated,
            'response_en': response_text,
            'intent': intent_result.get('intent', 'unknown'),
            'confidence': confidence,
            'sentiment': sentiment,
            'source': response_source,
            'detected_language': detected_lang,
            'timestamp': datetime.now().isoformat(),
            'conversation_id': user_id
        }
        
        return response_data
    
    def _get_fallback_response(self, sentiment: Dict) -> str:
        """Generate fallback response based on sentiment"""
        
        sentiment_type = sentiment.get('label', 'neutral')
        
        responses = {
            'positive': [
                "That's interesting! Could you tell me more?",
                "I'd love to hear more about that!",
                "That sounds great! What else would you like to know?"
            ],
            'negative': [
                "I understand this might be frustrating. How can I help?",
                "I'm here to help. Can you provide more details?",
                "Let me try to assist you better. What specifically do you need?"
            ],
            'neutral': [
                "I'm not sure I understand. Could you rephrase that?",
                "Can you provide more details so I can help you better?",
                "I'm still learning. Could you ask that differently?"
            ]
        }
        
        import random
        return random.choice(responses.get(sentiment_type, responses['neutral']))
    
    def _adapt_to_sentiment(self, response: str, sentiment: Dict) -> str:
        """Adapt response tone based on user sentiment"""
        
        sentiment_type = sentiment.get('label', 'neutral')
        
        # Add empathetic prefix for negative sentiment
        if sentiment_type == 'negative' and sentiment.get('score', 0) < -0.3:
            empathy_phrases = [
                "I understand your concern. ",
                "I hear you. ",
                "That can be frustrating. "
            ]
            import random
            response = random.choice(empathy_phrases) + response
        
        # Add enthusiasm for positive sentiment
        elif sentiment_type == 'positive' and sentiment.get('score', 0) > 0.3:
            if not any(punct in response for punct in ['!', '?']):
                response = response.rstrip('.') + '!'
        
        return response
    
    def get_context(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation context for a user"""
        return self.context_manager.get_context(user_id, limit)
    
    def clear_context(self, user_id: str):
        """Clear conversation context for a user"""
        self.context_manager.clear_context(user_id)
    
    def provide_feedback(self, user_id: str, message: str, 
                        response: str, rating: int):
        """Store user feedback for learning"""
        self.learning_system.add_feedback(
            message=message,
            response=response,
            rating=rating,
            user_id=user_id
        )
    
    def get_statistics(self) -> Dict:
        """Get chatbot usage statistics"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            'conversation_count': self.conversation_count,
            'uptime_seconds': uptime,
            'uptime_formatted': self._format_duration(uptime),
            'intents_available': len(self.intent_matcher.intents),
            'knowledge_base_size': self.knowledge_base.get_size(),
            'learned_responses': self.learning_system.get_learned_count(),
            'active_contexts': self.context_manager.get_active_count()
        }
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"
    
    def export_conversation(self, user_id: str, format: str = 'json') -> str:
        """Export conversation history"""
        messages = self.context_manager.get_context(user_id, limit=None)
        
        if format == 'json':
            return json.dumps(messages, indent=2)
        elif format == 'text':
            lines = []
            for msg in messages:
                sender = "You" if msg['sender'] == 'user' else "Bot"
                lines.append(f"{sender}: {msg['message']}")
            return '\n'.join(lines)
        else:
            return json.dumps(messages, indent=2)
    
    def shutdown(self):
        """Cleanup and save data before shutdown"""
        print("[INFO] Shutting down chatbot engine...")
        self.learning_system.save()
        self.context_manager.save()
        print("[OK] Chatbot engine shutdown complete")
