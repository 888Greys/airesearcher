#!/usr/bin/env python3
"""
Test script to demonstrate API access to your running CrewAI system
"""

import requests
import json
import time

# Your server URL (change if different)
BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("🧪 Testing CrewAI Research System API")
    print("=" * 50)
    
    # Test 1: Start a research task
    print("\n1. 🚀 Starting research task...")
    try:
        response = requests.post(f"{BASE_URL}/start_research", 
                               json={"topic": "Quantum Computing 2025"})
        
        if response.status_code == 200:
            data = response.json()
            task_id = data['task_id']
            print(f"✅ Research started! Task ID: {task_id}")
            
            # Test 2: Monitor progress
            print(f"\n2. 📊 Monitoring progress for task {task_id}...")
            for i in range(10):  # Check 10 times
                status_response = requests.get(f"{BASE_URL}/task_status/{task_id}")
                if status_response.status_code == 200:
                    status = status_response.json()
                    print(f"   Status: {status['status']} - {status.get('progress', 'Processing...')}")
                    
                    if status['status'] in ['completed', 'failed']:
                        break
                
                time.sleep(3)  # Wait 3 seconds between checks
            
            # Test 3: Get report if completed
            if status['status'] == 'completed':
                print(f"\n3. 📄 Retrieving report content...")
                report_response = requests.get(f"{BASE_URL}/api/report/{task_id}")
                if report_response.status_code == 200:
                    report = report_response.json()
                    print(f"✅ Report retrieved!")
                    print(f"   Topic: {report['topic']}")
                    print(f"   Length: {len(report['content'])} characters")
                    print(f"   Preview: {report['content'][:200]}...")
                    
                    # Save report locally
                    with open(f"downloaded_report_{task_id}.md", 'w', encoding='utf-8') as f:
                        f.write(report['content'])
                    print(f"💾 Report saved as: downloaded_report_{task_id}.md")
        
        else:
            print(f"❌ Failed to start research: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure it's running at http://127.0.0.1:5000")
        return
    
    # Test 4: List all reports
    print(f"\n4. 📚 Listing all completed reports...")
    try:
        reports_response = requests.get(f"{BASE_URL}/api/reports")
        if reports_response.status_code == 200:
            reports = reports_response.json()
            print(f"✅ Found {len(reports)} completed reports:")
            for task_id, info in reports.items():
                print(f"   - {task_id}: {info['topic']} ({info['status']})")
        else:
            print(f"❌ Failed to get reports: {reports_response.status_code}")
    except Exception as e:
        print(f"❌ Error getting reports: {e}")

if __name__ == "__main__":
    test_api()