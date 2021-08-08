import json

import logging
import logging.config

from pika.exchange_type import ExchangeType

import speedtest

from config import PIKA_PARAMETERS, EXCHANGE
from config import LOGGING
from config import DEVICE_NAME

from pika_wrapper import Client, Queue, Exchange


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('telebot_temp_worker')

consumer = Client(parameters=PIKA_PARAMETERS, prefetch_count=1)
exchange = Exchange(exchange=EXCHANGE, exchange_type=ExchangeType.fanout)
consumer.exchanges['exchange'] = exchange
queue = Queue(name='')
queue.exchange = exchange
consumer.queues['queue'] = queue

consumer.connect()

st = speedtest.Speedtest()


def callback(body: bytes,
             reply_threadsafe: callable = None
             ):
    logger.info(f'    [*]    body="{body}"')

    reply_threadsafe(json.dumps(
        {
            'message': json.loads(body.decode()),
            'text': f'Измеряю на {DEVICE_NAME}'
        }
    ).encode()
    )

    server = st.get_best_server()
    reply_threadsafe(json.dumps(
        {
            'message': json.loads(body.decode()),
            'text': f'Для измерения на {DEVICE_NAME} выбран сервер - "{server.get("url")}". Ping = {server.get("latency")} ms'
        }
    ).encode()
    )

    down = st.download()/1000000
    reply_threadsafe(json.dumps(
        {
            'message': json.loads(body.decode()),
            'text': f'Скорость закачки на {DEVICE_NAME}- {down} Mbps'
        }
    ).encode()
    )

    up = st.upload()/1000000
    reply_threadsafe(json.dumps(
        {
            'message': json.loads(body.decode()),
            'text': f'Скорость отдачи на {DEVICE_NAME} - {up} Mbps'
        }
    ).encode()
    )

    return True


consumer.setup_consumer(queue=queue, callback=callback)
consumer.start_consuming()
