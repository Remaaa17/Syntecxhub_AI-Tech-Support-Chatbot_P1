"""
Context Manager - Maintains conversation history and context
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


class ContextManager:
    """Manages conversation context and history"""
    
    def __init__(self, max_context_length: int = 50):
        """
        Initialize context manager
        
        Args:
            max_context_length: Maximum messages to store per user
        """
        self.max_context_length = max_context_length
        self.contexts = defaultdict(list)
        self.metadata = defaultdict(dict)
        self._load_contexts()
        
    def add_message(self, user_id: str, message: str, sender: str = "user"):
        """
        Add message to conversation context
        
        Args:
            user_id: Unique user identifier
            message: Message text
            sender: "user" or "bot"
        """
        timestamp = datetime.now().isoformat()
        
        message_data = {
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }
        
        self.contexts[user_id].append(message_data)
        
        # Trim context if too long
        if len(self.contexts[user_id]) > self.max_context_length:
            self.contexts[user_id] = self.contexts[user_id][-self.max_context_length:]
        
        # Update metadata
        if user_id not in self.metadata:
            self.metadata[user_id] = {
                'first_message': timestamp,
                'message_count': 0
            }
        
        self.metadata[user_id]['last_message'] = timestamp
        self.metadata[user_id]['message_count'] += 1
    
    def get_context(self, user_id: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Get conversation context for a user
        
        Args:
            user_id: User identifier
            limit: Number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        context = self.contexts.get(user_id, [])
        
        if limit:
            return context[-limit:]
        return context
    
    def get_last_user_message(self, user_id: str) -> Optional[str]:
        """Get the last message from user"""
        context = self.contexts.get(user_id, [])
        
        for message in reversed(context):
            if message['sender'] == 'user':
                return message['message']
        
        return None
    
    def get_last_bot_message(self, user_id: str) -> Optional[str]:
        """Get the last message from bot"""
        context = self.contexts.get(user_id, [])
        
        for message in reversed(context):
            if message['sender'] == 'bot':
                return message['message']
        
        return None
    
    def clear_context(self, user_id: str):
        """Clear conversation context for a user"""
        if user_id in self.contexts:
            self.contexts[user_id] = []
        if user_id in self.metadata:
            self.metadata[user_id] = {
                'first_message': datetime.now().isoformat(),
                'message_count': 0
            }
    
    def get_active_count(self) -> int:
        """Get number of active conversation contexts"""
        return len(self.contexts)
    
    def get_user_metadata(self, user_id: str) -> Dict:
        """Get metadata for a user"""
        return self.metadata.get(user_id, {})
    
    def get_conversation_summary(self, user_id: str) -> Dict:
        """Get summary statistics for a conversation"""
        context = self.contexts.get(user_id, [])
        metadata = self.metadata.get(user_id, {})
        
        user_messages = sum(1 for msg in context if msg['sender'] == 'user')
        bot_messages = sum(1 for msg in context if msg['sender'] == 'bot')
        
        return {
            'total_messages': len(context),
            'user_messages': user_messages,
            'bot_messages': bot_messages,
            'first_message': metadata.get('first_message'),
            'last_message': metadata.get('last_message')
        }
    
    def save(self):
        """Save contexts to file"""
        context_path = os.path.join('data', 'conversations.json')
        os.makedirs('data', exist_ok=True)
        
        # Convert defaultdict to regular dict for JSON serialization
        data = {
            'contexts': dict(self.contexts),
            'metadata': dict(self.metadata)
        }
        
        with open(context_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_contexts(self):
        """Load contexts from file"""
        context_path = os.path.join('data', 'conversations.json')
        
        if os.path.exists(context_path):
            try:
                with open(context_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Load contexts
                    for user_id, messages in data.get('contexts', {}).items():
                        self.contexts[user_id] = messages
                    
                    # Load metadata
                    for user_id, meta in data.get('metadata', {}).items():
                        self.metadata[user_id] = meta
            except Exception as e:
                print(f"[WARNING] Could not load contexts: {e}")
