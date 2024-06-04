@echo off
echo ==================================================
echo [Remove container]
echo ==================================================
FOR /F "usebackq delims== tokens=1,2" %%a IN ("%~dp0..\config.ini") DO SET %%a=%%b
echo   PATH             : %~dp0
echo   Docker image     : %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VER%
echo   Docker container : %DOCKER_CONTAINER_NAME%
echo ==================================================

docker ps -a --format "{{.Names}}" --filter "name=%DOCKER_CONTAINER_NAME%" | findstr /r /c:"%DOCKER_CONTAINER_NAME%" > nul

if %ERRORLEVEL% EQU 0 (
    docker stop %DOCKER_CONTAINER_NAME% > nul
    docker rm %DOCKER_CONTAINER_NAME% > nul
    echo [INFO] Remove existing container : %DOCKER_CONTAINER_NAME%
    echo //////////////////////////////////////////////////
) else (
    echo [INFO] No container found
    echo //////////////////////////////////////////////////
)

docker ps -a --format "table {{.Names}}\t{{.Status}}"
echo //////////////////////////////////////////////////
