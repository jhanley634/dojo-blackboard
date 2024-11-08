# docker buildx build -t blackboard .
# docker run -it blackboard

# Noble Numbat, 24.04 LTS
FROM ubuntu:noble AS base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        libgirepository1.0-dev \
        libcairo2-dev \
        libjpeg8-dev \
        libpango1.0-dev \
        libgif-dev \
        build-essential \
        cmake \
        g++ \
        pipx \
        pkg-config \
        python3-pip \
        python3-venv \
        vim && \
    pipx install cookiecutter \
    && apt-get clean

WORKDIR /app
COPY . /app
# RUN pipx runpip cookiecutter install -r requirements.txt

ENTRYPOINT ["bash"]
