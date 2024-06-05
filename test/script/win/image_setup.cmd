@echo off
echo ==================================================
echo [Setup docker image]
echo ==================================================
FOR /F "usebackq delims== tokens=1,2" %%a IN ("%~dp0..\config.ini") DO SET %%a=%%b
echo   PATH             : %~dp0
echo   dockerfile       : %DOCKER_FILE_NAME%
echo   Docker image     : %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VER%
echo   Docker container : %DOCKER_CONTAINER_NAME%
echo       port         : %SERVER_PORT%
echo ==================================================

docker ps -a --format "{{.Names}}" --filter "name=%DOCKER_CONTAINER_NAME%" | findstr /r /c:"%DOCKER_CONTAINER_NAME%" > nul

if %ERRORLEVEL% EQU 0 (
    docker stop %DOCKER_CONTAINER_NAME% > nul
    docker rm %DOCKER_CONTAINER_NAME% > nul
    echo [INFO] Remove existing container : %DOCKER_CONTAINER_NAME%
    echo //////////////////////////////////////////////////
)

for /f "usebackq" %%B IN (`docker image ls -q %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VER%`) do set IMAGE_ID=%%B
if not "%IMAGE_ID%" == "" (
    docker rmi %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VER% > nul
    echo [INFO] Remove existing image : %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VER%
    echo //////////////////////////////////////////////////
)

docker build ^
    --build-arg SERVER_PORT=%SERVER_PORT% ^
    --no-cache ^
    -t %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VER% ^
    -f %~dp0..\%DOCKER_FILE_NAME% ^
    ./

echo //////////////////////////////////////////////////
docker volume ls
echo --------------------------------------------------
docker network ls
echo --------------------------------------------------
docker images
echo //////////////////////////////////////////////////
