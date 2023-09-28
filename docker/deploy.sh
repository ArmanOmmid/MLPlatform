#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source ${DIR}/.bash/variables.sh

if [[ ! -z "$1" ]]; then
    CONTAINER_NAME=$1
fi

source ${DIR}/.bash/setup.sh
set -x # Echo every command line below before executing
docker run --rm -it \
    --pids-limit -1 \
    -u ${USER_ID}:${GROUP_ID} \
    --volume ${DIR}/.bash/passwd:/etc/passwd:ro \
    --name ${CONTAINER_NAME} \
    --hostname ${HOST_NAME} \
    ${GPUS} \
    ${IMAGE_REPO_TAG} \
    /bin/bash
