# 🚀 Deploy to Render (Free) - Step by Step

## Step 1: Create GitHub Repository (Required for Render)

```bash
git init
git add .
git commit -m "Initial commit - CrewAI Research System"
git remote add origin https://github.com/yourusername/crewai-research.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy on Render

1. **Go to [render.com](https://render.com)**
2. **Sign up with GitHub**
3. **Click "New" → "Web Service"**
4. **Connect your repository**
5. **Configure:**
   - **Name**: `crewai-research`
   - **Environment**: `Docker`
   - **Plan**: `Free`
   - **Dockerfile Path**: `./Dockerfile`

## Step 3: Set Environment Variables

In Render dashboard, go to Environment tab and add your actual API keys:

```
GROQ_API_KEY=your_actual_groq_key
GEMINI_API_KEY=your_actual_gemini_key
KIMI_API_KEY=your_actual_kimi_key
SERP_API_KEY=your_actual_serp_key
PORT=5000
PYTHONPATH=/app/src
```

## Step 4: Deploy

Click "Create Web Service" and Render will build and deploy your app.