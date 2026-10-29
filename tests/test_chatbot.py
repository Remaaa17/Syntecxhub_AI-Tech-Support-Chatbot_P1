"""
Basic tests for Tech Support Chatbot
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.chatbot_engine import ChatbotEngine
from src.intent_matcher import IntentMatcher
from src.knowledge_base import KnowledgeBase
from src.sentiment_analyzer import SentimentAnalyzer


def test_intent_matcher():
    """Test intent matching"""
    print("\n[TEST] Intent Matcher")
    print("=" * 50)
    
    matcher = IntentMatcher()
    
    test_cases = [
        ("hello", "greeting"),
        ("my wifi is not working", "wifi_issue"),
        ("computer is slow", "slow_computer"),
        ("forgot my password", "password_reset"),
        ("blue screen error", "blue_screen"),
    ]
    
    passed = 0
    for message, expected_intent in test_cases:
        result = matcher.match(message)
        actual_intent = result['intent']
        confidence = result['confidence']
        
        status = "[OK]" if actual_intent == expected_intent else "[FAIL]"
        print(f"{status} '{message}' -> {actual_intent} (conf: {confidence:.2f})")
        
        if actual_intent == expected_intent:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)


def test_knowledge_base():
    """Test knowledge base search"""
    print("\n[TEST] Knowledge Base")
    print("=" * 50)
    
    kb = KnowledgeBase()
    
    test_queries = [
        "what is python",
        "how to check windows version",
        "what is ram",
        "ssd vs hdd",
    ]
    
    passed = 0
    for query in test_queries:
        result = kb.search(query)
        
        if result and result['confidence'] > 0.6:
            print(f"[OK] '{query}' -> Found answer (conf: {result['confidence']:.2f})")
            passed += 1
        else:
            print(f"[FAIL] '{query}' -> No answer found")
    
    print(f"\nPassed: {passed}/{len(test_queries)}")
    return passed >= len(test_queries) * 0.75  # 75% pass rate


def test_sentiment_analyzer():
    """Test sentiment analysis"""
    print("\n[TEST] Sentiment Analyzer")
    print("=" * 50)
    
    analyzer = SentimentAnalyzer()
    
    test_cases = [
        ("I love this chatbot! It's amazing!", "positive"),
        ("This is terrible and frustrating", "negative"),
        ("How do I install Python?", "neutral"),
        ("Thank you so much! Very helpful!", "positive"),
        ("Not working at all, very angry", "negative"),
    ]
    
    passed = 0
    for message, expected in test_cases:
        result = analyzer.analyze(message)
        actual = result['label']
        score = result['score']
        
        status = "[OK]" if actual == expected else "[FAIL]"
        print(f"{status} '{message}' -> {actual} (score: {score:.2f})")
        
        if actual == expected:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed >= len(test_cases) * 0.8  # 80% pass rate


def test_chatbot_engine():
    """Test complete chatbot engine"""
    print("\n[TEST] Chatbot Engine")
    print("=" * 50)
    
    chatbot = ChatbotEngine()
    
    test_messages = [
        "Hello!",
        "My WiFi is not working",
        "How do I speed up my computer?",
        "Thank you for your help!",
    ]
    
    passed = 0
    for message in test_messages:
        response_data = chatbot.process_message(message, "test_user")
        
        if response_data and response_data['response']:
            print(f"[OK] User: {message}")
            print(f"     Bot: {response_data['response'][:60]}...")
            passed += 1
        else:
            print(f"[FAIL] No response for: {message}")
    
    print(f"\nPassed: {passed}/{len(test_messages)}")
    return passed == len(test_messages)


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*50)
    print("  Tech Support Chatbot - Test Suite")
    print("="*50)
    
    results = []
    
    results.append(("Intent Matcher", test_intent_matcher()))
    results.append(("Knowledge Base", test_knowledge_base()))
    results.append(("Sentiment Analyzer", test_sentiment_analyzer()))
    results.append(("Chatbot Engine", test_chatbot_engine()))
    
    print("\n" + "="*50)
    print("  Test Results Summary")
    print("="*50)
    
    for test_name, passed in results:
        status = "[PASSED]" if passed else "[FAILED]"
        print(f"{status} {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\nOverall: {total_passed}/{total_tests} test suites passed")
    
    if total_passed == total_tests:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print("\n[WARNING] Some tests failed")
        return 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    exit(exit_code)
