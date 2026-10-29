"""
Console Interface for Tech Support Chatbot
"""

import os
import sys
from colorama import init, Fore, Style

# Initialize colorama for Windows
init(autoreset=True)

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.chatbot_engine import ChatbotEngine
from src.analytics_engine import AnalyticsEngine
from src.export_manager import ExportManager


def print_banner():
    """Print chatbot banner"""
    print(Fore.CYAN + "\n" + "="*60)
    print(Fore.CYAN + "  Tech Support Assistant - Console Mode")
    print(Fore.CYAN + "="*60)
    print(Fore.YELLOW + "\n  Type your technical issues and I'll help you solve them!")
    print(Fore.YELLOW + "  Commands: /help, /clear, /stats, /export, /quit")
    print(Fore.CYAN + "="*60 + "\n")


def print_help():
    """Print available commands"""
    print(Fore.CYAN + "\nAvailable Commands:")
    print(Fore.GREEN + "  /help     " + Fore.WHITE + "- Show this help message")
    print(Fore.GREEN + "  /clear    " + Fore.WHITE + "- Clear conversation history")
    print(Fore.GREEN + "  /stats    " + Fore.WHITE + "- Show chatbot statistics")
    print(Fore.GREEN + "  /export   " + Fore.WHITE + "- Export conversation history")
    print(Fore.GREEN + "  /analytics" + Fore.WHITE + "- Show conversation analytics")
    print(Fore.GREEN + "  /quit     " + Fore.WHITE + "- Exit chatbot\n")


def print_stats(chatbot):
    """Print chatbot statistics"""
    stats = chatbot.get_statistics()
    
    print(Fore.CYAN + "\nChatbot Statistics:")
    print(Fore.GREEN + "  Conversations: " + Fore.WHITE + str(stats['conversation_count']))
    print(Fore.GREEN + "  Uptime: " + Fore.WHITE + stats['uptime_formatted'])
    print(Fore.GREEN + "  Intents Available: " + Fore.WHITE + str(stats['intents_available']))
    print(Fore.GREEN + "  Knowledge Base Size: " + Fore.WHITE + str(stats['knowledge_base_size']))
    print(Fore.GREEN + "  Learned Responses: " + Fore.WHITE + str(stats['learned_responses']))
    print()


def print_analytics(analytics, user_id):
    """Print conversation analytics"""
    report = analytics.generate_report(user_id)
    
    print(Fore.CYAN + "\nConversation Analytics:")
    
    # Conversation stats
    if 'conversation_stats' in report:
        stats = report['conversation_stats']
        print(Fore.GREEN + "  Total Messages: " + Fore.WHITE + str(stats.get('total_messages', 0)))
        print(Fore.GREEN + "  Average Sentiment: " + Fore.WHITE + stats.get('sentiment_label', 'neutral'))
        print(Fore.GREEN + "  Duration: " + Fore.WHITE + stats.get('duration', '0m'))
    
    # Intent distribution
    if report['intent_distribution']:
        print(Fore.CYAN + "\n  Top Intents:")
        for intent, count in sorted(report['intent_distribution'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(Fore.GREEN + f"    {intent}: " + Fore.WHITE + str(count))
    
    # Satisfaction score
    print(Fore.GREEN + "\n  Satisfaction Score: " + Fore.WHITE + f"{report['satisfaction_score']}/100")
    print()


def main():
    """Main console chatbot loop"""
    print_banner()
    
    # Initialize chatbot
    print(Fore.YELLOW + "[INFO] Initializing chatbot...")
    chatbot = ChatbotEngine()
    analytics = AnalyticsEngine(
        chatbot.context_manager,
        chatbot.sentiment_analyzer,
        chatbot.intent_matcher
    )
    export_manager = ExportManager(chatbot.context_manager)
    
    print(Fore.GREEN + "[OK] Chatbot ready!\n")
    
    user_id = "console_user"
    
    try:
        while True:
            # Get user input
            user_input = input(Fore.BLUE + "You: " + Fore.WHITE).strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith('/'):
                command = user_input.lower()
                
                if command == '/help':
                    print_help()
                    
                elif command == '/clear':
                    chatbot.clear_context(user_id)
                    print(Fore.GREEN + "[OK] Conversation cleared\n")
                    
                elif command == '/stats':
                    print_stats(chatbot)
                    
                elif command == '/analytics':
                    print_analytics(analytics, user_id)
                    
                elif command == '/export':
                    print(Fore.YELLOW + "\nExport format? (json/text/pdf): ", end='')
                    format = input().strip().lower()
                    if format in ['json', 'text', 'pdf']:
                        filepath = export_manager.export_conversation(user_id, format)
                        if filepath:
                            print(Fore.GREEN + f"[OK] Exported to: {filepath}\n")
                        else:
                            print(Fore.RED + "[ERROR] Export failed\n")
                    else:
                        print(Fore.RED + "[ERROR] Invalid format. Use json, text, or pdf\n")
                    
                elif command == '/quit' or command == '/exit':
                    print(Fore.YELLOW + "\nGoodbye! Thank you for using Tech Support Assistant.")
                    break
                    
                else:
                    print(Fore.RED + f"[ERROR] Unknown command: {command}")
                    print(Fore.YELLOW + "Type /help for available commands\n")
                
                continue
            
            # Process message
            response_data = chatbot.process_message(user_input, user_id, "en")
            
            # Display response
            response_text = response_data['response']
            sentiment = response_data['sentiment']
            intent = response_data['intent']
            confidence = response_data['confidence']
            
            print(Fore.GREEN + "Bot: " + Fore.WHITE + response_text)
            
            # Show metadata (optional, can be disabled)
            if False:  # Set to True to see debug info
                print(Fore.CYAN + f"  [Intent: {intent}, Confidence: {confidence:.2f}, " +
                      f"Sentiment: {sentiment['label']}]")
            
            print()  # New line for readability
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n[INFO] Interrupted by user")
    
    except Exception as e:
        print(Fore.RED + f"\n[ERROR] {e}")
    
    finally:
        # Cleanup
        print(Fore.YELLOW + "\n[INFO] Shutting down...")
        chatbot.shutdown()
        print(Fore.GREEN + "[OK] Chatbot stopped\n")


if __name__ == '__main__':
    main()
