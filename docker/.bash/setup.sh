# Should be called after: "source .bash/variables" -> "CONTAINER_NAME" -> "source .bash/set_user"
IFS=":" read IMAGE_REPO IMAGE_TAG <<< "${IMAGE_REPO_TAG}"
DOCKER_SIGNATURE="[${IMAGE_REPO}][${IMAGE_TAG}][${CONTAINER_NAME}]"

# Define the Docker Username
if [ "${VERBOSE_USERNAME}" = "1" ]; then
    DOCKER_USERNAME="${DOCKER_SIGNATURE}"[${USER}]
else
    DOCKER_USERNAME="${USER}"
fi

SET_USER="${DOCKER_USERNAME}:x:${USER_ID}:${GROUP_ID}:${DOCKER_USERNAME}"
echo "${SET_USER}" > ${DIR}/.bash/passwd

echo "alias signature='echo ${DOCKER_SIGNATURE}'" > ${DIR}/.bash/.bashrc
