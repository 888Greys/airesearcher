#!/usr/bin/env python3
"""
Bot Launcher for CrewAI Tech Research System
Starts Telegram and/or Slack bots
"""

import os
import sys
import asyncio
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def start_telegram_bot():
    """Start Telegram bot"""
    try:
        from bots.telegram_bot import main as telegram_main
        print("🤖 Starting Telegram bot...")
        telegram_main()
    except ImportError:
        print("❌ python-telegram-bot not installed. Install with: pip install python-telegram-bot")
    except Exception as e:
        print(f"❌ Error starting Telegram bot: {e}")

def start_slack_bot():
    """Start Slack bot"""
    try:
        from bots.slack_bot import main as slack_main
        print("💬 Starting Slack bot...")
        slack_main()
    except ImportError:
        print("❌ slack-bolt not installed. Install with: pip install slack-bolt")
    except Exception as e:
        print(f"❌ Error starting Slack bot: {e}")

def main():
    """Main launcher"""
    print("🚀 CrewAI Bot Launcher")
    print("=" * 40)
    
    # Check for bot tokens
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    slack_bot_token = os.getenv('SLACK_BOT_TOKEN')
    slack_app_token = os.getenv('SLACK_APP_TOKEN')
    api_url = os.getenv('API_BASE_URL', 'http://localhost:5000')
    
    print(f"🌐 API URL: {api_url}")
    print(f"📱 Telegram: {'✅' if telegram_token else '❌'}")
    print(f"💬 Slack: {'✅' if slack_bot_token and slack_app_token else '❌'}")
    print()
    
    if not telegram_token and not (slack_bot_token and slack_app_token):
        print("❌ No bot tokens found!")
        print("Please add bot tokens to your .env file:")
        print("  TELEGRAM_BOT_TOKEN=your_telegram_token")
        print("  SLACK_BOT_TOKEN=your_slack_token")
        print("  SLACK_APP_TOKEN=your_slack_app_token")
        return
    
    # Start available bots
    if len(sys.argv) > 1:
        bot_type = sys.argv[1].lower()
        
        if bot_type == 'telegram' and telegram_token:
            start_telegram_bot()
        elif bot_type == 'slack' and slack_bot_token and slack_app_token:
            start_slack_bot()
        else:
            print(f"❌ Invalid bot type or missing tokens: {bot_type}")
    
    else:
        # Start all available bots
        threads = []
        
        if telegram_token:
            telegram_thread = threading.Thread(target=start_telegram_bot)
            telegram_thread.daemon = True
            threads.append(telegram_thread)
        
        if slack_bot_token and slack_app_token:
            slack_thread = threading.Thread(target=start_slack_bot)
            slack_thread.daemon = True
            threads.append(slack_thread)
        
        if not threads:
            print("❌ No bots to start!")
            return
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        print(f"🚀 Started {len(threads)} bot(s)")
        print("Press Ctrl+C to stop all bots")
        
        try:
            # Keep main thread alive
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            print("\n🛑 Stopping all bots...")

if __name__ == '__main__':
    main()