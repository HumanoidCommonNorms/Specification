#!/bin/bash
echo ==================================================
echo "[Create network]"
echo ==================================================
INI_FILE=$(readlink -f $(dirname $0)/../config.ini)
source <(sed -n -E 's/^\s*(\S+)\s*=\s*(.+)$/\1=\2/p' <"${INI_FILE}")
echo "  Docker netowr:"
echo "      name   : ${DOCKER_NETWORK_NAME}"
echo "      subnet : ${DOCKER_NETWORK_SUBNET}"
echo ==================================================
ret=0

FILTER_LIST=($(docker network ls --format "{{.Name}}" --filter "name=${DOCKER_NETWORK_NAME}"))
for LINE in ${FILTER_LIST}; do
    if [ "${LINE}" == "${DOCKER_NETWORK_NAME}" ]; then
        ret=1
    fi
done

if [ 0 -eq ${ret} ]; then
    docker network create ${DOCKER_NETWORK_NAME} --subnet ${DOCKER_NETWORK_SUBNET} > /dev/null
    ret=$?
    if [ 0 -eq ${ret} ]; then
        echo [INFO] Create network : ${DOCKER_NETWORK_NAME}
        echo //////////////////////////////////////////////////
        echo docker network inspect ${DOCKER_NETWORK_NAME}
        echo --------------------------------------------------
        docker network inspect ${DOCKER_NETWORK_NAME}
    fi
fi
echo //////////////////////////////////////////////////
docker network ls
echo --------------------------------------------------
