#!/usr/bin/env python3
"""
CrewAI Research System API Client Example

This script demonstrates how to interact with your hosted CrewAI research system
programmatically to start research tasks and retrieve results.
"""

import requests
import time
import json
from typing import Dict, Any, Optional

class CrewAIClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialize the CrewAI API client.
        
        Args:
            base_url: The base URL of your hosted CrewAI system
        """
        self.base_url = base_url.rstrip('/')
    
    def start_research(self, topic: str) -> Dict[str, Any]:
        """
        Start a new research task.
        
        Args:
            topic: The research topic
            
        Returns:
            Dictionary containing task_id and status
        """
        url = f"{self.base_url}/start_research"
        payload = {"topic": topic}
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a research task.
        
        Args:
            task_id: The task ID returned from start_research
            
        Returns:
            Dictionary containing task status and progress
        """
        url = f"{self.base_url}/task_status/{task_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def wait_for_completion(self, task_id: str, timeout: int = 300, poll_interval: int = 5) -> Dict[str, Any]:
        """
        Wait for a research task to complete.
        
        Args:
            task_id: The task ID
            timeout: Maximum time to wait in seconds
            poll_interval: How often to check status in seconds
            
        Returns:
            Final task status
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_task_status(task_id)
            
            print(f"Status: {status['status']} - {status.get('progress', 'Processing...')}")
            
            if status['status'] in ['completed', 'failed']:
                return status
            
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Task {task_id} did not complete within {timeout} seconds")
    
    def get_report_content(self, task_id: str) -> Dict[str, Any]:
        """
        Get the content of a completed research report.
        
        Args:
            task_id: The task ID
            
        Returns:
            Dictionary containing report content and metadata
        """
        url = f"{self.base_url}/api/report/{task_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def list_reports(self) -> Dict[str, Any]:
        """
        List all completed research reports.
        
        Returns:
            Dictionary of completed reports
        """
        url = f"{self.base_url}/api/reports"
        
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def download_report(self, task_id: str, filename: Optional[str] = None) -> str:
        """
        Download a research report as a markdown file.
        
        Args:
            task_id: The task ID
            filename: Optional filename to save as
            
        Returns:
            Path to the downloaded file
        """
        url = f"{self.base_url}/download_report/{task_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        
        if not filename:
            filename = f"research_report_{task_id}.md"
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        return filename

def main():
    """Example usage of the CrewAI API client."""
    
    # Initialize client (change URL if hosted elsewhere)
    client = CrewAIClient("http://localhost:5000")
    
    print("🤖 CrewAI Research System API Client")
    print("=" * 50)
    
    # Example 1: Start a research task
    print("\n1. Starting research on 'Quantum Computing 2025'...")
    
    try:
        result = client.start_research("Quantum Computing 2025")
        task_id = result['task_id']
        print(f"✅ Research started! Task ID: {task_id}")
        
        # Example 2: Wait for completion
        print("\n2. Waiting for research to complete...")
        final_status = client.wait_for_completion(task_id)
        
        if final_status['status'] == 'completed':
            print("✅ Research completed successfully!")
            
            # Example 3: Get report content
            print("\n3. Retrieving report content...")
            report = client.get_report_content(task_id)
            
            print(f"📊 Report Topic: {report['topic']}")
            print(f"📅 Completed: {report['end_time']}")
            print(f"📝 Content Preview: {report['content'][:200]}...")
            
            # Example 4: Download report
            print("\n4. Downloading report...")
            filename = client.download_report(task_id)
            print(f"💾 Report saved as: {filename}")
            
        else:
            print(f"❌ Research failed: {final_status.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 5: List all reports
    print("\n5. Listing all completed reports...")
    try:
        reports = client.list_reports()
        print(f"📚 Found {len(reports)} completed reports:")
        
        for task_id, report_info in reports.items():
            print(f"  - {task_id}: {report_info['topic']} ({report_info['status']})")
    
    except Exception as e:
        print(f"❌ Error listing reports: {e}")

if __name__ == "__main__":
    main()