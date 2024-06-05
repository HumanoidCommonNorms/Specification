@echo off
echo ==================================================
echo [Remove network]
echo ==================================================
FOR /F "usebackq delims== tokens=1,2" %%a IN ("%~dp0..\config.ini") DO SET %%a=%%b
echo   Docker netowr:
echo       name   : %DOCKER_NETWORK_NAME%
echo       subnet : %DOCKER_NETWORK_SUBNET%
echo ==================================================

docker network ls --format "{{.Name}}" --filter "name=%DOCKER_NETWORK_NAME%" | findstr /r /c:"%DOCKER_NETWORK_NAME%" > nul

if %ERRORLEVEL% EQU 0 (
    docker network rm %DOCKER_NETWORK_NAME% > nul
    echo [INFO] Remove existing network : %DOCKER_NETWORK_NAME%
)

echo //////////////////////////////////////////////////
docker network ls
echo --------------------------------------------------
