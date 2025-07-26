# Docker Setup for FirstCrew

This document explains how to run your CrewAI project using Docker, which eliminates installation issues and provides a consistent environment.

## Prerequisites

- Docker Desktop installed on your system
- Docker Compose (usually included with Docker Desktop)

## Quick Start

### 1. Build and Run the Application

```bash
# Navigate to the project directory
cd firstcrew

# Build and run the crew
docker-compose up --build
```

### 2. Alternative Commands

#### Run in detached mode (background)
```bash
docker-compose up -d --build
```

#### Run specific operations

**Training:**
```bash
docker-compose --profile training up crewai-train --build
```

**Testing:**
```bash
docker-compose --profile testing up crewai-test --build
```

#### Interactive mode (for debugging)
```bash
# Uncomment stdin_open and tty in docker-compose.yml first
docker-compose run --rm crewai-app bash
```

### 3. Direct Docker Commands (Alternative)

#### Build the image
```bash
docker build -t firstcrew .
```

#### Run the container
```bash
docker run --rm -v "$(pwd)/output:/app/output" firstcrew
```

#### Run with environment file
```bash
docker run --rm --env-file .env -v "$(pwd)/output:/app/output" firstcrew
```

## Project Structure

```
firstcrew/
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Multi-container setup
├── .dockerignore           # Files to exclude from Docker build
├── output/                 # Persistent output directory
├── src/                    # Source code
├── config/                 # Configuration files
├── knowledge/              # Knowledge base
└── .env                    # Environment variables
```

## Key Features

1. **Isolated Environment**: No need to install Python dependencies locally
2. **Consistent Runtime**: Same environment across different machines
3. **Persistent Output**: Reports and outputs are saved to the `output/` directory
4. **Easy Scaling**: Can easily add more services or workers
5. **Development Mode**: Source code is mounted for live development

## Customization

### Environment Variables

Add your API keys and configuration to the `.env` file:

```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
# Add other environment variables as needed
```

### Modify Resources

Edit the `docker-compose.yml` file to adjust memory limits:

```yaml
deploy:
  resources:
    limits:
      memory: 4G  # Increase if needed
    reservations:
      memory: 2G
```

### Add New Services

You can add additional services to `docker-compose.yml` for different crew configurations or tools.

## Troubleshooting

### Common Issues

1. **Permission Issues**: Make sure Docker has access to your project directory
2. **Memory Issues**: Increase Docker's memory allocation in Docker Desktop settings
3. **Port Conflicts**: Change port mappings in docker-compose.yml if needed

### Viewing Logs

```bash
# View logs from all services
docker-compose logs

# View logs from specific service
docker-compose logs crewai-app

# Follow logs in real-time
docker-compose logs -f crewai-app
```

### Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove images and volumes
docker-compose down --rmi all --volumes
```

## Development Workflow

1. Make changes to your source code
2. The changes are automatically reflected in the container (due to volume mounting)
3. Restart the container if needed: `docker-compose restart crewai-app`

For major dependency changes, rebuild the image:
```bash
docker-compose up --build
```