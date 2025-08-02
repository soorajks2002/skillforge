Logging: From Beginner to Expert

https://claude.ai/chat/5038f520-663e-4ef8-9811-b9cb9e8280bb

## Table of Contentsq
1. [Introduction to Logging](#introduction-to-logging)
2. [Beginner: Basic Logging Concepts](#beginner-basic-logging-concepts)
3. [Intermediate: Configuration and Customization](#intermediate-configuration-and-customization)
4. [Advanced: Structured Logging and Integration](#advanced-structured-logging-and-integration)
5. [Expert: Production-Grade Logging](#expert-production-grade-logging)
6. [Deployment Scenarios](#deployment-scenarios)
7. [Best Practices](#best-practices)
8. [Common Pitfalls](#common-pitfalls)
9. [Additional Resources](#additional-resources)

## Introduction to Logging

Logging is a critical aspect of application development that provides visibility into application behavior, helps troubleshoot issues, and monitors application health. Python's built-in `logging` module offers a flexible framework for emitting log messages from Python programs.

### Why Use Logging Instead of print()?

- **Severity levels**: Distinguish between different types of messages
- **Output destinations**: Send logs to files, sockets, email, etc.
- **Formatting control**: Customize how messages appear
- **Configurability**: Enable/disable logging at runtime

## Beginner: Basic Logging Concepts

### Getting Started

To use the logging module, first import it:

```python
import logging
```

### Log Levels

The logging module provides five standard levels (in increasing order of severity):

| Level    | Numeric Value | When to Use                                     |
|----------|---------------|------------------------------------------------|
| DEBUG    | 10            | Detailed information for diagnosing problems    |
| INFO     | 20            | Confirmation that things are working as expected|
| WARNING  | 30            | Indication of potential issues (default level)  |
| ERROR    | 40            | Error that prevented something from working     |
| CRITICAL | 50            | Serious error that may prevent program execution|

### Basic Logging

Simple logging can be done with level-specific methods:

```python
# These will only show WARNING and above by default
logging.debug("This is a debug message")     # Won't show by default
logging.info("This is an info message")      # Won't show by default
logging.warning("This is a warning message") # Will show
logging.error("This is an error message")    # Will show
logging.critical("This is a critical message") # Will show
```

### Setting Log Level

To see all messages, set the log level:

```python
# Now all messages DEBUG and above will show
logging.basicConfig(level=logging.DEBUG)
```

### Logging to a File

To write logs to a file instead of the console:

```python
logging.basicConfig(
    filename='app.log',
    filemode='w',  # 'w' to overwrite, 'a' to append
    level=logging.DEBUG
)
```

### Basic Formatting

Control the format of log messages:

```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Intermediate: Configuration and Customization

### Loggers, Handlers, Formatters, and Filters

The logging system consists of four main components:

1. **Loggers**: Entry points into the logging system
2. **Handlers**: Determine where logs go (file, console, etc.)
3. **Formatters**: Control how log records are converted to text
4. **Filters**: Provide additional control over which logs are output

### Creating a Logger

Instead of using the root logger, create your own named logger:

```python
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)

# Now use logger instead of logging
logger.debug("This is a debug message")
```

### Adding Handlers

Handlers send log records to their destinations:

```python
# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# File handler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
```

### Custom Formatters

Create custom formats for different handlers:

```python
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)
```

### Using Configuration Files

For larger applications, configuration files are more maintainable:

```python
import logging.config

# Using a dictionary config
logging_config = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': 'app.log',
            'mode': 'a',
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

logging.config.dictConfig(logging_config)
```

Or use a file:

```python
logging.config.fileConfig('logging.conf')
```

### Using Logger Hierarchies

Loggers are organized in a hierarchy based on their names:

```python
logger_main = logging.getLogger('app')
logger_api = logging.getLogger('app.api')
logger_db = logging.getLogger('app.database')

# Messages to logger_api and logger_db will propagate to logger_main
```

## Advanced: Structured Logging and Integration

### Contextual Information with LogRecord Attributes

Enrich logs with contextual data:

```python
def process_request(request_id, user_id):
    logger = logging.getLogger('app.api')
    logger = logging.LoggerAdapter(logger, {'request_id': request_id, 'user_id': user_id})
    logger.info('Processing request')
```

### Structured Logging with JSON

For better integration with log management systems, use JSON formatting:

```python
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'name': record.name,
            'message': record.getMessage(),
        }
        # Add extra attributes
        for key, value in record.__dict__.items():
            if key not in ('args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
                           'funcName', 'id', 'levelname', 'levelno', 'lineno', 'module',
                           'msecs', 'message', 'msg', 'name', 'pathname', 'process',
                           'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName'):
                log_record[key] = value
        
        return json.dumps(log_record)
```

### Third-party Libraries for Structured Logging

Consider using specialized libraries:

- **structlog**: Adds structured logging to Python
- **python-json-logger**: JSON formatter for Python's logging module

```python
# Using structlog
import structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

log = structlog.get_logger()
log.info("User logged in", user_id=123, session_id="abc456")
```

### Integration with Web Frameworks

#### Flask Integration

```python
from flask import Flask, request, g
import logging
import uuid

app = Flask(__name__)

@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())
    
class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(g, 'request_id', 'no_request_id')
        return True

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s'
))
handler.addFilter(RequestIdFilter())
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
    app.logger.info('Index page requested')
    return 'Hello, World!'
```

#### Django Integration

Django has built-in logging configuration in settings.py:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'myapp': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Expert: Production-Grade Logging

### Rotating File Handlers

Prevent log files from growing too large:

```python
handler = logging.handlers.RotatingFileHandler(
    'app.log',
    maxBytes=10485760,  # 10MB
    backupCount=5        # Keep 5 backup files
)
```

### Time-Based Rotation

Rotate logs based on time intervals:

```python
handler = logging.handlers.TimedRotatingFileHandler(
    'app.log',
    when='midnight',     # Rotate at midnight
    interval=1,          # Once per day
    backupCount=7        # Keep a week's worth of logs
)
```

### Asynchronous Logging

For high-performance applications, use asynchronous logging:

```python
import logging
import threading
import queue

class AsyncHandler(logging.Handler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._process_logs)
        self.thread.daemon = True
        self.thread.start()
        
    def emit(self, record):
        self.queue.put(record)
        
    def _process_logs(self):
        while True:
            record = self.queue.get()
            self.handler.emit(record)
            self.queue.task_done()
```

### Log Aggregation and Centralized Logging

#### Sending Logs to Syslog

```python
handler = logging.handlers.SysLogHandler(
    address=('syslog-server.example.com', 514),
    facility=logging.handlers.SysLogHandler.LOG_USER
)
```

#### HTTP Handler for Log Management Systems

```python
class HTTPHandler(logging.Handler):
    def __init__(self, url, auth_token):
        super().__init__()
        self.url = url
        self.auth_token = auth_token
        
    def emit(self, record):
        import requests
        
        log_entry = self.format(record)
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        try:
            requests.post(self.url, json={'message': log_entry}, headers=headers)
        except Exception:
            self.handleError(record)
```

### Performance Optimization

Minimize logging overhead:

```python
# Check log level before formatting expensive messages
if logger.isEnabledFor(logging.DEBUG):
    logger.debug(f"Complex calculation result: {expensive_function()}")
```

### Robust Error Handling

Make sure logging doesn't break your application:

```python
class RobustFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        try:
            super().__init__(filename, mode, encoding, delay)
        except Exception as e:
            # Fall back to stderr
            self.stream = sys.stderr
            print(f"Failed to open log file: {e}", file=sys.stderr)
    
    def emit(self, record):
        try:
            super().emit(record)
        except Exception as e:
            # If logging fails, print to stderr
            print(f"Failed to log: {e}", file=sys.stderr)
```

## Deployment Scenarios

### Local Development Environment

For local development, prioritize readability and debugging:

```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Console output
    ]
)
```

### Testing Environment

For automated testing, configure logging to help debug test failures:

```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test.log'),
        logging.StreamHandler()
    ]
)
```

### Staging/QA Environment

In staging, mimic production settings but with more detail:

```python
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - [%(process)d:%(thread)d] - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detailed',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'app.log',
            'maxBytes': 10485760,
            'backupCount': 3,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        }
    }
})
```

### Production Environment

In production, focus on efficiency, security, and integration:

```python
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'json': {
            '()': 'json_log_formatter.JSONFormatter',
        },
    },
    'handlers': {
        'syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'level': 'WARNING',
            'formatter': 'json',
            'address': '/dev/log',
            'facility': 'local0',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'json',
            'filename': '/var/log/app/app.log',
            'when': 'midnight',
            'backupCount': 14,
        }
    },
    'loggers': {
        '': {
            'handlers': ['syslog', 'file'],
            'level': 'INFO',
        }
    }
})
```

### Containerized Environments (Docker)

For containerized applications, write logs to stdout/stderr:

```python
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'fmt': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'json',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
})
```

### Serverless Environment (AWS Lambda)

For Lambda functions, log to CloudWatch:

```python
import logging

# Lambda automatically captures logs sent to stdout/stderr
logger = logging.getLogger('lambda_function')
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('Lambda invoked', extra={
        'request_id': context.aws_request_id,
        'event_type': event.get('type')
    })
    # Function code...
```

### Cloud-native Applications (Kubernetes)

For Kubernetes applications, use structured logging:

```python
import json
import logging
import sys

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'time': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
        }
        
        # Add extra fields
        for key, value in getattr(record, 'extra_fields', {}).items():
            log_data[key] = value
            
        # Add exception info if available
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
            
        return json.dumps(log_data)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

## Best Practices

### Security Considerations

1. **Sanitize sensitive data**: Never log passwords, tokens, or personal identifiable information (PII)
   ```python
   def sanitize_user_data(user_dict):
       sanitized = user_dict.copy()
       for key in ['password', 'credit_card', 'ssn']:
           if key in sanitized:
               sanitized[key] = '********'
       return sanitized
       
   logger.info(f"User data: {sanitize_user_data(user)}")
   ```

2. **Log access control**: Secure log files with appropriate permissions
3. **Validate and sanitize log inputs**: Prevent log injection attacks

### Performance Best Practices

1. **Use lazy evaluation**: Only construct complex log messages if needed
2. **Benchmark logging overhead**: Measure impact on application performance
3. **Rate limiting**: Consider implementing rate limiting for high-volume logs

### Structure and Organization

1. **Consistent naming**: Use a consistent naming convention for loggers
2. **Appropriate log levels**: Use the correct level for each message
3. **Descriptive messages**: Make log messages clear and actionable

### Monitoring and Alerting

1. **Set up alerts**: Configure alerts for ERROR and CRITICAL messages
2. **Implement health checks**: Use logging to monitor application health
3. **Establish baselines**: Understand normal log volume and patterns

## Common Pitfalls

1. **Configuration order issues**: `basicConfig()` has no effect after handlers are configured
2. **Propagation confusion**: Logger hierarchy can lead to duplicate messages
3. **Resource leaks**: Failing to close file handlers
4. **Missing context**: Not including enough information to diagnose issues
5. **Overwhelming volume**: Logging too much, making important messages hard to find
6. **Performance impact**: Excessive logging slowing down the application
7. **Format inconsistency**: Using different formats across the application

## Additional Resources

### Standard Library Documentation
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [Logging Module Documentation](https://docs.python.org/3/library/logging.html)

### Third-Party Packages
- [structlog](https://www.structlog.org/en/stable/) - Structured logging for Python
- [python-json-logger](https://github.com/madzak/python-json-logger) - JSON formatter for Python logging
- [loguru](https://github.com/Delgan/loguru) - Python logging made simple

### Books and Articles
- "Python Logging: The Ultimate Guide" by Real Python
- "Effective Logging Practices" by Python Software Foundation
- "High-Performance Python Logging" by Python Weekly