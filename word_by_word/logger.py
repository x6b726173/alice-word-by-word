import logging.config
import os

logs_dir = os.path.join(os.path.dirname(__file__), 'logs')

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_and_file': {
            'format': '%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',  # noqa
            'datefmt': "%Y-%m-%d %H:%M:%S%z",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_and_file',
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(logs_dir, 'info.log'),
            'when': 'MIDNIGHT',
            'backupCount': 5,
            'encoding': 'utf-8',
            'formatter': 'console_and_file',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(logs_dir, 'error.log'),
            'when': 'MIDNIGHT',
            'backupCount': 5,
            'encoding': 'utf-8',
            'formatter': 'console_and_file'
        },
        'player_says': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(logs_dir, 'player_says.log'),
            'when': 'MIDNIGHT',
            'backupCount': 5,
            'encoding': 'utf-8',
            'formatter': 'console_and_file'
        }

    },
    'loggers': {
        'base': {
            'handlers': ['console', 'file_info', 'file_error'],
            'propagate': False,
            'level': 'DEBUG'
        },
        'words': {
            'handlers': ['console', 'player_says'],
            'propagate': False,
            'level': 'INFO'
        }
    }
}

logging.config.dictConfig(LOGGING)
