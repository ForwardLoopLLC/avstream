FROM python:3.6 

# modified from Dockerfile for https://github.com/chrisdaish/docker-vlc
# to use debian instead of ubuntu

MAINTAINER "Nick F. Settje <nick@forward-loop.com>"

RUN apt-get update && apt-get install -y multiarch-support
RUN apt-get install -y debconf vlc

# need to run vlc as non-root user
ENV GID 1000
ENV UID 1000
RUN \
        useradd -m vlc && \
        groupmod -g $GID vlc && \
        usermod -u $UID -g $GID vlc
