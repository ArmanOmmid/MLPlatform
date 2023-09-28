#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source ${DIR}/../source/variables.sh

if [[ ! -z "$1" ]]; then
    BASE_REPO_TAG=$1
fi

if [[ ! -z "$2" ]]; then
    IMAGE_REPO_TAG=$2
fi

if [[ ! -z "$3" ]]; then
    PROJECT_NAME=$3
fi

set -x # Echo command lines before executing; set +x = off
docker build \
    --build-arg BASE_REPO_TAG=${BASE_REPO_TAG} \
    --build-arg PROJECT_NAME=${PROJECT_NAME} \
    -f ${DIR}/Dockerfile \
    -t ${IMAGE_REPO_TAG} \
    ${PROJECT_ROOT}
docker image prune -f
