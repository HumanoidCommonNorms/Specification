@echo off
echo ==================================================
echo Build
echo ==================================================
FOR /F "usebackq delims== tokens=1,2" %%a IN ("%~dp0..\config.ini") DO SET %%a=%%b
echo   PATH             : %~dp0
echo   Open port        : %OPEN_PORT%
echo   Docker image     : %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VER%
echo   Docker container : %DOCKER_CONTAINER_NAME%
echo       port         : %SERVER_PORT%
echo       user name    : %USER_NAME%
echo ==================================================

docker ps -a --format "{{.Names}}" --filter "name=%DOCKER_CONTAINER_NAME%" | findstr /r /c:"%DOCKER_CONTAINER_NAME%" > nul

if %ERRORLEVEL% EQU 0 (
    rem # //SOURCE_DIR
    docker cp %~dp0..\..\..\%SOURCE_DIR% %DOCKER_CONTAINER_NAME%:/home/%USER_NAME%/workspace
) else (
    echo [ERROR] No container found
)
