FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

LABEL maintainer="Nehcy <cibershaman@gmail.com>"

ARG NB_USER="wald"
ARG NB_UID="1000"
ARG NB_GID="100"
ARG NB_DIR="work"

RUN apt-get update --yes && \
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    python3 python-is-python3 pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create NB_USER with name NB_USER user with UID=1000 and in the 'users' group
#chmod g+w /etc/passwd && \

RUN useradd -l -m -s /bin/bash -N -u "${NB_UID}" "${NB_USER}" # && \
    chown "${NB_USER}:${NB_GID}" "/home/${NB_USER}/"
 
USER "${NB_UID}"

WORKDIR "/home/${NB_USER}/"

ENV PATH="$PATH:/home/${NB_USER}/.local/bin"

COPY requirements.txt ./

RUN python -m pip install --user --upgrade pip && \
    pip install --user -r requirements.txt && \
    python -m pip cache purge

WORKDIR "./${NB_DIR}"

ARG TG_TOKEN=""

ENV TG_TOKEN="${TG_TOKEN}" 
