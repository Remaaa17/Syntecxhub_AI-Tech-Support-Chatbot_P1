"""
Sentiment Analyzer - Detects user emotions and sentiment
"""

from typing import Dict
import re


class SentimentAnalyzer:
    """Analyzes sentiment and emotions in user messages"""
    
    def __init__(self):
        """Initialize sentiment analyzer with lexicons"""
        self.positive_words = {
            'good', 'great', 'excellent', 'awesome', 'fantastic', 'wonderful',
            'amazing', 'perfect', 'love', 'like', 'helpful', 'thanks', 'thank',
            'appreciate', 'happy', 'glad', 'pleased', 'satisfied', 'works',
            'working', 'solved', 'fixed', 'resolved', 'success', 'brilliant'
        }
        
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'angry',
            'frustrated', 'annoying', 'useless', 'broken', 'not working',
            'failed', 'error', 'problem', 'issue', 'stuck', 'cant', "can't",
            'wont', "won't", 'dont', "don't", 'unable', 'impossible', 'crash',
            'slow', 'lagging', 'freezing', 'disappointed', 'upset'
        }
        
        self.intensifiers = {
            'very': 1.5, 'really': 1.5, 'extremely': 2.0, 'super': 1.5,
            'incredibly': 2.0, 'absolutely': 1.8, 'totally': 1.5
        }
        
        self.negations = {
            'not', 'no', 'never', 'nothing', 'nobody', 'none', 'neither',
            "don't", "doesn't", "didn't", "won't", "wouldn't", "can't",
            "couldn't", "isn't", "aren't", "wasn't", "weren't"
        }
        
    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment of text
        
        Args:
            text: User's message
            
        Returns:
            Dict with sentiment label, score, and emotion
        """
        if not text or not text.strip():
            return {
                'label': 'neutral',
                'score': 0.0,
                'emotion': 'neutral',
                'confidence': 0.0
            }
        
        text = text.lower().strip()
        words = re.findall(r'\b\w+\b', text)
        
        score = 0.0
        word_count = 0
        negation_active = False
        intensifier_multiplier = 1.0
        
        for i, word in enumerate(words):
            # Check for intensifiers
            if word in self.intensifiers:
                intensifier_multiplier = self.intensifiers[word]
                continue
            
            # Check for negations
            if word in self.negations:
                negation_active = True
                continue
            
            # Score positive words
            if word in self.positive_words:
                word_score = 1.0 * intensifier_multiplier
                if negation_active:
                    word_score = -word_score
                score += word_score
                word_count += 1
            
            # Score negative words
            elif word in self.negative_words:
                word_score = -1.0 * intensifier_multiplier
                if negation_active:
                    word_score = -word_score
                score += word_score
                word_count += 1
            
            # Reset flags after 3 words
            if i > 0 and (i % 3 == 0):
                negation_active = False
                intensifier_multiplier = 1.0
        
        # Normalize score
        if word_count > 0:
            normalized_score = score / word_count
            # Clamp between -1 and 1
            normalized_score = max(-1.0, min(1.0, normalized_score))
            confidence = min(word_count / 10.0, 1.0)  # More words = higher confidence
        else:
            normalized_score = 0.0
            confidence = 0.0
        
        # Determine label and emotion
        if normalized_score > 0.2:
            label = 'positive'
            if normalized_score > 0.6:
                emotion = 'happy'
            else:
                emotion = 'satisfied'
        elif normalized_score < -0.2:
            label = 'negative'
            if normalized_score < -0.6:
                emotion = 'angry'
            else:
                emotion = 'frustrated'
        else:
            label = 'neutral'
            emotion = 'neutral'
        
        return {
            'label': label,
            'score': round(normalized_score, 3),
            'emotion': emotion,
            'confidence': round(confidence, 3)
        }
    
    def get_emoji(self, sentiment: Dict) -> str:
        """Get emoji representation of sentiment"""
        emotion_emojis = {
            'happy': '😊',
            'satisfied': '🙂',
            'neutral': '😐',
            'frustrated': '😟',
            'angry': '😠'
        }
        return emotion_emojis.get(sentiment.get('emotion', 'neutral'), '😐')
