#!/bin/bash
echo ==================================================
echo "[Create container]"
echo ==================================================
CURRENT_DIR=$(dirname $0)
INI_FILE=$(readlink -f ${CURRENT_DIR}/../config.ini)
source <(sed -n -E 's/^\s*(\S+)\s*=\s*(.+)$/\1=\2/p' <"${INI_FILE}")
echo "  PATH             : ${INI_FILE}"
echo "  Docker image     : ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VER}"
echo "  Docker container : ${DOCKER_CONTAINER_NAME}"
echo "      user name    : ${USER_NAME}"
echo "  Open port        : ${OPEN_PORT}"
echo ==================================================
NETWORT_OPTION=""
if [ "${DOCKER_NETWORK_NAME}" != "" ]; then
    NETWORT_OPTION="--network ${DOCKER_NETWORK_NAME}"
fi

FILTER_LIST=($(docker ps -a --format "{{.Names}}" --filter "name=${DOCKER_CONTAINER_NAME}"))
for LINE in ${FILTER_LIST}; do
    if [ "${LINE}" == "${DOCKER_CONTAINER_NAME}" ]; then
        docker stop ${DOCKER_CONTAINER_NAME} > /dev/null
        docker rm ${DOCKER_CONTAINER_NAME} > /dev/null
        echo [INFO] Remove existing container : ${DOCKER_CONTAINER_NAME}
        echo //////////////////////////////////////////////////
    fi
done

docker run \
    -dit \
    --name ${DOCKER_CONTAINER_NAME} \
    --hostname ${DOCKER_CONTAINER_NAME} \
    --publish ${OPEN_PORT}:${SERVER_PORT} ${NETWORT_OPTION} \
    --user ${USER_NAME} \
    -v $(readlink -f ${CURRENT_DIR}/../../${SOURCE_DIR}):/home/${USER_NAME}/jekyll \
    -v $(readlink -f ${CURRENT_DIR}/../../${WEB_DIR}):/home/${USER_NAME}/jekyll \
    --workdir /home/${USER_NAME}/jekyll \
    ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VER} \
    /bin/bash > /dev/null

docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo --------------------------------------------------
echo "[DOCKER LOGS]"
docker logs ${DOCKER_CONTAINER_NAME}
