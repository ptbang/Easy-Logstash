import logging

from logstash_async.formatter import LogstashFormatter
from logstash_async.handler import AsynchronousLogstashHandler

from easy_logstash.constants import LOGSTASH_NAMESPACE


class EasyLogstashHandler(AsynchronousLogstashHandler):
    DEFAULT_LEVEL = logging.DEBUG

    def __init__(
        self,
        host,
        port,
        database_path,
        transport='logstash_async.transport.TcpTransport',
        ssl_enable=False,
        ssl_verify=True,
        keyfile=None,
        certfile=None,
        ca_certs=None,
        enable=True,
        event_ttl=None,
        encoding='utf-8',
        app_name='',
        **kwargs,
    ) -> None:
        self._elasticsearch_index = f'{LOGSTASH_NAMESPACE}-{app_name}' if app_name else LOGSTASH_NAMESPACE
        super().__init__(
            host,
            port,
            database_path,
            transport,
            ssl_enable,
            ssl_verify,
            keyfile,
            certfile,
            ca_certs,
            enable,
            event_ttl,
            encoding,
            **kwargs,
        )
        self._set_default_level()
        self._set_default_format()

    def _set_default_format(self) -> None:
        metadata = dict(elasticsearch_index=self._elasticsearch_index)
        formatter = LogstashFormatter(metadata=metadata)
        self.setFormatter(formatter)

    def _set_default_level(self) -> None:
        self.setLevel(self.DEFAULT_LEVEL)
