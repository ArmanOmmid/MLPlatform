#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source ${DIR}/../.source/variables.sh

if [[ ! -z "$1" ]]; then
    BASE_REPO_TAG=$1
fi

set -x # Echo command lines before executing; set +x = off
docker build \
    --pull \
    -f ${DIR}/Dockerfile \
    -t ${BASE_REPO_TAG} \
    ${DIR}
docker image prune -f
