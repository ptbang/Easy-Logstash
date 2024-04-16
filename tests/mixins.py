import pathlib


class TestMixin:
    LOGSTASH_HOST = 'localhost'
    LOGSTASH_PORT = 5000
    LOGSTASH_DATABASE_PATH = pathlib.Path(__file__).parent / 'logstash.db'
    ELASTICSEARCH_INDEX = 'example-com-test'
