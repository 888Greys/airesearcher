@echo off
echo Starting CrewAI Research System Web Interface...
echo.

REM Check if Docker is running
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed or not running
    echo Please install Docker Desktop and make sure it's running
    pause
    exit /b 1
)

echo 🐳 Building Docker image...
docker-compose -f docker-compose.web.yml build

if errorlevel 1 (
    echo ❌ Failed to build Docker image
    pause
    exit /b 1
)

echo 🚀 Starting web interface...
docker-compose -f docker-compose.web.yml up

echo.
echo Web interface stopped.
pause