FROM python:3.8-slim

ENV USER usr
ENV HOME /home/${USER}

RUN apt-get update

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
RUN apt-get install -y tzdata

COPY ./requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

WORKDIR ${HOME}
COPY . ${HOME}


CMD python worker.py
