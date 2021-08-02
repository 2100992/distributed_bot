import os
import json
import pika

BOT_TOKEN = os.getenv('BOT_TOKEN', 'youre_bot_token')
ADMIN_IDS = json.loads(os.getenv('ADMIN_IDS', '[]'))

RABBITMQ_URL = os.getenv(
    'RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/%2F')
PIKA_PARAMETERS = pika.URLParameters(
    RABBITMQ_URL
)

REPLY_TO_QUEUE = os.getenv('REPLY_TO_QUEUE', 'bot_reply_queue')

queue_commands = {
    'start': {'admins_only': False},
    'who_am_i': {'admins_only': False},
    'test': {'admins_only': True},
    'ping': {'admins_only': False}
}

topic_commands = {
    'speedtest': {'admins_only': True},
    'temp': {'admins_only': True},
}

LOG_NAME = 'bot_receiver.log'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-26s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-26s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': LOG_NAME
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': [
                'console',
                'file'
            ]
        },
    }
}
