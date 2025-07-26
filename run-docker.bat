@echo off
REM Windows batch script to run CrewAI with Docker

echo Starting CrewAI Docker Setup...
echo.

if "%1"=="build" (
    echo Building Docker image...
    docker-compose up --build
    goto :end
)

if "%1"=="run" (
    echo Running CrewAI crew...
    docker-compose up
    goto :end
)

if "%1"=="train" (
    echo Running training...
    docker-compose --profile training up crewai-train --build
    goto :end
)

if "%1"=="test" (
    echo Running tests...
    docker-compose --profile testing up crewai-test --build
    goto :end
)

if "%1"=="shell" (
    echo Starting interactive shell...
    docker-compose run --rm crewai-app bash
    goto :end
)

if "%1"=="clean" (
    echo Cleaning up Docker containers and images...
    docker-compose down --rmi all --volumes
    goto :end
)

if "%1"=="logs" (
    echo Showing logs...
    docker-compose logs -f
    goto :end
)

REM Default action
echo Usage: run-docker.bat [command]
echo.
echo Commands:
echo   build  - Build and run the application
echo   run    - Run the application
echo   train  - Run training
echo   test   - Run tests
echo   shell  - Start interactive shell
echo   logs   - Show logs
echo   clean  - Clean up containers and images
echo.
echo Running default build command...
docker-compose up --build

:end
echo.
echo Done!