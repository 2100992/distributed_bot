import json

import logging
import logging.config

from pika.exchange_type import ExchangeType

import pyspeedtest

from config import PIKA_PARAMETERS, EXCHANGE
from config import LOGGING, MESSAGE_UP, MESSAGE_DOWN, MESSAGE_PING


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

st = pyspeedtest.SpeedTest()


def callback(body: bytes,
             reply_threadsafe: callable = None
             ):
    logger.info(f'    [*]    body="{body}"')

    reply_threadsafe(json.dumps(
        {
            'message': json.loads(body.decode()),
            'text': 'Подождите, измеряю'
        }
    ).encode()
    )

    reply_threadsafe(json.dumps(
        {
            'message': json.loads(body.decode()),
            'text': MESSAGE_PING.format(ping=st.ping())
        }
    ).encode()
    )

    reply_threadsafe(json.dumps(
        {
            'message': json.loads(body.decode()),
            'text': MESSAGE_DOWN.format(speed=st.download()/1000000)
        }
    ).encode()
    )

    reply_threadsafe(json.dumps(
        {
            'message': json.loads(body.decode()),
            'text': MESSAGE_UP.format(speed=st.upload()/1000000)
        }
    ).encode()
    )


consumer.setup_consumer(queue=queue, callback=callback)
consumer.start_consuming()
