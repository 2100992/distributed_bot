FROM python:3.8-alpine

ENV USER usr
ENV HOME /home/${USER}

# Установка необходимых зависимостей для запускающего Python скрипта
COPY ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR ${HOME}
COPY . ${HOME}

CMD python receiver.py
