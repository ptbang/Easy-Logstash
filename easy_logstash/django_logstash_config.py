import logging
from typing import Any

from easy_logstash.constants import LOG_LEVELS, LOGSTASH_NAMESPACE


class DjangoLogstashConfig:
    DJANGO_LOGGER_NAME = 'django'
    DJANGO_LOGSTASH_HANDLER_NAME = 'django-logstash'
    DJANGO_LOGSTASH_HANDLER_LEVEL = LOG_LEVELS[logging.WARNING]
    DJANGO_LOGGERS_LEVEL = LOG_LEVELS[logging.DEBUG]
    DEFAULT_CONSOLE_LEVEL = LOG_LEVELS[logging.INFO]
    HANDLER_CLASS = 'logstash_async.handler.AsynchronousLogstashHandler'
    TRANSPORT = 'logstash_async.transport.TcpTransport'

    def __init__(self, host: str, port: int, database_path: str, elasticsearch_index: str) -> None:
        self.host = host
        self.port = port
        self.database_path = database_path
        self.elasticsearch_index = elasticsearch_index
        self.APP_LOGSTASH_LOGGER_NAME = self.LOGSTASH_HANDLER_NAME = self._get_logstash_logger_name()

    def get_dict_config(self) -> dict:
        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {
                'require_debug_false': {
                    '()': 'django.utils.log.RequireDebugFalse',
                },
                'require_debug_true': {
                    '()': 'django.utils.log.RequireDebugTrue',
                },
            },
            'formatters': {
                'logstash': {
                    '()': 'logstash_async.formatter.DjangoLogstashFormatter',
                    'fqdn': False,
                    'metadata': {'index_suffix': f'{LOGSTASH_NAMESPACE}-{self.elasticsearch_index}'},
                }
            },
            'handlers': {
                'console': {
                    'level': self.DEFAULT_CONSOLE_LEVEL,
                    'filters': ['require_debug_true'],
                    'class': 'logging.StreamHandler',
                },
                self.DJANGO_LOGSTASH_HANDLER_NAME: self._get_handler(self.DJANGO_LOGSTASH_HANDLER_LEVEL),
                self.LOGSTASH_HANDLER_NAME: self._get_handler(LOG_LEVELS[logging.DEBUG]),
            },
            'loggers': {
                self.DJANGO_LOGGER_NAME: {
                    'handlers': [self.DJANGO_LOGSTASH_HANDLER_NAME, 'console'],
                    'level': self.DJANGO_LOGGERS_LEVEL,
                    'propagate': False,
                },
                self.APP_LOGSTASH_LOGGER_NAME: {
                    'handlers': [self.LOGSTASH_HANDLER_NAME],
                    'level': LOG_LEVELS[logging.DEBUG],
                    'propagate': False,
                },
            },
        }
        return config

    def _get_handler(self, level: str = LOG_LEVELS[logging.DEBUG]) -> dict[str, Any]:
        return {
            'level': level,
            'class': 'logstash_async.handler.AsynchronousLogstashHandler',
            'formatter': 'logstash',
            'transport': 'logstash_async.transport.TcpTransport',
            'host': self.host,
            'port': self.port,
            'database_path': self.database_path,
        }

    def _get_logstash_logger_name(self) -> str:
        return f'{LOGSTASH_NAMESPACE}-{self.elasticsearch_index}'

    def get_logger(self, name: str | None = None) -> logging.Logger:
        name = f'.{name}' if name else ''
        return logging.getLogger(f'{self.APP_LOGSTASH_LOGGER_NAME}{name}')
