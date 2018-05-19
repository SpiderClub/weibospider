import os
import logging
from logging import config as log_conf

from ..config import (
    log_dir, log_name)


__all__ = ['crawler_logger', 'parser_logger',
           'db_logger', 'other_logger']


abslote_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), log_dir)
if not os.path.exists(abslote_dir):
    os.mkdir(abslote_dir)

log_path = os.path.join(abslote_dir, log_name)

log_config = {
    'version': 1.0,
    'formatters': {
        'detail': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detail'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'filename': log_path,
            'level': 'INFO',
            'formatter': 'detail',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'crawler_logger': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'parser_logger': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'other_logger': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'db_logger': {
            'handlers': ['file'],
            'level': 'INFO',
        }
    }
}

log_conf.dictConfig(log_config)

crawler_logger = logging.getLogger('crawler_logger')
parser_logger = logging.getLogger('parser_logger')
db_logger = logging.getLogger('db_logger')
other_logger = logging.getLogger('other_logger')