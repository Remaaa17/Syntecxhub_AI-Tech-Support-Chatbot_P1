"""
Analytics Engine - Conversation insights and statistics
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
from collections import Counter, defaultdict


class AnalyticsEngine:
    """Provides analytics and insights on conversations"""
    
    def __init__(self, context_manager, sentiment_analyzer, intent_matcher):
        """
        Initialize analytics engine
        
        Args:
            context_manager: Reference to context manager
            sentiment_analyzer: Reference to sentiment analyzer
            intent_matcher: Reference to intent matcher
        """
        self.context_manager = context_manager
        self.sentiment_analyzer = sentiment_analyzer
        self.intent_matcher = intent_matcher
        
    def get_conversation_stats(self, user_id: str) -> Dict:
        """Get statistics for a specific conversation"""
        context = self.context_manager.get_context(user_id)
        
        if not context:
            return {
                'total_messages': 0,
                'user_messages': 0,
                'bot_messages': 0,
                'avg_sentiment': 0.0,
                'duration': '0m'
            }
        
        user_msgs = [m for m in context if m['sender'] == 'user']
        bot_msgs = [m for m in context if m['sender'] == 'bot']
        
        # Calculate sentiment
        sentiments = []
        for msg in user_msgs:
            sentiment = self.sentiment_analyzer.analyze(msg['message'])
            sentiments.append(sentiment['score'])
        
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0
        
        # Calculate duration
        if context:
            first_time = datetime.fromisoformat(context[0]['timestamp'])
            last_time = datetime.fromisoformat(context[-1]['timestamp'])
            duration = last_time - first_time
            duration_str = self._format_duration(duration.total_seconds())
        else:
            duration_str = '0m'
        
        return {
            'total_messages': len(context),
            'user_messages': len(user_msgs),
            'bot_messages': len(bot_msgs),
            'avg_sentiment': round(avg_sentiment, 3),
            'sentiment_label': 'positive' if avg_sentiment > 0.2 else 'negative' if avg_sentiment < -0.2 else 'neutral',
            'duration': duration_str
        }
    
    def get_intent_distribution(self, user_id: Optional[str] = None) -> Dict:
        """
        Get distribution of intents
        
        Args:
            user_id: Specific user or None for all users
            
        Returns:
            Dictionary with intent counts
        """
        contexts = []
        
        if user_id:
            contexts = [self.context_manager.get_context(user_id)]
        else:
            # Get all contexts
            for uid in self.context_manager.contexts.keys():
                contexts.append(self.context_manager.get_context(uid))
        
        intent_counts = Counter()
        
        for context in contexts:
            for msg in context:
                if msg['sender'] == 'user':
                    result = self.intent_matcher.match(msg['message'])
                    intent_counts[result['intent']] += 1
        
        return dict(intent_counts)
    
    def get_sentiment_distribution(self, user_id: Optional[str] = None) -> Dict:
        """
        Get distribution of sentiments
        
        Args:
            user_id: Specific user or None for all users
            
        Returns:
            Dictionary with sentiment counts
        """
        contexts = []
        
        if user_id:
            contexts = [self.context_manager.get_context(user_id)]
        else:
            for uid in self.context_manager.contexts.keys():
                contexts.append(self.context_manager.get_context(uid))
        
        sentiment_counts = Counter()
        
        for context in contexts:
            for msg in context:
                if msg['sender'] == 'user':
                    sentiment = self.sentiment_analyzer.analyze(msg['message'])
                    sentiment_counts[sentiment['label']] += 1
        
        return dict(sentiment_counts)
    
    def get_hourly_activity(self, user_id: Optional[str] = None) -> Dict:
        """Get message activity by hour of day"""
        contexts = []
        
        if user_id:
            contexts = [self.context_manager.get_context(user_id)]
        else:
            for uid in self.context_manager.contexts.keys():
                contexts.append(self.context_manager.get_context(uid))
        
        hourly_counts = defaultdict(int)
        
        for context in contexts:
            for msg in context:
                timestamp = datetime.fromisoformat(msg['timestamp'])
                hour = timestamp.hour
                hourly_counts[hour] += 1
        
        return dict(hourly_counts)
    
    def get_popular_topics(self, user_id: Optional[str] = None, top_n: int = 10) -> List[tuple]:
        """
        Get most common topics/keywords
        
        Args:
            user_id: Specific user or None for all
            top_n: Number of top topics to return
            
        Returns:
            List of (topic, count) tuples
        """
        contexts = []
        
        if user_id:
            contexts = [self.context_manager.get_context(user_id)]
        else:
            for uid in self.context_manager.contexts.keys():
                contexts.append(self.context_manager.get_context(uid))
        
        # Common tech support keywords
        keywords = [
            'wifi', 'internet', 'password', 'error', 'install', 'update',
            'slow', 'crash', 'printer', 'email', 'virus', 'backup',
            'windows', 'mac', 'linux', 'python', 'code', 'driver'
        ]
        
        keyword_counts = Counter()
        
        for context in contexts:
            for msg in context:
                if msg['sender'] == 'user':
                    text = msg['message'].lower()
                    for keyword in keywords:
                        if keyword in text:
                            keyword_counts[keyword] += 1
        
        return keyword_counts.most_common(top_n)
    
    def get_response_time_stats(self) -> Dict:
        """Calculate average response time"""
        # Simplified - in production, track actual response times
        return {
            'avg_response_time_ms': 150,
            'min_response_time_ms': 50,
            'max_response_time_ms': 500
        }
    
    def get_satisfaction_score(self, user_id: Optional[str] = None) -> float:
        """
        Calculate satisfaction score based on sentiment
        
        Returns:
            Score from 0-100
        """
        sentiment_dist = self.get_sentiment_distribution(user_id)
        
        total = sum(sentiment_dist.values())
        if total == 0:
            return 50.0  # Neutral
        
        positive = sentiment_dist.get('positive', 0)
        negative = sentiment_dist.get('negative', 0)
        neutral = sentiment_dist.get('neutral', 0)
        
        # Calculate weighted score
        score = ((positive * 100) + (neutral * 50) + (negative * 0)) / total
        
        return round(score, 1)
    
    def generate_report(self, user_id: Optional[str] = None) -> Dict:
        """
        Generate comprehensive analytics report
        
        Args:
            user_id: Specific user or None for all users
            
        Returns:
            Complete analytics report
        """
        return {
            'conversation_stats': self.get_conversation_stats(user_id) if user_id else {},
            'intent_distribution': self.get_intent_distribution(user_id),
            'sentiment_distribution': self.get_sentiment_distribution(user_id),
            'hourly_activity': self.get_hourly_activity(user_id),
            'popular_topics': dict(self.get_popular_topics(user_id, top_n=5)),
            'satisfaction_score': self.get_satisfaction_score(user_id),
            'response_times': self.get_response_time_stats(),
            'generated_at': datetime.now().isoformat()
        }
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes}m"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"
    
    def export_analytics(self, filepath: str, user_id: Optional[str] = None):
        """Export analytics to JSON file"""
        report = self.generate_report(user_id)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
