FROM python:3

ENV USER usr
ENV HOME /home/${USER}


RUN apt-get update

# Добавление таймзоны в сервис что бы логер писал логи с указанием коректного времени
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
RUN apt-get install -y tzdata

RUN apt install -y python3-pip

# Установка необходимых зависимостей для запускающего Python скрипта
COPY ./requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

WORKDIR ${HOME}
COPY . ${HOME}
RUN git clone https://github.com/2100992/pika_wrapper.git

CMD python transmitter.py

