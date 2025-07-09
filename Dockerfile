# docker buildx build -t blackboard .
# docker run -it blackboard

# Noble Numbat, 24.04 LTS
FROM ubuntu:noble AS base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get install -y \
        libcairo2-dev \
        libgif-dev \
        libgirepository1.0-dev \
        libjpeg8-dev \
        libpango1.0-dev \
        build-essential \
        cloc \
        cmake \
        g++ \
        git \
        net-tools \
        pipx \
        pkg-config \
        python-is-python3 \
        python3-pip \
        python3-venv \
        sudo \
        vim && \
    pipx install cookiecutter && \
    apt-get clean

WORKDIR /app
COPY . .
RUN mkdir /dojo-secrets

# RUN pipx runpip cookiecutter install -r requirements.txt
RUN touch /dojo-secrets/api-keys.txt && \
    useradd --create-home bboard && \
    chown -R bboard:bboard /app /dojo-secrets && \
    usermod -aG sudo bboard && \
    echo "bboard ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER bboard
ENTRYPOINT ["bash"]
