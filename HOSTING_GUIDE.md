# 🌐 CrewAI Research System - Hosting & Access Guide

## 🚀 Quick Start

### Option 1: Local Web Interface (Recommended)

1. **Start the web interface:**
   ```bash
   # Windows
   start_web.bat
   
   # Linux/Mac
   chmod +x start_web.sh
   ./start_web.sh
   ```

2. **Access the interface:**
   - Open your browser and go to: `http://localhost:5000`
   - Enter a research topic and click "Start Research"
   - Monitor progress in real-time
   - Download completed reports

### Option 2: Manual Docker Setup

```bash
# Build and run the web interface
docker-compose -f docker-compose.web.yml up --build

# Access at http://localhost:5000
```

## 🌍 Hosting Options

### 1. **Local Hosting (Development)**
- **URL**: `http://localhost:5000`
- **Use case**: Personal use, development, testing
- **Setup**: Run the scripts above

### 2. **Cloud Hosting (Production)**

#### **Option A: Railway**
1. Fork your repository to GitHub
2. Connect to [Railway](https://railway.app)
3. Deploy from GitHub
4. Set environment variables (GROQ_API_KEY, SERP_API_KEY)

#### **Option B: Heroku**
1. Install Heroku CLI
2. Create Heroku app: `heroku create your-crewai-app`
3. Set environment variables:
   ```bash
   heroku config:set GROQ_API_KEY=your_key
   heroku config:set SERP_API_KEY=your_key
   ```
4. Deploy: `git push heroku main`

#### **Option C: DigitalOcean App Platform**
1. Connect your GitHub repository
2. Configure environment variables
3. Deploy with one click

#### **Option D: AWS/GCP/Azure**
- Use container services (ECS, Cloud Run, Container Instances)
- Deploy the Docker image
- Configure load balancer and domain

### 3. **VPS Hosting**
```bash
# On your VPS
git clone your-repo
cd firstcrew
docker-compose -f docker-compose.web.yml up -d

# Access via your VPS IP: http://your-vps-ip:5000
```

## 📊 Accessing Research Data

### 1. **Web Interface**
- **URL**: `http://your-host:5000`
- **Features**:
  - Start new research tasks
  - Monitor progress in real-time
  - Download reports as Markdown files
  - View research history

### 2. **REST API**

#### **Start Research**
```bash
curl -X POST http://your-host:5000/start_research \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI Trends 2025"}'
```

#### **Check Status**
```bash
curl http://your-host:5000/task_status/task_123456789
```

#### **Get Report Content**
```bash
curl http://your-host:5000/api/report/task_123456789
```

#### **List All Reports**
```bash
curl http://your-host:5000/api/reports
```

#### **Download Report**
```bash
curl -O http://your-host:5000/download_report/task_123456789
```

### 3. **Python API Client**

```python
from api_client_example import CrewAIClient

# Initialize client
client = CrewAIClient("http://your-host:5000")

# Start research
result = client.start_research("Blockchain Technology 2025")
task_id = result['task_id']

# Wait for completion
status = client.wait_for_completion(task_id)

# Get report
if status['status'] == 'completed':
    report = client.get_report_content(task_id)
    print(report['content'])
```

### 4. **JavaScript/Web Integration**

```javascript
// Start research
const response = await fetch('/start_research', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic: 'Machine Learning 2025' })
});

const { task_id } = await response.json();

// Check status
const statusResponse = await fetch(`/task_status/${task_id}`);
const status = await statusResponse.json();

// Get report when completed
if (status.status === 'completed') {
    const reportResponse = await fetch(`/api/report/${task_id}`);
    const report = await reportResponse.json();
    console.log(report.content);
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
GROQ_API_KEY=your_groq_api_key
SERP_API_KEY=your_serp_api_key

# Optional
FLASK_ENV=production
MODEL=groq/llama-3.1-8b-instant
```

### Custom Topics
You can research any topic by changing the input:
- "Artificial Intelligence 2025"
- "Climate Change Solutions"
- "Cryptocurrency Market Analysis"
- "Space Technology Developments"
- "Renewable Energy Trends"

## 📁 File Structure

```
firstcrew/
├── web_app.py              # Flask web application
├── templates/
│   └── index.html          # Web interface
├── api_client_example.py   # Python API client
├── docker-compose.web.yml  # Docker setup for web hosting
├── Dockerfile.web          # Web app Docker image
├── start_web.bat          # Windows startup script
├── start_web.sh           # Linux/Mac startup script
├── reports/               # Generated reports storage
└── output/                # Additional output files
```

## 🔒 Security Considerations

### For Production Hosting:
1. **Environment Variables**: Never commit API keys to version control
2. **HTTPS**: Use SSL certificates for production
3. **Authentication**: Add user authentication if needed
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Firewall**: Configure proper firewall rules

### Example Nginx Configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 Monitoring & Logs

### View Logs:
```bash
# Docker logs
docker-compose -f docker-compose.web.yml logs -f

# Application logs
docker exec -it firstcrew-web tail -f /app/logs/app.log
```

### Health Check:
```bash
curl http://your-host:5000/health
```

## 🎯 Use Cases

1. **Personal Research Assistant**: Research any topic with real-time data
2. **Business Intelligence**: Market research and competitor analysis
3. **Academic Research**: Literature reviews and trend analysis
4. **Content Creation**: Research for articles, blogs, and reports
5. **API Integration**: Embed research capabilities into other applications

## 🆘 Troubleshooting

### Common Issues:

1. **Port 5000 already in use**:
   ```bash
   # Change port in docker-compose.web.yml
   ports:
     - "8080:5000"  # Use port 8080 instead
   ```

2. **API key errors**:
   - Check `.env` file has correct keys
   - Verify keys are not expired

3. **Docker build fails**:
   ```bash
   # Clean Docker cache
   docker system prune -a
   docker-compose -f docker-compose.web.yml build --no-cache
   ```

4. **Research tasks fail**:
   - Check Groq API rate limits
   - Verify SERP API quota
   - Check internet connectivity

## 📞 Support

For issues or questions:
1. Check the logs for error messages
2. Verify all environment variables are set
3. Test API endpoints individually
4. Check Docker container status

Your CrewAI Research System is now ready to be hosted and accessed from anywhere! 🚀