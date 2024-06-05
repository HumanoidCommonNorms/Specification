@echo off
echo ==================================================
echo [Create container]
echo ==================================================
FOR /F "usebackq delims== tokens=1,2" %%a IN ("%~dp0..\config.ini") DO SET %%a=%%b
echo   PATH             : %~dp0
echo   Docker image     : %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VER%
echo   Docker container : %DOCKER_CONTAINER_NAME%
echo   Open port        : %OPEN_PORT%
echo ==================================================
SET DOCKER_MACHINE_NAME=default

SET NETWORT_OPTION=
if not "%DOCKER_NETWORK_NAME%" == "" (
    SET NETWORT_OPTION=--network %DOCKER_NETWORK_NAME%
)

docker ps -a --format "{{.Names}}" --filter "name=%DOCKER_CONTAINER_NAME%" | findstr /r /c:"%DOCKER_CONTAINER_NAME%" > nul

if %ERRORLEVEL% EQU 0 (
    docker stop %DOCKER_CONTAINER_NAME% > nul
    docker rm %DOCKER_CONTAINER_NAME% > nul
    echo [INFO] Remove existing container : %DOCKER_CONTAINER_NAME%
    echo //////////////////////////////////////////////////
)

docker ps -a --format "{{.Names}}" --filter "name=%DOCKER_MACHINE_NAME%" | findstr /r /c:"%DOCKER_MACHINE_NAME%" > nul

if %ERRORLEVEL% EQU 0 (
    docker stop %DOCKER_MACHINE_NAME% > nul
    docker rm %DOCKER_MACHINE_NAME% > nul
    echo [INFO] Remove existing container : %DOCKER_MACHINE_NAME%
    echo //////////////////////////////////////////////////
)

rem docker-machine create --driver virtualbox %DOCKER_MACHINE_NAME%
rem docker-machine start %DOCKER_MACHINE_NAME%
rem docker-machine ssh %DOCKER_CONTAINER_NAME% -f -N -L %OPEN_PORT%:localhost:%SERVER_PORT%

docker run ^
    -dit ^
    --name %DOCKER_CONTAINER_NAME% ^
    --hostname %DOCKER_CONTAINER_NAME% ^
    --publish %OPEN_PORT%:%SERVER_PORT% %NETWORT_OPTION% ^
    -v %~dp0..\..\..\%SOURCE_DIR%:/root/docs ^
    -v %~dp0..\..\..\%WEB_DIR%:/root/jekyll ^
    -v %~dp0..\..\..\__site:/root/_site ^
    --workdir /root/jekyll ^
    %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VER% ^
    /bin/bash > nul

docker exec -it %DOCKER_CONTAINER_NAME% /bin/bash -c "cd /root/jekyll;bundler install"

docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo --------------------------------------------------
echo [DOCKER LOGS]
docker logs %DOCKER_CONTAINER_NAME%
