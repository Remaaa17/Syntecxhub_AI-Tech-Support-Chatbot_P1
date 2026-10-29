"""
Knowledge Base - Tech support Q&A database
"""

import json
import os
from typing import Dict, List, Optional
from difflib import SequenceMatcher


class KnowledgeBase:
    """Stores and retrieves technical knowledge"""
    
    def __init__(self):
        """Initialize knowledge base"""
        self.knowledge = self._load_knowledge()
        
    def _load_knowledge(self) -> List[Dict]:
        """Load knowledge from JSON file"""
        kb_path = os.path.join('data', 'knowledge_base.json')
        
        if os.path.exists(kb_path):
            with open(kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle both list and dict formats
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return data.get('knowledge', [])
                else:
                    return []
        else:
            return self._get_default_knowledge()
    
    def _get_default_knowledge(self) -> List[Dict]:
        """Return default tech support knowledge"""
        return [
            {
                "question": "What is Python?",
                "answer": "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used for web development, data analysis, artificial intelligence, and automation.",
                "keywords": ["python", "programming language", "what is python"],
                "category": "programming"
            },
            {
                "question": "How do I check my Windows version?",
                "answer": "To check Windows version:\n1. Press Win + R\n2. Type 'winver' and press Enter\nOr: Settings > System > About",
                "keywords": ["windows version", "check windows", "os version"],
                "category": "operating_system"
            },
            {
                "question": "What is an IP address?",
                "answer": "An IP address is a unique numerical label assigned to each device connected to a network. It identifies the device and enables communication. Example: 192.168.1.1",
                "keywords": ["ip address", "network", "what is ip"],
                "category": "networking"
            },
            {
                "question": "How do I find my IP address?",
                "answer": "To find your IP address:\nWindows: Open CMD and type 'ipconfig'\nMac: System Preferences > Network\nLinux: Terminal command 'ifconfig' or 'ip addr'",
                "keywords": ["find ip", "my ip address", "check ip"],
                "category": "networking"
            },
            {
                "question": "What is RAM?",
                "answer": "RAM (Random Access Memory) is temporary memory that your computer uses to store data for currently running programs. More RAM means better multitasking. Common sizes: 4GB, 8GB, 16GB, 32GB.",
                "keywords": ["ram", "memory", "what is ram"],
                "category": "hardware"
            },
            {
                "question": "What is SSD vs HDD?",
                "answer": "SSD (Solid State Drive) uses flash memory - faster, quieter, more expensive.\nHDD (Hard Disk Drive) uses spinning disks - slower, cheaper, larger capacity.\nSSD is recommended for OS and programs, HDD for storage.",
                "keywords": ["ssd", "hdd", "storage", "hard drive"],
                "category": "hardware"
            },
            {
                "question": "How do I clear cache?",
                "answer": "Clear cache in browsers:\nChrome: Ctrl+Shift+Del > Select cache\nFirefox: Ctrl+Shift+Del > Cookies and Cache\nEdge: Ctrl+Shift+Del > Cached files\nOr: Settings > Privacy > Clear browsing data",
                "keywords": ["clear cache", "delete cache", "cache"],
                "category": "browser"
            },
            {
                "question": "What is a firewall?",
                "answer": "A firewall is security software/hardware that monitors and controls incoming/outgoing network traffic. It acts as a barrier between trusted and untrusted networks, blocking malicious access.",
                "keywords": ["firewall", "network security", "what is firewall"],
                "category": "security"
            },
            {
                "question": "How do I update drivers?",
                "answer": "Update drivers:\n1. Right-click Start > Device Manager\n2. Find the device\n3. Right-click > Update driver\n4. Choose 'Search automatically'\nOr download from manufacturer's website.",
                "keywords": ["update drivers", "driver update", "device drivers"],
                "category": "drivers"
            },
            {
                "question": "What is BIOS?",
                "answer": "BIOS (Basic Input/Output System) is firmware that initializes hardware during boot. Access it by pressing F2, F12, or Del during startup (varies by manufacturer). Used to change boot order, enable virtualization, etc.",
                "keywords": ["bios", "boot", "what is bios"],
                "category": "system"
            },
            {
                "question": "How do I take a screenshot?",
                "answer": "Screenshot methods:\nWindows: Win+PrintScreen (full screen), Win+Shift+S (snipping tool)\nMac: Cmd+Shift+3 (full), Cmd+Shift+4 (selection)\nLinux: PrintScreen or use Screenshot app",
                "keywords": ["screenshot", "print screen", "capture screen"],
                "category": "tips"
            },
            {
                "question": "What is cloud storage?",
                "answer": "Cloud storage saves data on remote servers accessible via internet. Popular services: Google Drive (15GB free), OneDrive, Dropbox, iCloud. Benefits: access anywhere, automatic backup, file sharing.",
                "keywords": ["cloud storage", "online storage", "backup"],
                "category": "storage"
            },
            {
                "question": "How do I speed up my computer?",
                "answer": "Speed up tips:\n1. Disable startup programs\n2. Uninstall unused software\n3. Run disk cleanup\n4. Defragment HDD (not SSD)\n5. Add more RAM\n6. Upgrade to SSD\n7. Check for malware\n8. Update Windows",
                "keywords": ["speed up", "faster computer", "improve performance"],
                "category": "performance"
            },
            {
                "question": "What is VPN?",
                "answer": "VPN (Virtual Private Network) encrypts your internet connection and hides your IP address, providing privacy and security. Used for: secure browsing, accessing blocked content, remote work.",
                "keywords": ["vpn", "virtual private network", "secure connection"],
                "category": "security"
            },
            {
                "question": "How do I recover deleted files?",
                "answer": "File recovery:\n1. Check Recycle Bin\n2. Use File History (Windows)\n3. Try Recuva (free software)\n4. Check cloud backup\n5. Professional recovery for critical data\nNote: Don't save new files to same drive!",
                "keywords": ["recover files", "deleted files", "file recovery"],
                "category": "data_recovery"
            }
        ]
    
    def search(self, query: str, threshold: float = 0.6) -> Optional[Dict]:
        """
        Search knowledge base for relevant answer
        
        Args:
            query: User's question
            threshold: Minimum confidence score
            
        Returns:
            Dict with answer and confidence, or None
        """
        if not query or not query.strip():
            return None
        
        query = query.lower().strip()
        best_match = None
        best_score = 0.0
        
        for item in self.knowledge:
            # Calculate match score
            score = 0.0
            
            # Check question similarity
            question_score = self._calculate_similarity(
                query, 
                item['question'].lower()
            )
            score = max(score, question_score)
            
            # Check keyword matches
            query_words = set(query.split())
            for keyword in item['keywords']:
                keyword_words = set(keyword.lower().split())
                if query_words & keyword_words:  # Intersection
                    keyword_score = len(query_words & keyword_words) / len(keyword_words)
                    score = max(score, keyword_score)
                
                # Check if keyword phrase is in query
                if keyword.lower() in query:
                    score = max(score, 0.9)
            
            if score > best_score:
                best_score = score
                best_match = item
        
        if best_match and best_score >= threshold:
            return {
                'answer': best_match['answer'],
                'question': best_match['question'],
                'category': best_match.get('category', 'general'),
                'confidence': best_score
            }
        
        return None
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, str1, str2).ratio()
    
    def get_size(self) -> int:
        """Get number of knowledge entries"""
        return len(self.knowledge)
    
    def get_categories(self) -> List[str]:
        """Get list of knowledge categories"""
        categories = set()
        for item in self.knowledge:
            if 'category' in item:
                categories.add(item['category'])
        return sorted(list(categories))
    
    def add_knowledge(self, question: str, answer: str, 
                     keywords: List[str], category: str = "general"):
        """Add new knowledge entry"""
        new_entry = {
            'question': question,
            'answer': answer,
            'keywords': keywords,
            'category': category
        }
        self.knowledge.append(new_entry)
    
    def save(self):
        """Save knowledge base to file"""
        kb_path = os.path.join('data', 'knowledge_base.json')
        os.makedirs('data', exist_ok=True)
        
        with open(kb_path, 'w', encoding='utf-8') as f:
            json.dump({'knowledge': self.knowledge}, f, indent=2, ensure_ascii=False)
