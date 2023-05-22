# Use an official Ubuntu base image
FROM ubuntu:latest

# Update the package manager and install required dependencies
RUN apt-get update
RUN apt-get install -y git curl jq file unzip make gcc g++ python3 python-dev-is-python3 libtool nmap pip redis nginx gunicorn

# Create the server directory
RUN mkdir -p /mnt/server

# Set the working directory
WORKDIR /mnt/server

# Conditionally clone the Git repository
ARG GIT_ADDRESS
ARG BRANCH
ARG REQUIREMENTS_FILE

RUN if [ "${USER_UPLOAD}" == "true" ] || [ "${USER_UPLOAD}" == "1" ]; then \
        echo -e "assuming user knows what they are doing have a good day." && \
        exit 0; \
    fi

RUN if [[ ${GIT_ADDRESS} != *.git ]]; then \
        GIT_ADDRESS=${GIT_ADDRESS}.git; \
    fi


RUN if [ "$(ls -A /mnt/server)" ]; then \
        echo -e "/mnt/server directory is not empty."; \
        if [ -d *.git ]; then \
            echo -e ".git directory exists"; \
            if [ -f .git/config ]; then \
                echo -e "loading info from git config"; \
                ORIGIN=$(git config --get remote.origin.url); \
            else \
                echo -e "files found with no git config"; \
                echo -e "closing out without touching things to not break anything"; \
                exit 10; \
            fi; \
        fi; \
        if [ "${ORIGIN}" == "${GIT_ADDRESS}" ]; then \
            echo "pulling latest from github"; \
            git pull; \
        fi; \
    else \
        echo -e "/mnt/server is empty.\ncloning files into repo"; \
        if [ -z ${BRANCH} ]; then \
            echo -e "cloning default branch"; \
            git clone ${GIT_ADDRESS} .; \
        else \
            echo -e "cloning ${BRANCH}'"; \
            git clone --single-branch --branch ${BRANCH} ${GIT_ADDRESS} .; \
        fi; \
    fi

# Set the HOME environment variable
ENV HOME=/mnt/server

# Install Python requirements
RUN echo "Installing python requirements into folder" && \
    if [ -f /mnt/server/requirements.txt ]; then \
        pip install -U --prefix .local -r ${REQUIREMENTS_FILE}; \
    fi

# Expose port 80 for HTTP traffic
EXPOSE 8080

# Print installation complete message
RUN echo -e "install complete"

ENTRYPOINT ["pip", "install", "-r", "requirements.txt"]
