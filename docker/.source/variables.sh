# "source ./bash/variables"
PROJECT_ROOT_INDICATOR=docker
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
while [[ ! -d "${PROJECT_ROOT}/${PROJECT_ROOT_INDICATOR}" ]]; do
  PROJECT_ROOT=$(dirname "${PROJECT_ROOT}")
done
PROJECT_NAME=$(basename "${PROJECT_ROOT}")
DOCKER_WORKDIR=/app/${PROJECT_NAME}

USER_ID=$(id -u ${USER})
GROUP_ID=$(id -g ${USER})
HOST_NAME=$(hostname)

GPUS="" # Docker NVidia Support with [GPUS=--gpus all] or [GPUS=--gpus "device=0, 1"]
BASE_REPO_TAG=mlplatform/base:latest
IMAGE_REPO_TAG=mlplatform/dev:latest
CONTAINER_NAME=$(date +"%Y-%m-%d_%H-%M-%S")
VERBOSE_USERNAME=0
