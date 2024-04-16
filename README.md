# Easy Logstash

Easy Logstash is a python package that allows you to use logstash logging
in your applications in very simple manner.

Because of using [Python logstash async](https://github.com/eht16/python-logstash-async/tree/49635e1fdac463329196f44693735070c5275231)
on the background, you can read more about the python logstash async at the link above.

## Installation
 Just `pip install easy-logstash`

## Usage
Assuming that your application is named `example-com` and the environment is `test`,
and you may want to save all your logs of this application
into elasticsearch index named `logstash-example-com-test`.

There are a few code examples:

```python
# file log_config.py
from easy_logstash import EasyLogstashConfig

log_config = EasyLogstashConfig(
    LOGSTASH_HOST, LOGSTASH_PORT, LOGSTASH_DATABASE_PATH, 'example-com-test'
)


# file foo.py
from log_config import log_config

logger = log_config.get_logger(__name__)
logger.warning('Some things look strangely ...')
```

It's very simple, right?

Now, take a look at the situation when you use only the package `python-logstash-async`
to do the same thing without `easy-logstash`
for better understanding what `easy-logstash` does.

```python
# file log_config.py should be involved while application is starting
import logging
from logstash_async.formatter import LogstashFormatter
from logstash_async.handler import AsynchronousLogstashHandler

# create the application root logger with logstash
root_logger = logging.getLogger('logstash-example-com-test')
root_logger.propagate = False
root_logger.setLevel(logging.DEBUG)

# create the handler and formatter
handler = AsynchronousLogstashHandler(LOGSTASH_HOST, LOGSTASH_PORT, LOGSTASH_DATABASE_PATH)
formatter = LogstashFormatter(metadata={'elasticsearch_index': 'logstash-example-com-test'})
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

# add handler to the application root logger
root_logger.addHandler(handler)


# create your log in your file foo.py
logger = logging.getLogger(f'logstash-example-com-test.{__name__}')
logger.warning('Some things look strangely ...')
```

### Django
You can also configure the constant LOGGING in your `setting.py` file in a very simple way.

```python
# setting.py
...
from easy_logstash import DjangoLogstashConfig

LOGGING_CONFIG = DjangoLogstashConfig(
    LOGSTASH_HOST, LOGSTASH_PORT, LOGSTASH_DATABASE_PATH, 'example-com-test'
)
LOGGING = LOGGING_CONFIG.get_dict_config()
...

# foo.py
from django.conf import settings

logger = settings.LOGGING_CONFIG.get_logger(__name__)
logger.warning('Some things look strangely ...')
```

## Logstash pipeline configuration
For example, the logstash pipeline configuration would look like this:

```
input {
	beats {
		port => 5044
	}

	tcp {
		port => 50000
	}
}

## Add your filters / logstash plugins configuration here
filter {
  json {
    source => "message"
    #add_field => {"log_time" => " %{@timestamp}"}
  }
}

output {
	elasticsearch {
		hosts => "elasticsearch:9200"
		user => "logstash_internal"
		password => "strong_password"
		index => "%{[@metadata][elasticsearch_index]}"
	}
}
```


*That's all. Enjoy coding!*
