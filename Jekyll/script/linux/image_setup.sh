#!/bin/bash
echo ==================================================
echo "[Setup docker image]"
echo ==================================================
CURRENT_DIR=$(dirname $0)
INI_FILE=$(readlink -f ${CURRENT_DIR}/../config.ini)
source <(sed -n -E 's/^\s*(\S+)\s*=\s*(.+)$/\1=\2/p' <"${INI_FILE}")
echo "  PATH             : ${INI_FILE}"
echo "  dockerfile       : ${DOCKER_FILE_NAME}"
echo "  Docker image     : ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VER}"
echo "  Docker container : ${DOCKER_CONTAINER_NAME}"
echo "      port         : ${SERVER_PORT}"
echo "      user name    : ${USER_NAME}"
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

FILTER_LIST=($(docker image ls -q ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VER}))
for LINE in ${FILTER_LIST}; do
    if [ "${LINE}" == "${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VER}" ]; then
    docker rmi ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VER} > /dev/null
    echo [INFO] Remove existing image : ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VER}
    echo //////////////////////////////////////////////////
    fi
done

docker build \
    --build-arg USER_NAME=${USER_NAME} \
    --build-arg GROUP_NAME=${GROUP_NAME} \
    --no-cache \
    -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VER} \
    -f $(readlink -f ${CURRENT_DIR}/../${DOCKER_FILE_NAME}) \
    ./

echo //////////////////////////////////////////////////
docker volume ls
echo --------------------------------------------------
docker network ls
echo --------------------------------------------------
docker images
echo //////////////////////////////////////////////////
