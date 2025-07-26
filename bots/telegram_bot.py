"""
Telegram Bot for CrewAI Tech Research System
Provides instant access to AI research via Telegram
"""

import os
import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import requests
import json

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TechResearchBot:
    def __init__(self, token: str, api_base_url: str):
        self.token = token
        self.api_base_url = api_base_url.rstrip('/')
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup bot command handlers"""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("research", self.research))
        self.application.add_handler(CommandHandler("status", self.status))
        self.application.add_handler(CommandHandler("reports", self.list_reports))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        welcome_text = """
🤖 **Welcome to Tech Research AI!**

I'm your personal AI research assistant for software development and tech trends.

**Quick Commands:**
🔍 `/research <topic>` - Start AI research
📊 `/status` - Check system status  
📋 `/reports` - View recent reports
❓ `/help` - Show all commands

**Example:**
`/research Latest AI frameworks 2025`

Ready to keep you ahead of the tech curve! 🚀
        """
        
        keyboard = [
            [InlineKeyboardButton("🔍 Start Research", callback_data="quick_research")],
            [InlineKeyboardButton("📊 System Status", callback_data="status")],
            [InlineKeyboardButton("📋 Recent Reports", callback_data="reports")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def research(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Research command handler"""
        if not context.args:
            await update.message.reply_text(
                "🔍 **Please specify a research topic!**\n\n"
                "Example: `/research Latest AI frameworks 2025`",
                parse_mode='Markdown'
            )
            return
        
        topic = ' '.join(context.args)
        await self.start_research(update, topic)
    
    async def start_research(self, update: Update, topic: str):
        """Start research process"""
        status_message = await update.message.reply_text(
            f"🔍 **Starting research on:** {topic}\n\n"
            "⏳ Initializing AI research crew...",
            parse_mode='Markdown'
        )
        
        try:
            response = requests.post(
                f"{self.api_base_url}/start_research",
                json={"topic": topic},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                task_id = data['task_id']
                
                await status_message.edit_text(
                    f"🔍 **Research Started:** {topic}\n\n"
                    f"📋 **Task ID:** `{task_id}`\n"
                    "🤖 AI agents are working...\n\n"
                    "⏳ This may take 1-3 minutes",
                    parse_mode='Markdown'
                )
                
                await self.monitor_research(update, task_id, topic, status_message)
                
            else:
                await status_message.edit_text(
                    f"❌ **Error starting research**\n\n"
                    f"Status: {response.status_code}\n"
                    "Please try again later.",
                    parse_mode='Markdown'
                )
        
        except Exception as e:
            await status_message.edit_text(
                f"❌ **Error:** {str(e)}\n\n"
                "Please check if the research system is online.",
                parse_mode='Markdown'
            )
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram bot...")
        self.application.run_polling()

def main():
    """Main function"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    api_url = os.getenv('API_BASE_URL', 'http://localhost:5000')
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables")
        print("Please add your Telegram bot token to .env file")
        return
    
    bot = TechResearchBot(bot_token, api_url)
    bot.run()

if __name__ == '__main__':
    main()