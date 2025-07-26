#!/bin/bash

echo "Starting CrewAI Research System Web Interface..."
echo

# Check if Docker is running
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Please install Docker and make sure it's running"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker is not running"
    echo "Please start Docker and try again"
    exit 1
fi

echo "🐳 Building Docker image..."
docker-compose -f docker-compose.web.yml build

if [ $? -ne 0 ]; then
    echo "❌ Failed to build Docker image"
    exit 1
fi

echo "🚀 Starting web interface..."
echo "📱 Access the interface at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop"
echo

docker-compose -f docker-compose.web.yml up