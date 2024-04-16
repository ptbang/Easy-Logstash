import logging
from unittest import TestCase

from logstash_async.formatter import LogstashFormatter
from logstash_async.handler import AsynchronousLogstashHandler

from easy_logstash.constants import LOGSTASH_NAMESPACE
from easy_logstash.handler import EasyLogstashHandler
from tests.mixins import TestMixin


class EasyLogstashHandlerTest(TestCase, TestMixin):
    def test_create_instance(self):
        handler = EasyLogstashHandler(
            self.LOGSTASH_HOST,
            self.LOGSTASH_PORT,
            self.LOGSTASH_DATABASE_PATH,
            app_name=self.ELASTICSEARCH_INDEX,
        )
        self.assertTrue(isinstance(handler, AsynchronousLogstashHandler))
        self.assertEqual(handler._elasticsearch_index, f'{LOGSTASH_NAMESPACE}-{self.ELASTICSEARCH_INDEX}')
        self.assertEqual(handler._host, self.LOGSTASH_HOST)
        self.assertEqual(handler._port, self.LOGSTASH_PORT)
        self.assertEqual(handler._transport_path, 'logstash_async.transport.TcpTransport')
        self.assertEqual(handler.level, logging.DEBUG)
        self.assertTrue(isinstance(handler.formatter, LogstashFormatter))
        self.assertEqual(handler.formatter._metadata, {'elasticsearch_index': handler._elasticsearch_index})  # type: ignore
