#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source ${DIR}/.source/variables.sh

if [[ ! -z "$1" ]]; then
    CONTAINER_NAME=$1
fi

source ${DIR}/.source/setup.sh
set -x # Echo every command line below before executing
docker run --rm -it \
    --pids-limit ${PID_LIMIT} \
    -u ${USER_ID}:${GROUP_ID} \
    --volume ${TMP_PATH}/passwd:/etc/passwd:ro \
    --volume ${TMP_PATH}/.bashrc:/app/.bashrc:ro \
    --volume ${PROJECT_ROOT}:${DOCKER_WORKDIR} \
    --name ${CONTAINER_NAME} \
    --hostname ${HOST_NAME} \
    ${GPUS} \
    ${IMAGE_REPO_TAG} \
    /bin/bash --init-file /app/.bashrc
