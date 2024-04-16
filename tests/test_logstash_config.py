import logging
from unittest import TestCase

from easy_logstash.constants import LOGSTASH_NAMESPACE
from easy_logstash.handler import EasyLogstashHandler
from easy_logstash.logstash_config import EasyLogstashConfig
from tests.mixins import TestMixin


class EasyLogstashConfigTest(TestCase, TestMixin):

    def test_config(self) -> None:
        root_logstash_logger = logging.getLogger(f'{LOGSTASH_NAMESPACE}-{self.ELASTICSEARCH_INDEX}')
        self.assertEqual(root_logstash_logger.handlers, [])
        easy_logstash_config = EasyLogstashConfig(
            self.LOGSTASH_HOST, self.LOGSTASH_PORT, str(self.LOGSTASH_DATABASE_PATH), self.ELASTICSEARCH_INDEX
        )
        self.assertEqual(easy_logstash_config.app_name, self.ELASTICSEARCH_INDEX)
        self.assertEqual(len(root_logstash_logger.handlers), 1)
        handler: EasyLogstashHandler = root_logstash_logger.handlers[0]  # type: ignore
        self.assertTrue(isinstance(handler, EasyLogstashHandler))
        self.assertEqual(handler._elasticsearch_index, f'{LOGSTASH_NAMESPACE}-{self.ELASTICSEARCH_INDEX}')
        self.assertEqual(handler._host, self.LOGSTASH_HOST)
        self.assertEqual(handler._port, self.LOGSTASH_PORT)
        self.assertEqual(handler._transport_path, 'logstash_async.transport.TcpTransport')

        LOGGER_NAME = 'test-name'
        test_logger = easy_logstash_config.get_logger(LOGGER_NAME)
        self.assertEqual(test_logger.name, f'{LOGSTASH_NAMESPACE}-{self.ELASTICSEARCH_INDEX}.{LOGGER_NAME}')
        self.assertEqual(test_logger.parent, root_logstash_logger)

        LOGGER_NAME_2 = 'test-name-2.next'
        test_logger_2 = easy_logstash_config.get_logger(LOGGER_NAME_2)
        self.assertEqual(test_logger_2.name, f'{LOGSTASH_NAMESPACE}-{self.ELASTICSEARCH_INDEX}.{LOGGER_NAME_2}')
        self.assertEqual(test_logger_2.parent, root_logstash_logger)

        test_logger_3 = easy_logstash_config.get_logger()
        self.assertEqual(test_logger_3.name, f'{LOGSTASH_NAMESPACE}-{self.ELASTICSEARCH_INDEX}')
        self.assertEqual(test_logger_3, root_logstash_logger)
