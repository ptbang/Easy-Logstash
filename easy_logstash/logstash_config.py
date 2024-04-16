import logging

from easy_logstash.constants import LOGSTASH_NAMESPACE
from easy_logstash.handler import EasyLogstashHandler


class EasyLogstashConfig:
    def __init__(self, host: str, port: int, database_path: str, app_name: str = '', **kwargs) -> None:
        self.host = host
        self.port = port
        self.database_path = database_path
        self.app_name = app_name
        self.root_logger_name = f'{LOGSTASH_NAMESPACE}-{app_name}'
        self.kwargs = kwargs
        self.set_root_logger()

    def set_root_logger(self) -> None:
        """
        Sets the root logstash logger with the name `logstash-{elasticsearch_index}`.
        All earlier existent handlers will be removed and new logstash handlers is added to the new root logstash logger
        """
        logstash_root = logging.getLogger(self.root_logger_name)
        logstash_root.propagate = False
        logstash_root.setLevel(logging.DEBUG)
        for handler in logstash_root.handlers:
            logstash_root.removeHandler(handler)
        handler = EasyLogstashHandler(self.host, self.port, self.database_path, app_name=self.app_name, **self.kwargs)
        logstash_root.addHandler(handler)

    def get_logger(self, name: str | None = None) -> logging.Logger:
        """
        Returns new logger which will be descendant of root logstash logger
        by adding prefix `logstash-{elasticsearch_index}` to its name
        """
        name = f'.{name}' if name else ''
        return logging.getLogger(f'{self.root_logger_name}{name}')
