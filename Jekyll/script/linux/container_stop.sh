#!/bin/bash
echo ==================================================
echo "[Stop container]"
echo ==================================================
INI_FILE=$(readlink -f $(dirname $0)/../config.ini)
source <(sed -n -E 's/^\s*(\S+)\s*=\s*(.+)$/\1=\2/p' <"${INI_FILE}")
echo "  PATH             : ${INI_FILE}"
echo "  Open port        : ${OPEN_PORT}"
echo "  Docker image     : ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VER}"
echo "  Docker container : ${DOCKER_CONTAINER_NAME}"
echo "      port         : ${SERVER_PORT}"
echo "      user name    : ${USER_NAME}"
echo ==================================================

docker ps --format "{{.Names}}" --filter "name=${DOCKER_CONTAINER_NAME}" | findstr /r /c:"${DOCKER_CONTAINER_NAME}" > /dev/null
ret=$?
if [ 0 -eq ${ret} ]; then
    docker stop ${DOCKER_CONTAINER_NAME} > /dev/null
    echo Stop existing container : ${DOCKER_CONTAINER_NAME}
    echo //////////////////////////////////////////////////
    docker ps -a --format "table {{.Names}}\t{{.Status}}"
    echo //////////////////////////////////////////////////
else
    echo The container is not running : ${DOCKER_CONTAINER_NAME}
fi

