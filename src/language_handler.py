"""
Language Handler - Multi-language support and translation
"""

from typing import Optional


class LanguageHandler:
    """Handles language detection and translation"""
    
    def __init__(self):
        """Initialize language handler"""
        self.supported_languages = ['en', 'ar']
        self.use_simple_translation = True  # Use simple for demo, can upgrade later
        
    def detect_language(self, text: str) -> str:
        """
        Detect language of text
        
        Args:
            text: Input text
            
        Returns:
            Language code ('en' or 'ar')
        """
        if not text:
            return 'en'
        
        # Simple Arabic detection (check for Arabic characters)
        arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        
        if arabic_chars > len(text) * 0.3:  # If 30%+ are Arabic
            return 'ar'
        
        return 'en'
    
    def translate(self, text: str, source: str = 'auto', 
                 target: str = 'en') -> str:
        """
        Translate text between languages
        
        Args:
            text: Text to translate
            source: Source language code
            target: Target language code
            
        Returns:
            Translated text
        """
        # For now, return original text
        # In production, integrate with Google Translate API or similar
        
        # Simple placeholder responses for demonstration
        if source == 'ar' and target == 'en':
            common_phrases = {
                'مرحبا': 'hello',
                'شكرا': 'thank you',
                'مساعدة': 'help',
                'مشكلة': 'problem'
            }
            for ar, en in common_phrases.items():
                if ar in text:
                    text = text.replace(ar, en)
        
        elif source == 'en' and target == 'ar':
            common_phrases = {
                'hello': 'مرحبا',
                'thank you': 'شكرا',
                'help': 'مساعدة',
                'problem': 'مشكلة'
            }
            for en, ar in common_phrases.items():
                if en.lower() in text.lower():
                    text = text.lower().replace(en.lower(), ar)
        
        return text
    
    def is_supported(self, language: str) -> bool:
        """Check if language is supported"""
        return language in self.supported_languages
