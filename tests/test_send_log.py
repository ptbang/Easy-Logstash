import datetime
import logging
from unittest import TestCase

from easy_logstash.constants import LOGSTASH_NAMESPACE
from easy_logstash.logstash_config import EasyLogstashConfig
from tests.mixins import TestMixin


class SendLogTest(TestCase, TestMixin):
    def test_send_log(self) -> None:
        logstash_config = EasyLogstashConfig(
            self.LOGSTASH_HOST, self.LOGSTASH_PORT, str(self.LOGSTASH_DATABASE_PATH), self.ELASTICSEARCH_INDEX
        )
        LOGGER_NAME = 'test-name'
        MESSAGE = 'test-message'
        logger = logstash_config.get_logger(LOGGER_NAME)
        with self.assertLogs(logger.name, logging.INFO) as context:
            logger.info(MESSAGE)
            handler = logger.parent.handlers[0]  # type: ignore
            content = handler.formatter._format_to_dict(context.records[0])  # type: ignore
            record_created_at = datetime.datetime.strptime(content['@timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z')
            now = datetime.datetime.now(datetime.timezone.utc)
            self.assertTrue(now - record_created_at < datetime.timedelta(seconds=0.1))
            self.assertEqual(content['message'], MESSAGE)
            self.assertEqual(
                content['@metadata'], {'elasticsearch_index': f'{LOGSTASH_NAMESPACE}-{self.ELASTICSEARCH_INDEX}'}
            )
            self.assertTrue(isinstance(content['extra'], dict))
