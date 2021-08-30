import json

import logging
import logging.config


from config import PIKA_PARAMETERS, QUEUE
from config import LOGGING


from pika_wrapper import Client, Queue


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

    reply_threadsafe(json.dumps(
        {
            'message': json.loads(body.decode()),
            'text': 'pong'
        }
    ).encode()
    )

    return True


consumer.setup_consumer(queue=queue, callback=callback)
consumer.start_consuming()
