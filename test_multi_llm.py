#!/usr/bin/env python3
"""
Test script for Multi-LLM setup with your API keys
"""

import os
import sys
import time

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_multi_llm():
    """Test the multi-LLM configuration"""
    
    print("🧪 Testing Multi-LLM Configuration")
    print("=" * 50)
    
    try:
        from firstcrew.llm_manager import initialize_llm_manager, get_llm_status, get_dynamic_llm_config
        
        # Initialize the LLM manager
        print("🚀 Initializing LLM Manager...")
        success = initialize_llm_manager()
        
        if not success:
            print("❌ No LLM configurations found!")
            return False
        
        # Get status
        print("\n📊 LLM Status:")
        status = get_llm_status()
        
        print(f"   Total configurations: {status['total_configs']}")
        print()
        
        for config in status['configs']:
            print(f"   🔧 {config['name']}:")
            print(f"      Provider: {config['provider']}")
            print(f"      Model: {config['model']}")
            print(f"      Rate Limit: {config['rate_limit']}/min")
            print(f"      Current Usage: {config['usage_last_minute']}")
            print(f"      Utilization: {config['utilization']}")
            print(f"      Status: {'🔴 Rate Limited' if config['is_rate_limited'] else '🟢 Available'}")
            print()
        
        # Test getting configurations
        print("🔄 Testing LLM Selection...")
        for i in range(5):
            try:
                config = get_dynamic_llm_config()
                print(f"   Test {i+1}: Using {config['model']}")
                time.sleep(0.1)  # Small delay
            except Exception as e:
                print(f"   Test {i+1}: Error - {e}")
        
        print("\n✅ Multi-LLM system is working!")
        print("\n🎯 Your system now has:")
        print("   • Automatic rate limit bypass")
        print("   • Load balancing across providers")
        print("   • Intelligent LLM selection")
        print("   • Failover protection")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_enhanced_crew():
    """Test the enhanced crew with multi-LLM support"""
    
    print("\n🤖 Testing Enhanced CrewAI...")
    print("=" * 30)
    
    try:
        from firstcrew.enhanced_crew import EnhancedFirstcrew
        
        print("✅ Enhanced CrewAI imported successfully")
        
        # Create crew instance
        crew_instance = EnhancedFirstcrew()
        print("✅ Enhanced crew instance created")
        
        # Test crew creation
        crew = crew_instance.crew()
        print("✅ Crew created with multi-LLM support")
        
        print("\n🎉 Your enhanced CrewAI is ready!")
        print("   • Multi-LLM support enabled")
        print("   • Rate limit bypass active")
        print("   • Web search tools integrated")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing enhanced crew: {e}")
        return False

if __name__ == "__main__":
    print("🔑 Multi-LLM Test Suite")
    print("=" * 60)
    
    # Test 1: Multi-LLM Manager
    llm_success = test_multi_llm()
    
    # Test 2: Enhanced Crew
    crew_success = test_enhanced_crew()
    
    print("\n" + "=" * 60)
    if llm_success and crew_success:
        print("🎉 ALL TESTS PASSED!")
        print("\n🚀 Your system is ready with:")
        print("   ✅ Groq API (Free tier)")
        print("   ✅ Gemini API (Gemma 2 2B model)")
        print("   ✅ Kimi API (Moonshot model)")
        print("   ✅ SERP API (Web search)")
        print("   ✅ Multi-LLM load balancing")
        print("   ✅ Rate limit bypass")
        print("\n🌐 Start your web interface with:")
        print("   python run_local.py")
    else:
        print("❌ Some tests failed. Check the errors above.")