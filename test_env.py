#!/usr/bin/env python3
"""
Test environment variables loading
"""

import os
from dotenv import load_dotenv

def test_env():
    print("🔍 Testing Environment Variables")
    print("=" * 40)
    
    # Load .env file
    load_dotenv()
    
    # Check for API keys
    keys_to_check = [
        "GROQ_API_KEY",
        "GEMINI_API_KEY", 
        "KIMI_API_KEY",
        "SERP_API_KEY"
    ]
    
    found_keys = {}
    for key in keys_to_check:
        value = os.getenv(key)
        if value:
            found_keys[key] = value[:20] + "..." if len(value) > 20 else value
            print(f"✅ {key}: {found_keys[key]}")
        else:
            print(f"❌ {key}: Not found")
    
    print(f"\n📊 Found {len(found_keys)} out of {len(keys_to_check)} API keys")
    
    if len(found_keys) >= 2:  # Need at least 2 keys for multi-LLM
        print("🎉 Sufficient API keys for multi-LLM setup!")
        return True
    else:
        print("⚠️  Need more API keys for optimal performance")
        return False

if __name__ == "__main__":
    test_env()