import pika
import os

RABBITMQ_URL = os.getenv(
    'RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/%2F')
PIKA_PARAMETERS = pika.URLParameters(
    RABBITMQ_URL
)

EXCHANGE = os.getenv('EXCHANGE', 'speedtest_exchange')
MESSAGE_PING = os.getenv('MESSAGE_PING', 'Пинг - {ping} ms')
MESSAGE_DOWN = os.getenv('MESSAGE_DOWN', 'Скорость закачки - {speed} Mbps')
MESSAGE_UP = os.getenv('MESSAGE_UP', 'Скорость отдачи - {speed} Mbps')


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
