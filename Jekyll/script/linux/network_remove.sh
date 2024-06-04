#!/bin/bash
echo ==================================================
echo "[Remove network]"
echo ==================================================
INI_FILE=$(readlink -f $(dirname $0)/../config.ini)
source <(sed -n -E 's/^\s*(\S+)\s*=\s*(.+)$/\1=\2/p' <"${INI_FILE}")
echo "  Docker netowr:"
echo "      name   : ${DOCKER_NETWORK_NAME}"
echo "      subnet : ${DOCKER_NETWORK_SUBNET}"
echo ==================================================

FILTER_LIST=($(docker network ls --format "{{.Name}}" --filter "name=${DOCKER_NETWORK_NAME}"))
for LINE in ${FILTER_LIST}; do
    if [ "${LINE}" == "${DOCKER_NETWORK_NAME}" ]; then
        docker network rm ${DOCKER_NETWORK_NAME} > /dev/null
        echo [INFO] Remove existing network : ${DOCKER_NETWORK_NAME}
    fi
done

echo //////////////////////////////////////////////////
docker network ls
echo --------------------------------------------------
