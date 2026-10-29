"""
AI Fallback - Uses free LLM API when knowledge base has no answer
"""

import requests
import os
from typing import Optional, Dict


class AIFallback:
    """Provides AI-powered responses when rule-based systems fail"""
    
    def __init__(self):
        """Initialize AI fallback with Groq API"""
        # Using Groq API with GPT-OSS 120B (flagship model with 120B parameters)
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = os.getenv('GROQ_API_KEY', '')  # Load from environment variable
        self.model = "openai/gpt-oss-120b"  # Current production flagship model
        self.enabled = bool(self.api_key)  # Only enable if API key is set
        self.max_tokens = 1200
        self.temperature = 0.7
        
        if not self.api_key:
            print("[WARNING] GROQ_API_KEY not set. AI fallback disabled. Set it in .env file.")
        else:
            print(f"[OK] AI Fallback initialized with model: {self.model}")
        
    def get_ai_response(self, question: str, context: str = "") -> Optional[Dict]:
        """
        Get AI-generated response for a question
        
        Args:
            question: User's question
            context: Optional context from conversation
            
        Returns:
            Dictionary with response and metadata, or None if failed
        """
        if not self.enabled:
            print(f"[WARNING] AI fallback disabled. API key not set.")
            return None
        
        print(f"[INFO] AI Fallback enabled. Calling Groq API...")
        
        try:
            # Format prompt for tech support
            system_prompt = self._get_system_prompt(context)
            
            # Try Groq API
            response = self._call_groq_api(system_prompt, question)
            
            if response:
                print(f"[INFO] Groq API success: {len(response)} characters")
                return {
                    'answer': response,
                    'source': 'ai_fallback_groq',
                    'confidence': 0.85,
                    'model': 'gpt-oss-120b'
                }
            
            print(f"[WARNING] Groq API returned empty response. Using simple fallback.")
            # Fallback to simple response
            return self._get_simple_fallback(question)
            
        except Exception as e:
            print(f"[ERROR] AI Fallback exception: {e}")
            return self._get_simple_fallback(question)
    
    def _get_system_prompt(self, context: str = "") -> str:
        """Get system prompt for tech support"""
        
        system_prompt = """You are an expert Tech Support Assistant with deep knowledge in:
- Software installation and troubleshooting
- Network and WiFi configuration
- System performance optimization
- Programming and coding issues
- Password recovery and security
- Error diagnosis and resolution
- Hardware compatibility
- Operating system issues

IMPORTANT FORMATTING RULES:
- Do NOT use markdown symbols (*, #, |, -, etc.)
- Do NOT use tables with pipes (|)
- Use plain text only
- Use clear headings on separate lines
- Use bullet points with simple dashes or numbers
- Use line breaks to separate sections
- Keep formatting clean and readable

Provide clear, accurate, and helpful technical support. Use step-by-step instructions when appropriate.
Be concise but thorough. Format responses in plain text without markdown."""
        
        if context:
            system_prompt += f"\n\nConversation Context: {context}"
        
        return system_prompt
    
    def _call_groq_api(self, system_prompt: str, question: str) -> Optional[str]:
        """Call Groq API with Qwen model"""
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            print(f"[INFO] Calling Groq API with model: {self.model}")
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=15
            )
            
            print(f"[INFO] Groq API status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    message = result['choices'][0].get('message', {})
                    content = message.get('content', '')
                    cleaned = self._clean_response(content)
                    if cleaned:
                        return cleaned
                    else:
                        print(f"[WARNING] Response too short after cleaning")
            else:
                error_text = response.text[:200]
                print(f"[ERROR] Groq API error {response.status_code}: {error_text}")
            
            return None
            
        except requests.exceptions.Timeout:
            print("[ERROR] Groq API timeout after 15 seconds")
            return None
        except Exception as e:
            print(f"[ERROR] Groq API exception: {type(e).__name__}: {str(e)}")
            return None
    
    def _clean_response(self, text: str) -> str:
        """Clean and format AI response"""
        
        # Remove prompt echo
        text = text.strip()
        
        # Remove common prefixes
        prefixes = ['Answer:', 'Response:', 'Solution:']
        for prefix in prefixes:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
        
        # Ensure it's not too short
        if len(text) < 10:
            return None
        
        return text
    
    def _get_simple_fallback(self, question: str) -> Dict:
        """Simple rule-based fallback when AI fails"""
        
        question_lower = question.lower()
        
        # Detect question type
        if any(word in question_lower for word in ['install', 'setup', 'download']):
            answer = "To install software:\n1. Download from the official website\n2. Run the installer as administrator\n3. Follow the installation wizard\n4. Restart your computer if prompted\n\nWhat specific software are you trying to install?"
        
        elif any(word in question_lower for word in ['error', 'crash', 'not working']):
            answer = "For troubleshooting errors:\n1. Note the exact error message\n2. Restart the application\n3. Check for updates\n4. Search the error code online\n5. Check system logs\n\nCan you share the specific error message?"
        
        elif any(word in question_lower for word in ['slow', 'performance', 'lag']):
            answer = "To improve performance:\n1. Close unnecessary programs\n2. Check Task Manager for resource usage\n3. Clear temporary files\n4. Update drivers\n5. Check for malware\n6. Consider upgrading hardware (RAM/SSD)\n\nWhat specifically is running slow?"
        
        elif any(word in question_lower for word in ['password', 'forgot', 'login']):
            answer = "For password issues:\n1. Use 'Forgot Password' link\n2. Check email for reset instructions\n3. Try common password variations\n4. Contact account support\n5. Check password manager\n\nWhich service are you trying to access?"
        
        elif any(word in question_lower for word in ['backup', 'recover', 'lost']):
            answer = "For data backup/recovery:\n1. Check Recycle Bin\n2. Use File History (Windows)\n3. Check cloud backups (OneDrive, Google Drive)\n4. Try file recovery software (Recuva)\n5. Contact professional data recovery if critical\n\nWhat type of data did you lose?"
        
        else:
            answer = "I can help you with that tech support question. To provide the best answer, could you give me more details?\n\nI specialize in:\n- Software installation\n- Error troubleshooting\n- Performance issues\n- Network problems\n- Password recovery\n- Data backup\n\nWhat specific issue are you facing?"
        
        return {
            'answer': answer,
            'source': 'simple_fallback',
            'confidence': 0.5,
            'model': 'rule-based'
        }
    
    def enable(self):
        """Enable AI fallback"""
        self.enabled = True
    
    def disable(self):
        """Disable AI fallback"""
        self.enabled = False
    
    def set_api_key(self, api_key: str):
        """Set Groq API key"""
        self.api_key = api_key
    
    def set_model(self, model: str):
        """Change the AI model"""
        self.model = model


# Available Groq Models (October 2026):
"""
Current Production Models:

1. openai/gpt-oss-120b (CURRENT - Flagship)
   - 120B parameters
   - Built-in browser search and code execution
   - Best reasoning capabilities
   
2. openai/gpt-oss-20b
   - 20B parameters
   - Faster, lighter alternative

3. qwen/qwen3.8-27b
   - 27B parameters
   - Qwen model family

4. allam-2-7b
   - 7B parameters
   - Lightweight option

Note: Many older models (llama3-8b-8192, llama-3.3-70b-versatile, etc.) 
have been decommissioned. Check https://console.groq.com/docs/deprecations 
for the latest model recommendations.
"""
