# Download base image ubuntu 14.04
FROM ubuntu:20.04

# LABEL about the custom image
LABEL maintainer="leber@technikum-wien.at"
LABEL version="0.1"
LABEL description="This is custom Docker Image for \
running the BPMNbasedController"

ARG DEBIAN_FRONTEND=noninteractive

## installing dependencies
RUN apt update -y
RUN apt upgrade -y
RUN apt install -y python3-pip

RUN pip3 install numpy networkx math3d scipy ipython pypubsub python-dateutil pytz lxml cryptography pyyaml
RUN pip3 install matplotlib

## copy files into image
RUN mkdir /usr/src/samy
WORKDIR /usr/src/samy
COPY . ./

RUN pip3 install pip/opcua-0.98.13-py3-none-any.whl