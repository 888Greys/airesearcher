"""
Slack Bot for CrewAI Tech Research System
Provides instant access to AI research via Slack
"""

import os
import asyncio
import logging
from datetime import datetime
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
import requests
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechResearchSlackBot:
    def __init__(self, bot_token: str, app_token: str, api_base_url: str):
        self.api_base_url = api_base_url.rstrip('/')
        self.app = AsyncApp(token=bot_token)
        self.app_token = app_token
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup Slack event handlers"""
        
        @self.app.message("hello")
        async def message_hello(message, say):
            await say(f"Hey there <@{message['user']}>! ��")
        
        @self.app.command("/research")
        async def research_command(ack, respond, command):
            await ack()
            
            topic = command['text'].strip()
            if not topic:
                await respond({
                    "text": "🔍 **Please specify a research topic!**",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "🔍 *Please specify a research topic!*\n\nExample: `/research Latest AI frameworks 2025`"
                            }
                        }
                    ]
                })
                return
            
            await self.start_research(respond, topic, command['user_id'])
        
        @self.app.command("/status")
        async def status_command(ack, respond, command):
            await ack()
            await self.get_status(respond)
        
        @self.app.command("/reports")
        async def reports_command(ack, respond, command):
            await ack()
            await self.list_reports(respond)
        
        @self.app.event("app_mention")
        async def handle_app_mention(event, say):
            text = event['text'].lower()
            user = event['user']
            
            if 'research' in text:
                # Extract topic after mention
                mention_text = text.split('>', 1)[-1].strip()
                if 'research' in mention_text:
                    topic = mention_text.replace('research', '').strip()
                    if topic:
                        await self.start_research_mention(say, topic, user, event['channel'])
                    else:
                        await say(f"<@{user}> What would you like me to research? 🔍")
                else:
                    await say(f"<@{user}> What would you like me to research? 🔍")
            else:
                await say(f"Hello <@{user}> 👋 I can help you with tech research! Try `/research <topic>`")
    
    async def start_research(self, respond, topic: str, user_id: str):
        """Start research process via slash command"""
        # Send initial response
        await respond({
            "text": f"🔍 Starting research on: {topic}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"🔍 *Starting research on:* {topic}\n\n⏳ Initializing AI research crew..."
                    }
                }
            ]
        })
        
        try:
            # Start research via API
            response = requests.post(
                f"{self.api_base_url}/start_research",
                json={"topic": topic},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                task_id = data['task_id']
                
                # Update with task ID
                await respond({
                    "text": f"Research started: {topic}",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"🔍 *Research Started:* {topic}\n\n📋 *Task ID:* `{task_id}`\n🤖 AI agents are working...\n\n⏳ This may take 1-3 minutes"
                            }
                        }
                    ]
                })
                
                # Monitor progress in background
                asyncio.create_task(self.monitor_research_background(task_id, topic, user_id))
                
            else:
                await respond({
                    "text": "Error starting research",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"❌ *Error starting research*\n\nStatus: {response.status_code}\nPlease try again later."
                            }
                        }
                    ]
                })
        
        except Exception as e:
            await respond({
                "text": "Error starting research",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"❌ *Error:* {str(e)}\n\nPlease check if the research system is online."
                        }
                    }
                ]
            })
    
    async def start_research_mention(self, say, topic: str, user_id: str, channel: str):
        """Start research process via mention"""
        await say({
            "text": f"🔍 Starting research on: {topic}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"🔍 *Starting research on:* {topic}\n\n⏳ Initializing AI research crew..."
                    }
                }
            ]
        })
        
        try:
            response = requests.post(
                f"{self.api_base_url}/start_research",
                json={"topic": topic},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                task_id = data['task_id']
                
                await say({
                    "text": f"Research started: {topic}",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"🔍 *Research Started:* {topic}\n\n📋 *Task ID:* `{task_id}`\n🤖 AI agents are working...\n\n⏳ This may take 1-3 minutes"
                            }
                        }
                    ]
                })
                
                # Monitor progress
                asyncio.create_task(self.monitor_research_background_mention(task_id, topic, user_id, channel))
        
        except Exception as e:
            await say(f"❌ Error starting research: {str(e)}")
    
    async def monitor_research_background(self, task_id: str, topic: str, user_id: str):
        """Monitor research progress in background"""
        max_attempts = 60  # 5 minutes max
        attempt = 0
        
        while attempt < max_attempts:
            try:
                response = requests.get(f"{self.api_base_url}/task_status/{task_id}")
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get('status')
                    
                    if status == 'completed':
                        await self.send_research_results_dm(task_id, topic, user_id)
                        return
                    
                    elif status == 'failed':
                        error = data.get('error', 'Unknown error')
                        await self.app.client.chat_postMessage(
                            channel=user_id,
                            text=f"❌ Research failed: {topic}\n\nError: {error}"
                        )
                        return
                
                await asyncio.sleep(5)
                attempt += 1
                
            except Exception as e:
                logger.error(f"Error monitoring research: {e}")
                await asyncio.sleep(5)
                attempt += 1
        
        # Timeout
        await self.app.client.chat_postMessage(
            channel=user_id,
            text=f"⏰ Research timeout: {topic}\n\nTask ID: {task_id}\n\nCheck `/reports` later for results."
        )
    
    async def send_research_results_dm(self, task_id: str, topic: str, user_id: str):
        """Send research results via DM"""
        try:
            response = requests.get(f"{self.api_base_url}/api/report/{task_id}")
            
            if response.status_code == 200:
                data = response.json()
                content = data.get('content', '')
                
                # Send completion message
                await self.app.client.chat_postMessage(
                    channel=user_id,
                    blocks=[
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"✅ *Research Completed:* {topic}\n\n📋 *Task ID:* `{task_id}`"
                            }
                        },
                        {
                            "type": "actions",
                            "elements": [
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "📥 Download Report"
                                    },
                                    "url": f"{self.api_base_url}/download_report/{task_id}"
                                }
                            ]
                        }
                    ]
                )
                
                # Send report content (truncated if too long)
                if len(content) > 3000:
                    content = content[:3000] + "\n\n... (truncated, download full report)"
                
                await self.app.client.chat_postMessage(
                    channel=user_id,
                    text=f"📄 *Report: {topic}*\n\n{content}"
                )
            
            else:
                await self.app.client.chat_postMessage(
                    channel=user_id,
                    text=f"✅ Research completed: {topic}\n\n❌ Error retrieving report content.\nUse `/reports` to access your report."
                )
        
        except Exception as e:
            logger.error(f"Error sending results: {e}")
            await self.app.client.chat_postMessage(
                channel=user_id,
                text=f"✅ Research completed: {topic}\n\n❌ Error sending report. Use `/reports` to access."
            )
    
    async def get_status(self, respond):
        """Get system status"""
        try:
            response = requests.get(f"{self.api_base_url}/api/llm_status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                total_configs = data.get('total_configs', 0)
                configs = data.get('configs', [])
                
                status_blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"📊 *System Status*\n\n🤖 *LLM Providers:* {total_configs}"
                        }
                    }
                ]
                
                for config in configs:
                    name = config.get('name', 'Unknown')
                    provider = config.get('provider', 'unknown')
                    is_limited = config.get('is_rate_limited', False)
                    utilization = config.get('utilization', '0%')
                    
                    status_emoji = "🔴" if is_limited else "🟢"
                    
                    status_blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{status_emoji} *{name}* ({provider})\nUsage: {utilization}"
                        }
                    })
                
                status_blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "✅ System is operational!"
                    }
                })
                
                await respond({
                    "text": "System Status",
                    "blocks": status_blocks
                })
                
            else:
                await respond({
                    "text": "❌ System Status: Offline\n\nCannot connect to research system."
                })
        
        except Exception as e:
            await respond({
                "text": f"❌ System Status: Error\n\n{str(e)}"
            })
    
    async def list_reports(self, respond):
        """List recent reports"""
        try:
            response = requests.get(f"{self.api_base_url}/api/reports", timeout=10)
            
            if response.status_code == 200:
                reports = response.json()
                
                if not reports:
                    await respond({
                        "text": "📋 No reports found\n\nStart your first research with `/research <topic>`"
                    })
                    return
                
                report_blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "📋 *Recent Research Reports*"
                        }
                    }
                ]
                
                for task_id, report in list(reports.items())[:10]:
                    topic = report.get('topic', 'Unknown')
                    status = report.get('status', 'unknown')
                    start_time = report.get('start_time', '')
                    
                    try:
                        dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                        time_str = dt.strftime('%m/%d %H:%M')
                    except:
                        time_str = 'Unknown'
                    
                    status_emoji = "✅" if status == "completed" else "❌"
                    
                    report_blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{status_emoji} *{topic}*\n📅 {time_str} | ID: `{task_id}`"
                        }
                    })
                
                await respond({
                    "text": "Recent Reports",
                    "blocks": report_blocks
                })
            
            else:
                await respond({
                    "text": "❌ Error retrieving reports\n\nPlease try again later."
                })
        
        except Exception as e:
            await respond({
                "text": f"❌ Error: {str(e)}\n\nCannot connect to research system."
            })
    
    async def start(self):
        """Start the Slack bot"""
        handler = AsyncSocketModeHandler(self.app, self.app_token)
        await handler.start_async()

def main():
    """Main function"""
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    app_token = os.getenv('SLACK_APP_TOKEN')
    api_url = os.getenv('API_BASE_URL', 'http://localhost:5000')
    
    if not bot_token or not app_token:
        print("❌ SLACK_BOT_TOKEN or SLACK_APP_TOKEN not found in environment variables")
        print("Please add your Slack tokens to .env file")
        return
    
    bot = TechResearchSlackBot(bot_token, app_token, api_url)
    
    async def run_bot():
        await bot.start()
    
    asyncio.run(run_bot())

if __name__ == '__main__':
    main()