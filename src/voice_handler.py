"""
Voice Handler - Speech recognition and text-to-speech
"""

import os
from typing import Optional


class VoiceHandler:
    """Handles voice input and output"""
    
    def __init__(self):
        """Initialize voice handler"""
        self.tts_enabled = True
        self.stt_enabled = True
        
        # Try to import speech libraries
        self.speech_available = self._check_speech_libraries()
        
    def _check_speech_libraries(self) -> bool:
        """Check if speech libraries are available"""
        try:
            import speech_recognition
            import pyttsx3
            return True
        except ImportError:
            print("[INFO] Speech libraries not installed. Voice features disabled.")
            print("[INFO] Install with: pip install SpeechRecognition pyttsx3 pyaudio")
            return False
    
    def speech_to_text(self, audio_file: Optional[str] = None) -> Optional[str]:
        """
        Convert speech to text
        
        Args:
            audio_file: Path to audio file (optional, uses microphone if None)
            
        Returns:
            Recognized text or None
        """
        if not self.speech_available or not self.stt_enabled:
            return None
        
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            if audio_file:
                # From file
                with sr.AudioFile(audio_file) as source:
                    audio = recognizer.record(source)
            else:
                # From microphone
                with sr.Microphone() as source:
                    print("[INFO] Listening... Speak now!")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            return text
            
        except ImportError:
            print("[ERROR] speech_recognition not installed")
            return None
        except Exception as e:
            print(f"[ERROR] Speech recognition failed: {e}")
            return None
    
    def text_to_speech(self, text: str, save_to_file: Optional[str] = None) -> bool:
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            save_to_file: Path to save audio file (optional)
            
        Returns:
            True if successful
        """
        if not self.speech_available or not self.tts_enabled:
            return False
        
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            
            # Set properties
            engine.setProperty('rate', 150)  # Speed
            engine.setProperty('volume', 0.9)  # Volume (0-1)
            
            if save_to_file:
                engine.save_to_file(text, save_to_file)
                engine.runAndWait()
            else:
                engine.say(text)
                engine.runAndWait()
            
            return True
            
        except ImportError:
            print("[ERROR] pyttsx3 not installed")
            return False
        except Exception as e:
            print(f"[ERROR] Text-to-speech failed: {e}")
            return False
    
    def enable_tts(self, enabled: bool = True):
        """Enable or disable text-to-speech"""
        self.tts_enabled = enabled
    
    def enable_stt(self, enabled: bool = True):
        """Enable or disable speech-to-text"""
        self.stt_enabled = enabled
    
    def is_available(self) -> bool:
        """Check if voice features are available"""
        return self.speech_available
