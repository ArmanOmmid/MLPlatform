ARG BASE_REPO_TAG
FROM ${BASE_REPO_TAG}

COPY requirements /app/requirements
RUN pip3 install -r /app/requirements/requirements.txt
RUN pip3 install -r /app/requirements/cicd.txt

ARG PROJECT_NAME
COPY . /app/${PROJECT_NAME}

# Default user instead of root
RUN echo "docker:x:9999:0:docker:/home:/bin/bash" >> /etc/passwd
USER docker

WORKDIR /app/${PROJECT_NAME}
