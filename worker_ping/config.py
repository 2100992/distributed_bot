import pika
import os

RABBITMQ_URL = os.getenv(
    'RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/%2F')
PIKA_PARAMETERS = pika.URLParameters(
    RABBITMQ_URL
)

QUEUE = os.getenv('QUEUE', 'ping_queue')


LOG_NAME = 'log.txt'
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
