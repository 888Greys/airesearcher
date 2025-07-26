#!/bin/bash
# Shell script to run CrewAI with Docker

echo "Starting CrewAI Docker Setup..."
echo

case "$1" in
    build)
        echo "Building Docker image..."
        docker-compose up --build
        ;;
    run)
        echo "Running CrewAI crew..."
        docker-compose up
        ;;
    train)
        echo "Running training..."
        docker-compose --profile training up crewai-train --build
        ;;
    test)
        echo "Running tests..."
        docker-compose --profile testing up crewai-test --build
        ;;
    shell)
        echo "Starting interactive shell..."
        docker-compose run --rm crewai-app bash
        ;;
    clean)
        echo "Cleaning up Docker containers and images..."
        docker-compose down --rmi all --volumes
        ;;
    logs)
        echo "Showing logs..."
        docker-compose logs -f
        ;;
    *)
        echo "Usage: $0 [command]"
        echo
        echo "Commands:"
        echo "  build  - Build and run the application"
        echo "  run    - Run the application"
        echo "  train  - Run training"
        echo "  test   - Run tests"
        echo "  shell  - Start interactive shell"
        echo "  logs   - Show logs"
        echo "  clean  - Clean up containers and images"
        echo
        echo "Running default build command..."
        docker-compose up --build
        ;;
esac

echo
echo "Done!"