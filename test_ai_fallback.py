"""
Test AI Fallback directly
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import AI fallback
from src.ai_fallback import AIFallback

# Initialize
ai = AIFallback()

print("=" * 60)
print("AI Fallback Test")
print("=" * 60)
print(f"API Key set: {'Yes' if ai.api_key else 'No'}")
print(f"API Key (first 20 chars): {ai.api_key[:20] if ai.api_key else 'None'}...")
print(f"Enabled: {ai.enabled}")
print(f"Model: {ai.model}")
print("=" * 60)

# Test question
question = "What is Docker?"
print(f"\nTesting question: '{question}'")
print("-" * 60)

result = ai.get_ai_response(question)

print("\nResult:")
print(f"Type: {type(result)}")
if result:
    print(f"Answer length: {len(result.get('answer', ''))} chars")
    print(f"Source: {result.get('source', 'N/A')}")
    print(f"Confidence: {result.get('confidence', 0)}")
    print(f"\nAnswer preview (first 200 chars):")
    print(result.get('answer', 'No answer')[:200] + "...")
else:
    print("Result is None!")

print("\n" + "=" * 60)
