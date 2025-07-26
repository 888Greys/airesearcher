#!/usr/bin/env python3
"""
Local runner for CrewAI web interface with proper imports
"""

import os
import sys
import subprocess

def main():
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Install the project in development mode if not already done
    try:
        import firstcrew
    except ImportError:
        print("Installing project in development mode...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
    
    # Now run the web app
    from web_app import app
    
    print("🚀 Starting CrewAI Research System Web Interface...")
    print("📱 Access the interface at:")
    print("   - Local: http://127.0.0.1:5000")
    print("   - Network: http://192.168.88.214:5000")
    print("🛑 Press Ctrl+C to stop")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()