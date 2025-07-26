# 🚀 Render Deployment Configuration

## After pushing to GitHub, follow these steps:

### 1. Go to [render.com](https://render.com)
### 2. Sign up with GitHub
### 3. Click "New" → "Web Service"
### 4. Connect your GitHub repository: `airesearcher`

### 5. Configure Service:
```
Name: crewai-research-system
Environment: Docker
Plan: Free
Branch: main
Dockerfile Path: ./Dockerfile
```

### 6. Add Environment Variables:
```
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
KIMI_API_KEY=your_kimi_key_here
SERP_API_KEY=your_serp_key_here
PORT=5000
PYTHONPATH=/app/src
FLASK_ENV=production
```

### 7. Click "Create Web Service"

### 8. Your app will be available at:
`https://crewai-research-system.onrender.com`

## Free Tier Details:
- ✅ 750 hours/month
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ Takes ~30s to wake up

## After Deployment:
1. Test your web interface
2. Set up Telegram bot with your new URL
3. Set up Slack bot (optional)
4. Start researching! 🚀