#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source ${DIR}/../.bash/variables.sh

set -x # Echo command lines before executing; set +x = off
docker build \
    --build-arg BASE_REPO_TAG=${BASE_REPO_TAG} \
    --build-arg PROJECT_NAME=${PROJECT_NAME} \
    -f ${DIR}/Dockerfile \
    -t ${IMAGE_REPO_TAG} \
    ${PROJECT_ROOT}
docker image prune -f
