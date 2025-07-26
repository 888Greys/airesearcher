# 🚀 Free Hosting & Bot Deployment Guide

## 🌐 **Free Hosting Options**

### **🥇 Option 1: Railway (Recommended)**

**Why Railway?**
- ✅ $5 free credit monthly (enough for your app)
- ✅ Automatic deployments from GitHub
- ✅ Built-in environment variables
- ✅ Custom domains
- ✅ Easy scaling

**Steps:**
1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/crewai-research.git
   git push -u origin main
   ```

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect the `railway.json` config

3. **Set Environment Variables:**
   ```
   GROQ_API_KEY=your_groq_key
   GEMINI_API_KEY=your_gemini_key
   KIMI_API_KEY=your_kimi_key
   SERP_API_KEY=your_serp_key
   ```

4. **Get Your URL:**
   - Railway provides: `https://your-app-name.railway.app`

---

### **🥈 Option 2: Render**

**Steps:**
1. **Push to GitHub** (same as above)

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New" → "Web Service"
   - Connect your repository
   - Render will use the `render.yaml` config

3. **Set Environment Variables:**
   - Go to Environment tab
   - Add your API keys

---

### **🥉 Option 3: Fly.io**

**Steps:**
1. **Install Fly CLI:**
   ```bash
   # Windows
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Mac/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Deploy:**
   ```bash
   fly auth login
   fly launch --copy-config --name crewai-research
   fly secrets set GROQ_API_KEY=your_key GEMINI_API_KEY=your_key
   fly deploy
   ```

---

## 🤖 **Bot Setup**

### **📱 Telegram Bot**

**1. Create Bot:**
- Message [@BotFather](https://t.me/botfather) on Telegram
- Send `/newbot`
- Choose a name: "Tech Research AI"
- Choose username: "your_research_bot"
- Save the token

**2. Add to Environment:**
```bash
TELEGRAM_BOT_TOKEN=your_telegram_token
API_BASE_URL=https://your-app.railway.app
```

**3. Run Bot:**
```bash
# Local testing
python bots/telegram_bot.py

# Or deploy as separate service
```

**4. Bot Commands:**
- `/start` - Welcome message
- `/research <topic>` - Start research
- `/status` - System status
- `/reports` - Recent reports
- `/help` - Show help

---

### **💬 Slack Bot**

**1. Create Slack App:**
- Go to [api.slack.com/apps](https://api.slack.com/apps)
- Click "Create New App" → "From scratch"
- Name: "Tech Research AI"
- Choose your workspace

**2. Configure Bot:**
- Go to "OAuth & Permissions"
- Add Bot Token Scopes:
  - `app_mentions:read`
  - `chat:write`
  - `commands`
  - `im:write`
- Install to workspace

**3. Add Slash Commands:**
- Go to "Slash Commands"
- Create commands:
  - `/research` - Start research
  - `/status` - System status
  - `/reports` - List reports

**4. Enable Socket Mode:**
- Go to "Socket Mode" → Enable
- Generate App-Level Token
- Add scope: `connections:write`

**5. Add to Environment:**
```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
API_BASE_URL=https://your-app.railway.app
```

---

## 📱 **Frontend Access Methods**

### **1. 📱 Telegram Bot**
```
🤖 Tech Research AI Bot
Commands:
- /research Latest AI frameworks 2025
- /status
- /reports

Features:
✅ Instant notifications
✅ Real-time progress
✅ Report downloads
✅ Mobile-friendly
```

### **2. 💬 Slack Bot**
```
🤖 Tech Research AI App
Commands:
- /research Latest Python tools
- @TechResearchAI research DevOps trends
- /status

Features:
✅ Team collaboration
✅ Channel integration
✅ DM notifications
✅ File sharing
```

### **3. 🌐 Web Interface**
```
🌐 https://your-app.railway.app
Features:
✅ Full dashboard
✅ Visual progress
✅ Report management
✅ LLM status monitoring
```

### **4. 🔗 API Access**
```bash
# Start research
curl -X POST https://your-app.railway.app/start_research \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI trends 2025"}'

# Get status
curl https://your-app.railway.app/api/llm_status
```

### **5. 📧 Email Reports (Future)**
- Scheduled daily/weekly digests
- Breaking news alerts
- Custom topic monitoring

---

## 🔧 **Environment Variables Setup**

**Complete .env for hosting:**
```bash
# LLM APIs
GROQ_API_KEY=gsk_your_groq_key
GEMINI_API_KEY=AIzaSy_your_gemini_key
KIMI_API_KEY=sk-your_kimi_key

# Search API
SERP_API_KEY=your_serp_key

# Bot Tokens
TELEGRAM_BOT_TOKEN=your_telegram_token
SLACK_BOT_TOKEN=xoxb-your_slack_token
SLACK_APP_TOKEN=xapp-your_slack_app_token

# Hosting
API_BASE_URL=https://your-app.railway.app
PORT=5000
FLASK_ENV=production
```

---

## 🚀 **Quick Deploy Commands**

### **Railway:**
```bash
# One-time setup
git init && git add . && git commit -m "Deploy"
git remote add origin https://github.com/yourusername/repo.git
git push -u origin main

# Then deploy on Railway dashboard
```

### **Render:**
```bash
# Push to GitHub, then connect on Render dashboard
```

### **Fly.io:**
```bash
fly launch --copy-config
fly secrets set GROQ_API_KEY=your_key
fly deploy
```

---

## 📊 **Recommended Setup**

**For Maximum Availability:**

1. **Main App**: Railway (web interface + API)
2. **Telegram Bot**: Railway (same instance)
3. **Slack Bot**: Render (separate instance)
4. **Backup**: Fly.io (if needed)

**Cost:** $0/month (within free tiers)

**Access Methods:**
- 📱 Telegram: Instant mobile access
- 💬 Slack: Team collaboration
- 🌐 Web: Full dashboard
- 🔗 API: Custom integrations

---

## 🎯 **Next Steps**

1. **Choose hosting platform** (Railway recommended)
2. **Deploy main app**
3. **Set up Telegram bot**
4. **Configure Slack bot** (optional)
5. **Test all access methods**

**Your tech research system will be accessible 24/7 from anywhere! 🌍**