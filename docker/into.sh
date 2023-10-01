#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source ${DIR}/.source/variables.sh

if [[ ! -z "$1" ]]; then
    CONTAINER_NAME=$1
else
    echo Please specify the Docker CONTAINER_NAME as the first argument
    exit 1
fi

docker exec -it ${CONTAINER_NAME} /bin/bash
