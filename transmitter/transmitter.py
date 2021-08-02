import logging
import logging.config


from config import LOGGING
from config import PIKA_PARAMETERS, QUEUE
from config import BOT_TOKEN

import telebot
import marshmallow

from schemas import RabbitReplySchema

from pika_wrapper import Client, Queue


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('telebot_transmitter')


def bot_maker():
    try:
        bot = telebot.TeleBot(BOT_TOKEN)
    except Exception as ex:
        logger.error(f'    [*]    create bot - "{ex}"')
        return bot_maker()
    else:
        logger.info(f'    [*]    bot created')
        return bot


bot = bot_maker()


def send_something(body: bytes,
                 reply_threadsafe: callable = None
                 ):
    logger.info(f'    [*]    body = "{body}"')
    try:
        data = RabbitReplySchema().loads(body.decode())
    except marshmallow.ValidationError as err:
        logger.error(f'    [*]    ValidationError - "{err}"')
        return False
    except Exception as err:
        logger.error(f'    [*]    Error - "{err}"')
        return False
    logger.info(f'    [*]    data = "{data}"')
    if data.get('text', ''):
        try:
            bot.send_message(chat_id=data['message']['chat']['id'], text=data['text'])
        except Exception as ex:
            logger.error(f'    [*]    send message - "{ex}"')
            send_something(body)


consumer = Client(parameters=PIKA_PARAMETERS, prefetch_count=1)
consumer.queues['queue'] = Queue(name=QUEUE, durable=True)

consumer.connect()

consumer.setup_consumer(
    queue=consumer.queues['queue'],
    callback=send_something
)

consumer.start_consuming()
