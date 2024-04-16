import datetime
import logging
from unittest import TestCase

from easy_logstash.constants import LOG_LEVELS, LOGSTASH_NAMESPACE
from easy_logstash.django_logstash_config import DjangoLogstashConfig
from easy_logstash.logstash_config import EasyLogstashConfig
from tests.mixins import TestMixin


class SendLogTest(TestCase, TestMixin):
    @classmethod
    def setUpClass(cls) -> None:
        cls.django_log_config = DjangoLogstashConfig(
            cls.LOGSTASH_HOST, cls.LOGSTASH_PORT, str(cls.LOGSTASH_DATABASE_PATH), cls.ELASTICSEARCH_INDEX
        )

    def test_init(self) -> None:
        self.assertEqual(
            self.django_log_config.APP_LOGSTASH_LOGGER_NAME, f'{LOGSTASH_NAMESPACE}-{self.ELASTICSEARCH_INDEX}'
        )
        self.assertEqual(
            self.django_log_config.LOGSTASH_HANDLER_NAME, f'{LOGSTASH_NAMESPACE}-{self.ELASTICSEARCH_INDEX}'
        )

    def test_get_config(self) -> None:
        settings_logging = self.django_log_config.get_dict_config()
        self.assertFalse(settings_logging['disable_existing_loggers'])
        filters = {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        }
        self.assertEqual(settings_logging['filters'], filters)
        formatters = {
            'logstash': {
                '()': 'logstash_async.formatter.DjangoLogstashFormatter',
                'fqdn': False,
                'metadata': {'index_suffix': f'{LOGSTASH_NAMESPACE}-{self.ELASTICSEARCH_INDEX}'},
            }
        }
        self.assertEqual(settings_logging['formatters'], formatters)
        handlers = {
            'console': {
                'level': self.django_log_config.DEFAULT_CONSOLE_LEVEL,
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            },
            self.django_log_config.DJANGO_LOGSTASH_HANDLER_NAME: self.django_log_config._get_handler(
                self.django_log_config.DJANGO_LOGSTASH_HANDLER_LEVEL
            ),
            self.django_log_config.LOGSTASH_HANDLER_NAME: self.django_log_config._get_handler(
                LOG_LEVELS[logging.DEBUG]
            ),
        }
        self.assertEqual(settings_logging['handlers'], handlers)
        loggers = {
            self.django_log_config.DJANGO_LOGGER_NAME: {
                'handlers': [self.django_log_config.DJANGO_LOGSTASH_HANDLER_NAME, 'console'],
                'level': self.django_log_config.DJANGO_LOGGERS_LEVEL,
                'propagate': False,
            },
            self.django_log_config.APP_LOGSTASH_LOGGER_NAME: {
                'handlers': [self.django_log_config.LOGSTASH_HANDLER_NAME],
                'level': LOG_LEVELS[logging.DEBUG],
                'propagate': False,
            },
        }
        self.assertEqual(settings_logging['loggers'], loggers)

    def test_get_logger(self) -> None:
        LOGGER_NAME = 'test-name'
        logger = self.django_log_config.get_logger(LOGGER_NAME)
        self.assertEqual(logger.name, f'{self.django_log_config.APP_LOGSTASH_LOGGER_NAME}.{LOGGER_NAME}')

        logger = self.django_log_config.get_logger()
        self.assertEqual(logger.name, f'{self.django_log_config.APP_LOGSTASH_LOGGER_NAME}')
