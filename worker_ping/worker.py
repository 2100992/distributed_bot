import json

import logging
import logging.config


import pika
from pika.exchange_type import ExchangeType
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from config import PIKA_PARAMETERS, QUEUE
from config import LOGGING


from pika_wrapper import Client, Queue, Exchange


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('telebot_ping_worker')

consumer = Client(parameters=PIKA_PARAMETERS, prefetch_count=1)
queue = Queue(name=QUEUE, durable=True)
consumer.queues['queue'] = queue

consumer.connect()


def callback(body: bytes,
             reply_threadsafe: callable = None
             ):
    logger.info(f'    [*]    body="{body}"')
    if reply_threadsafe:
        reply_threadsafe(json.dumps(
            {
                'message': json.loads(body.decode()),
                'text': 'wait please'
            }
        ).encode()
        )
    return json.dumps(
        {
            'message': json.loads(body.decode()),
            'text': 'pong'
        }
    ).encode()


consumer.setup_consumer(queue=queue, callback=callback)
consumer.start_consuming()
