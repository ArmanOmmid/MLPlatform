#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source ${DIR}/.source/variables.sh

if [[ ! -z "$1" ]]; then
    CONTAINER_NAME=$1
else
    echo Please specify the Docker CONTAINER_NAME as the first argument
    exit 1
fi

if [[ ! -z "$2" ]]; then
    COMMANDS="" # We need to recover the original argument seperations from argument quotations
    for arg in "${@:2}"; do
        COMMANDS="${COMMANDS} \"${arg}\""
    done
else
    echo Please specify the Docker COMMANDS as the second++ arguments
    exit 1
fi

source ${DIR}/.source/setup.sh
set -x # Echo every command line below before executing
docker run --rm \
    --pids-limit -1 \
    -u ${USER_ID}:${GROUP_ID} \
    --volume ${TMP_PATH}/passwd:/etc/passwd:ro \
    --volume ${TMP_PATH}/.bashrc:/app/.bashrc:ro \
    --volume ${PROJECT_ROOT}:${DOCKER_WORKDIR} \
    --name ${CONTAINER_NAME} \
    --hostname ${HOST_NAME} \
    ${GPUS} \
    ${IMAGE_REPO_TAG} \
    /bin/bash -c "source ../.bashrc && echo "COMMANDS:" && echo ""${COMMANDS}"" && echo && ${COMMANDS}"
