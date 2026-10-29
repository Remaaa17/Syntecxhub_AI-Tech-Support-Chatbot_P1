"""
Learning System - Improves responses based on user feedback
"""

import json
import os
from typing import Dict, Optional
from collections import defaultdict
from datetime import datetime


class LearningSystem:
    """Learns from user interactions and feedback"""
    
    def __init__(self):
        """Initialize learning system"""
        self.learned_responses = {}
        self.feedback_data = []
        self._load_learned_data()
        
    def add_feedback(self, message: str, response: str, 
                    rating: int, user_id: str = "default"):
        """
        Store user feedback
        
        Args:
            message: User's original message
            response: Bot's response
            rating: User rating (1-5)
            user_id: User identifier
        """
        feedback_entry = {
            'message': message.lower().strip(),
            'response': response,
            'rating': rating,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }
        
        self.feedback_data.append(feedback_entry)
        
        # If rating is good (4-5), store as learned response
        if rating >= 4:
            message_key = message.lower().strip()
            
            if message_key not in self.learned_responses:
                self.learned_responses[message_key] = {
                    'response': response,
                    'confidence': 0.7,
                    'count': 1,
                    'avg_rating': rating
                }
            else:
                # Update existing
                current = self.learned_responses[message_key]
                current['count'] += 1
                current['avg_rating'] = (
                    (current['avg_rating'] * (current['count'] - 1) + rating) / 
                    current['count']
                )
                # Increase confidence with more positive feedback
                current['confidence'] = min(0.95, current['confidence'] + 0.05)
        
        # Auto-save after every 10 feedback entries
        if len(self.feedback_data) % 10 == 0:
            self.save()
    
    def get_learned_response(self, message: str) -> Optional[Dict]:
        """
        Get learned response for a message
        
        Args:
            message: User's message
            
        Returns:
            Dict with response and confidence, or None
        """
        message_key = message.lower().strip()
        
        if message_key in self.learned_responses:
            return self.learned_responses[message_key]
        
        # Try partial matching
        for learned_msg, data in self.learned_responses.items():
            if learned_msg in message_key or message_key in learned_msg:
                return {
                    'response': data['response'],
                    'confidence': data['confidence'] * 0.8  # Lower confidence for partial match
                }
        
        return None
    
    def get_learned_count(self) -> int:
        """Get number of learned responses"""
        return len(self.learned_responses)
    
    def get_feedback_summary(self) -> Dict:
        """Get summary of feedback data"""
        if not self.feedback_data:
            return {
                'total_feedback': 0,
                'average_rating': 0.0,
                'ratings_distribution': {}
            }
        
        total = len(self.feedback_data)
        ratings = [f['rating'] for f in self.feedback_data]
        avg_rating = sum(ratings) / len(ratings)
        
        distribution = defaultdict(int)
        for rating in ratings:
            distribution[rating] += 1
        
        return {
            'total_feedback': total,
            'average_rating': round(avg_rating, 2),
            'ratings_distribution': dict(distribution)
        }
    
    def save(self):
        """Save learned data to files"""
        models_dir = 'models'
        os.makedirs(models_dir, exist_ok=True)
        
        # Save learned responses
        responses_path = os.path.join(models_dir, 'learned_responses.json')
        with open(responses_path, 'w', encoding='utf-8') as f:
            json.dump(self.learned_responses, f, indent=2, ensure_ascii=False)
        
        # Save feedback data
        feedback_path = os.path.join(models_dir, 'feedback_data.json')
        with open(feedback_path, 'w', encoding='utf-8') as f:
            json.dump(self.feedback_data, f, indent=2, ensure_ascii=False)
    
    def _load_learned_data(self):
        """Load learned data from files"""
        # Load learned responses
        responses_path = os.path.join('models', 'learned_responses.json')
        if os.path.exists(responses_path):
            try:
                with open(responses_path, 'r', encoding='utf-8') as f:
                    self.learned_responses = json.load(f)
            except Exception as e:
                print(f"[WARNING] Could not load learned responses: {e}")
        
        # Load feedback data
        feedback_path = os.path.join('models', 'feedback_data.json')
        if os.path.exists(feedback_path):
            try:
                with open(feedback_path, 'r', encoding='utf-8') as f:
                    self.feedback_data = json.load(f)
            except Exception as e:
                print(f"[WARNING] Could not load feedback data: {e}")
