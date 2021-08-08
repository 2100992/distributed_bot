import json

import logging
import logging.config


import pika
from pika.exchange_type import ExchangeType
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from config import PIKA_PARAMETERS, EXCHANGE
from config import LOGGING, DEVICE_NAME


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


def callback(body: bytes,
             reply_threadsafe: callable = None
             ):
    logger.info(f'    [*]    body="{body}"')
    logger.error('invalid reply_threadsafe')
    assert reply_threadsafe, 'invalid reply_threadsafe'

    reply_threadsafe(json.dumps(
        {
            'message': json.loads(body.decode()),
            'text': f'Измеряю на {DEVICE_NAME}'
        }
    ).encode()
    )

    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = f.read()
    except:
        reply_threadsafe(json.dumps(
            {
                'message': json.loads(body.decode()),
                'text': f'Устройство {DEVICE_NAME} не поддерживается'
            }
        ).encode()
        )
    else:
        try:
            temp = float(temp)/1000
        except:
            temp = 0

        reply_threadsafe(json.dumps(
            {
                'message': json.loads(body.decode()),
                'text': f'Температура процессора {DEVICE_NAME} - {temp} градусов цельсия'
            }
        ).encode()
        )

    return True


consumer.setup_consumer(queue=queue, callback=callback)
consumer.start_consuming()
