"""
Intent Matcher - Pattern-based intent recognition for tech support
"""

import json
import re
import os
from typing import Dict, List, Optional
from difflib import SequenceMatcher


class IntentMatcher:
    """Matches user input to predefined intents using pattern matching"""
    
    def __init__(self):
        """Initialize intent matcher with patterns"""
        self.intents = self._load_intents()
        self.fallback_responses = [
            "I'm not sure I understand. Can you rephrase your technical issue?",
            "Could you provide more details about the problem you're experiencing?",
            "I'm here to help with tech support. What specific issue are you facing?"
        ]
        
    def _load_intents(self) -> List[Dict]:
        """Load intents from JSON file"""
        intents_path = os.path.join('data', 'intents.json')
        
        if os.path.exists(intents_path):
            with open(intents_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('intents', [])
        else:
            # Return default tech support intents
            return self._get_default_intents()
    
    def _get_default_intents(self) -> List[Dict]:
        """Return default tech support intents"""
        return [
            {
                "tag": "greeting",
                "patterns": [
                    "hi", "hello", "hey", "good morning", "good afternoon",
                    "good evening", "greetings", "what's up", "sup"
                ],
                "responses": [
                    "Hello! I'm your Tech Support Assistant. How can I help you today?",
                    "Hi there! Having technical issues? I'm here to help!",
                    "Greetings! What technical problem can I assist you with?"
                ]
            },
            {
                "tag": "goodbye",
                "patterns": [
                    "bye", "goodbye", "see you", "later", "exit", "quit",
                    "thanks bye", "thank you bye"
                ],
                "responses": [
                    "Goodbye! Feel free to reach out if you need more tech support.",
                    "Have a great day! Come back if you encounter any issues.",
                    "Take care! I'm always here to help with technical problems."
                ]
            },
            {
                "tag": "thanks",
                "patterns": [
                    "thanks", "thank you", "appreciate it", "thanks a lot",
                    "that helped", "helpful", "perfect"
                ],
                "responses": [
                    "You're welcome! Glad I could help resolve your issue.",
                    "Happy to help! Let me know if you need anything else.",
                    "No problem! Feel free to ask if you have more questions."
                ]
            },
            {
                "tag": "help",
                "patterns": [
                    "help", "assist", "support", "what can you do",
                    "how to use", "capabilities", "features"
                ],
                "responses": [
                    "I can help with:\n- Software installation issues\n- Error troubleshooting\n- Network problems\n- Password resets\n- System performance\n- Programming questions\nWhat do you need help with?"
                ]
            },
            {
                "tag": "wifi_issue",
                "patterns": [
                    "wifi not working", "no internet", "can't connect to wifi",
                    "internet down", "wifi slow", "connection problem",
                    "no connection", "disconnected from wifi"
                ],
                "responses": [
                    "Let's fix your WiFi issue. Try these steps:\n1. Restart your router (unplug for 30 seconds)\n2. Forget and reconnect to the network\n3. Check if other devices can connect\n4. Update network drivers\nDid any of these help?"
                ]
            },
            {
                "tag": "slow_computer",
                "patterns": [
                    "computer slow", "pc running slow", "laptop lagging",
                    "system slow", "performance issue", "computer freezing",
                    "slow boot", "takes long to start"
                ],
                "responses": [
                    "To speed up your computer:\n1. Close unnecessary programs\n2. Check Task Manager for resource usage (Ctrl+Shift+Esc)\n3. Run Disk Cleanup\n4. Disable startup programs\n5. Check for malware\n6. Upgrade RAM if needed\nWhich step would you like details on?"
                ]
            },
            {
                "tag": "password_reset",
                "patterns": [
                    "forgot password", "reset password", "can't login",
                    "locked out", "password not working", "change password"
                ],
                "responses": [
                    "For password reset:\n1. Click 'Forgot Password' on login page\n2. Enter your email/username\n3. Check email for reset link\n4. Create a strong new password\n5. Use a password manager\nWhich service do you need to reset?"
                ]
            },
            {
                "tag": "software_install",
                "patterns": [
                    "how to install", "installation error", "can't install",
                    "setup failed", "install problem", "download issue"
                ],
                "responses": [
                    "For software installation:\n1. Download from official website only\n2. Run as administrator\n3. Disable antivirus temporarily\n4. Check system requirements\n5. Install required dependencies\nWhat software are you trying to install?"
                ]
            },
            {
                "tag": "blue_screen",
                "patterns": [
                    "blue screen", "bsod", "system crash", "computer crashed",
                    "blue screen error", "stop error"
                ],
                "responses": [
                    "Blue Screen of Death (BSOD) troubleshooting:\n1. Note the error code\n2. Boot into Safe Mode\n3. Update drivers\n4. Check for Windows updates\n5. Run memory diagnostic\n6. Check hard drive health\nDo you remember the error code?"
                ]
            },
            {
                "tag": "printer_issue",
                "patterns": [
                    "printer not working", "can't print", "printer offline",
                    "print job stuck", "printer error", "paper jam"
                ],
                "responses": [
                    "Printer troubleshooting:\n1. Check printer is powered on and connected\n2. Set as default printer\n3. Clear print queue\n4. Update printer drivers\n5. Run Windows printer troubleshooter\n6. Check ink/toner levels\nIs the printer showing any error lights?"
                ]
            },
            {
                "tag": "email_issue",
                "patterns": [
                    "email not working", "can't send email", "can't receive email",
                    "email error", "outlook problem", "gmail issue"
                ],
                "responses": [
                    "Email troubleshooting:\n1. Check internet connection\n2. Verify email settings (SMTP/IMAP)\n3. Check spam folder\n4. Clear cache and cookies\n5. Try different browser/app\n6. Check storage quota\nWhich email service are you using?"
                ]
            },
            {
                "tag": "virus_malware",
                "patterns": [
                    "virus", "malware", "computer infected", "suspicious program",
                    "pop-ups", "adware", "ransomware", "trojan"
                ],
                "responses": [
                    "Malware removal steps:\n1. Disconnect from internet\n2. Boot into Safe Mode\n3. Run Windows Defender full scan\n4. Use Malwarebytes (free)\n5. Remove suspicious programs\n6. Reset browser settings\n7. Change important passwords\nHave you run an antivirus scan yet?"
                ]
            },
            {
                "tag": "backup_data",
                "patterns": [
                    "backup", "data backup", "how to backup", "lost files",
                    "recover files", "data recovery", "save files"
                ],
                "responses": [
                    "Data backup options:\n1. Cloud storage (Google Drive, OneDrive, Dropbox)\n2. External hard drive\n3. Windows Backup tool\n4. File History feature\n5. System Image backup\nFor lost files, try:\n- Recycle Bin\n- File recovery software (Recuva)\n- Previous Versions feature\nWhat do you need to backup?"
                ]
            },
            {
                "tag": "update_error",
                "patterns": [
                    "update failed", "windows update error", "update stuck",
                    "can't update", "update problem", "update loop"
                ],
                "responses": [
                    "Windows Update troubleshooting:\n1. Run Windows Update Troubleshooter\n2. Clear update cache (C:\\Windows\\SoftwareDistribution)\n3. Restart Windows Update service\n4. Check disk space (20GB+ free)\n5. Disable third-party antivirus\n6. Manual update from Microsoft Catalog\nWhat error code are you seeing?"
                ]
            },
            {
                "tag": "programming_help",
                "patterns": [
                    "code error", "python error", "javascript error", "coding help",
                    "syntax error", "bug", "debug", "programming problem"
                ],
                "responses": [
                    "Programming support:\n1. Read the error message carefully\n2. Check syntax (brackets, semicolons)\n3. Verify variable names and types\n4. Use print statements for debugging\n5. Check documentation\n6. Search error on StackOverflow\nWhat programming language and error are you getting?"
                ]
            },
            {
                "tag": "system_requirements",
                "patterns": [
                    "system requirements", "minimum specs", "can i run",
                    "hardware requirements", "specs needed"
                ],
                "responses": [
                    "I can help check system requirements. Please specify:\n- What software/game?\n- Your current specs (CPU, RAM, GPU)?\n\nGeneral guidelines:\n- Basic use: 4GB RAM, i3 processor\n- Gaming: 8-16GB RAM, dedicated GPU\n- Video editing: 16GB+ RAM, powerful CPU\n- Programming: 8GB RAM minimum"
                ]
            }
        ]
    
    def match(self, user_input: str) -> Dict:
        """
        Match user input to an intent
        
        Args:
            user_input: User's message
            
        Returns:
            Dictionary with intent, confidence, and response
        """
        if not user_input or not user_input.strip():
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'response': self.fallback_responses[0]
            }
        
        user_input = user_input.lower().strip()
        best_match = None
        best_score = 0.0
        
        # Try to match patterns
        for intent in self.intents:
            for pattern in intent['patterns']:
                # Calculate similarity score
                score = self._calculate_similarity(user_input, pattern.lower())
                
                # Check for exact phrase match
                if pattern.lower() in user_input:
                    score = max(score, 0.9)
                
                # Check for keyword matches
                pattern_words = set(pattern.lower().split())
                input_words = set(user_input.split())
                common_words = pattern_words & input_words
                if common_words:
                    word_match_score = len(common_words) / len(pattern_words)
                    score = max(score, word_match_score * 0.8)
                
                if score > best_score:
                    best_score = score
                    best_match = intent
        
        # Return result
        if best_match and best_score > 0.5:
            import random
            return {
                'intent': best_match['tag'],
                'confidence': best_score,
                'response': random.choice(best_match['responses'])
            }
        else:
            import random
            return {
                'intent': 'unknown',
                'confidence': best_score,
                'response': random.choice(self.fallback_responses)
            }
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity score between two strings"""
        return SequenceMatcher(None, str1, str2).ratio()
    
    def get_available_intents(self) -> List[str]:
        """Get list of available intent tags"""
        return [intent['tag'] for intent in self.intents]
    
    def add_custom_intent(self, tag: str, patterns: List[str], 
                          responses: List[str]):
        """Add a custom intent at runtime"""
        new_intent = {
            'tag': tag,
            'patterns': patterns,
            'responses': responses
        }
        self.intents.append(new_intent)
