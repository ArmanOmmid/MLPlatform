# Should be called after: "source .bash/variables" -> "CONTAINER_NAME" -> "source .bash/set_user"
IFS=":" read IMAGE_REPO IMAGE_TAG <<< "${IMAGE_REPO_TAG}"
DOCKER_SIGNATURE="[${IMAGE_REPO}]-[${IMAGE_TAG}]-[${CONTAINER_NAME}]" # Repo - Tag - Container

# Define the Docker Username
if [ "${VERBOSE_USERNAME}" = "1" ]; then
    DOCKER_USERNAME="${DOCKER_SIGNATURE} - ${USER}"
else
    DOCKER_USERNAME="[D] - ${USER}"
fi

TMP_PATH=${PROJECT_ROOT}/docker/.source/.tmp
mkdir -p ${TMP_PATH}

SET_USER="${DOCKER_USERNAME}:x:${USER_ID}:${GROUP_ID}:${DOCKER_USERNAME}:/home:/bin/bash"
echo "${SET_USER}" > ${TMP_PATH}/passwd

# Create .bashrc and write to it for initial bash commands
echo "SIGNATURE_COMMAND=\"echo ; echo ${DOCKER_SIGNATURE} ; echo\"" > ${TMP_PATH}/.bashrc # > recreates
echo "echo ; echo ${DOCKER_SIGNATURE} ; echo" >> ${TMP_PATH}/.bashrc # >> appends
echo "alias signature=\"\${SIGNATURE_COMMAND}\"" >> ${TMP_PATH}/.bashrc
echo "alias sig=\"\${SIGNATURE_COMMAND}\"" >> ${TMP_PATH}/.bashrc
echo "alias rtc=\"\${SIGNATURE_COMMAND}\"" >> ${TMP_PATH}/.bashrc
