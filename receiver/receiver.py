import json
import logging.config
import logging

import pika
from pika.exchange_type import ExchangeType

import telebot
import telebot.types

from pika_wrapper import Client, Queue, Exchange

from config import BOT_TOKEN, ADMIN_IDS
from config import PIKA_PARAMETERS, REPLY_TO_QUEUE
from config import topic_commands, queue_commands
from config import LOGGING


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('telebot_receiver')

bot = telebot.TeleBot(BOT_TOKEN)

publisher = Client(parameters=PIKA_PARAMETERS, prefetch_count=1)

publisher.queues[REPLY_TO_QUEUE] = Queue(name=REPLY_TO_QUEUE, durable=True)

for _command in queue_commands:
    publisher.queues[_command] = Queue(
        name=_command + '_queue',
        durable=True
    )

for _command in topic_commands:
    publisher.exchanges[_command] = Exchange(
        exchange=_command+'_exchange',
        exchange_type=ExchangeType.fanout
    )

publisher.queues['text'] = Queue(
    name='text_queue',
    durable=True
)


@bot.message_handler(commands=list(queue_commands))
def handle_queue_commands(message: telebot.types.Message):
    if message.text:
        _command = message.text[1:]
    else:
        return False

    if queue_commands[_command]['admins_only']:
        if message.from_user.id in ADMIN_IDS:
            publisher.publish(
                body=json.dumps(message.json),
                queue=publisher.queues[_command],
                exchange='',
                reply_to_queue=publisher.queues[REPLY_TO_QUEUE],
                properties=pika.BasicProperties(
                    correlation_id=str(message.from_user.id)
                )
            )
            print('admin publish')
        else:
            bot.reply_to(message, 'Это только для админов')
    else:
        publisher.publish(
            body=json.dumps(message.json),
            queue=publisher.queues[_command],
            exchange='',
            reply_to_queue=publisher.queues[REPLY_TO_QUEUE],
            properties=pika.BasicProperties(
                correlation_id=str(message.from_user.id)
            )
        )
        print('no_admin publish')


@bot.message_handler(commands=list(topic_commands))
def handle_topic_commands(message: telebot.types.Message):
    if message.text:
        _command = message.text[1:]
    else:
        return False

    if topic_commands[_command]['admins_only']:
        if message.from_user.id in ADMIN_IDS:
            publisher.publish(
                body=json.dumps(message.json),
                queue='',
                exchange=publisher.exchanges[_command],
                reply_to_queue=publisher.queues[REPLY_TO_QUEUE],
                properties=pika.BasicProperties(
                    correlation_id=str(message.from_user.id)
                )
            )
            print('admin publish')
        else:
            bot.reply_to(message, 'Это только для админов')
    else:
        publisher.publish(
            body=json.dumps(message.json),
            queue='',
            exchange=publisher.exchanges[_command],
            reply_to_queue=publisher.queues[REPLY_TO_QUEUE],
            properties=pika.BasicProperties(
                correlation_id=str(message.from_user.id)
            )
        )
        print('no_admin publish')


publisher.connect()
bot.polling()
