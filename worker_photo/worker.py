import json
from pathlib import Path

import logging
import logging.config

import pika
from pika.exchange_type import ExchangeType
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from config import PIKA_PARAMETERS, QUEUE
from config import LOGGING

import requests
from PIL import Image

from pika_wrapper import Client, Queue, Exchange

import telebot


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('telebot_photo_worker')

consumer = Client(parameters=PIKA_PARAMETERS, prefetch_count=1)
queue = Queue(name=QUEUE, durable=True)
consumer.queues['queue'] = queue

consumer.connect()


def callback(body: bytes,
             reply_threadsafe: callable = None
             ):
    logger.info(f'    [*]    body="{body}"')
    message = json.loads(body)
    logger.info(f'    [*]    message = "{message}"')
    chat_id = message['chat']['id']
    try:
        bot = telebot.TeleBot(message.get('token'))
    except Exception as ex:
        logger.error(f'    [*]    unsuccesfull create bot - "{ex}"')
        return False

    # for photo_path in message.get('photo_paths', []):
    photo_path = message.get('photo_paths')[-1]
    path = Path(photo_path)
    url = 'https://api.telegram.org/file/bot{0}/{1}'.format(
        message.get('token'),
        photo_path
        )
    photo_file = requests.get(url)
    if photo_file.status_code == 200:
        path.parent.mkdir(exist_ok=True, parents=True)
        with open(path, 'wb') as f:
            f.write(photo_file.content)

        image = Image.open(path)
        grayscale = image.convert('L')

        grayscale.save(path)

        photo = open(path, 'rb')
        bot.send_chat_action(chat_id, 'upload_photo')
        bot.send_photo(
            chat_id,
            photo,
            reply_to_message_id=message['message_id'],
            caption=message.get('caption')
            )
        path.unlink()
    return True 


consumer.setup_consumer(queue=queue, callback=callback)
consumer.start_consuming()
