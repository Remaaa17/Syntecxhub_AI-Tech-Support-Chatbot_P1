"""
Test Groq API - List available models
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

print("=" * 60)
print("Testing Groq API")
print("=" * 60)
print(f"API Key (first 20 chars): {api_key[:20]}...")
print()

# Try to list models
url = "https://api.groq.com/openai/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("Fetching available models...")
print("-" * 60)

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            models = data['data']
            print(f"\nFound {len(models)} models:\n")
            for model in models:
                model_id = model.get('id', 'unknown')
                print(f"  - {model_id}")
        else:
            print("\nResponse:", response.json())
    else:
        print(f"\nError: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\nException: {e}")

print("\n" + "=" * 60)

# Try a simple chat completion with a common model
print("\nTrying chat completion with llama3-8b-8192...")
print("-" * 60)

chat_url = "https://api.groq.com/openai/v1/chat/completions"
payload = {
    "model": "llama3-8b-8192",
    "messages": [
        {"role": "user", "content": "Say 'test successful' if you receive this"}
    ],
    "max_tokens": 50
}

try:
    response = requests.post(chat_url, headers=headers, json=payload, timeout=15)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if 'choices' in result:
            message = result['choices'][0]['message']['content']
            print(f"\nResponse: {message}")
            print("\n✅ API KEY IS WORKING!")
    else:
        print(f"\nError: {response.text[:300]}")
        
except Exception as e:
    print(f"\nException: {e}")

print("\n" + "=" * 60)
