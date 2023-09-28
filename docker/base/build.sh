#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source ${DIR}/../source/variables.sh

set -x # Echo command lines before executing; set +x = off
docker build \
    --pull \
    -f ${DIR}/Dockerfile \
    -t ${BASE_REPO_TAG} \
    ${DIR}
docker image prune -f
