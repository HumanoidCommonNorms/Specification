#!/bin/bash
echo ==================================================
echo "[Remove container]"
echo ==================================================
INI_FILE=$(readlink -f $(dirname $0)/../config.ini)
source <(sed -n -E 's/^\s*(\S+)\s*=\s*(.+)$/\1=\2/p' <"${INI_FILE}")
echo "  PATH             : ${INI_FILE}"
echo "  Docker image     : ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VER}"
echo "  Docker container : ${DOCKER_CONTAINER_NAME}"
echo ==================================================

FILTER_LIST=($(docker ps -a --format "{{.Names}}" --filter "name=${DOCKER_CONTAINER_NAME}"))
for LINE in ${FILTER_LIST}; do
    if [ "${LINE}" == "${DOCKER_CONTAINER_NAME}" ]; then
        docker stop ${DOCKER_CONTAINER_NAME} > /dev/null
        docker rm ${DOCKER_CONTAINER_NAME} > /dev/null
        echo [INFO] Remove existing container : ${DOCKER_CONTAINER_NAME}
        echo //////////////////////////////////////////////////
    fi
done

docker ps -a --format "table {{.Names}}\t{{.Status}}"
echo //////////////////////////////////////////////////
