#!/usr/bin/env python3
"""
Simple test to check if the web server is working correctly
"""

import requests
import json

def test_server():
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Testing CrewAI Web Server")
    print("=" * 40)
    
    # Test 1: Check if server is responding
    print("\n1. Testing server connection...")
    try:
        response = requests.get(base_url, timeout=5)
        print(f"✅ Server responding: {response.status_code}")
        print(f"   Content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            if "CrewAI Research System" in response.text:
                print("✅ HTML content looks correct")
            else:
                print("❌ HTML content seems wrong")
                print("First 500 characters:")
                print(response.text[:500])
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print("   Make sure the server is running at http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Test API endpoint
    print("\n2. Testing API endpoints...")
    try:
        api_response = requests.get(f"{base_url}/api/reports", timeout=5)
        print(f"✅ API responding: {api_response.status_code}")
        
        if api_response.status_code == 200:
            reports = api_response.json()
            print(f"   Found {len(reports)} reports")
        
    except Exception as e:
        print(f"❌ API Error: {e}")
    
    # Test 3: Test starting research (but don't wait for completion)
    print("\n3. Testing research start...")
    try:
        start_response = requests.post(
            f"{base_url}/start_research",
            json={"topic": "Test Topic"},
            timeout=5
        )
        print(f"✅ Research start: {start_response.status_code}")
        
        if start_response.status_code == 200:
            data = start_response.json()
            task_id = data.get('task_id')
            print(f"   Task ID: {task_id}")
            
            # Check task status
            status_response = requests.get(f"{base_url}/task_status/{task_id}", timeout=5)
            if status_response.status_code == 200:
                status = status_response.json()
                print(f"   Task status: {status.get('status')}")
        
    except Exception as e:
        print(f"❌ Research start error: {e}")
    
    print("\n" + "=" * 40)
    print("✅ Server test completed!")
    return True

if __name__ == "__main__":
    test_server()