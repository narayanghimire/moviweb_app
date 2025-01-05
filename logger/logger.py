import logging
import logging.config
import os

# Ensure the logger and log directories exist
LOG_DIRECTORY = 'logger/log'
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

# Centralized logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'app.log'),
            'formatter': 'default',
            'level': 'DEBUG',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'INFO',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file', 'console'],
    },
}

def setup_logger(name: str):
    """
    Sets up a logger with the given name using the centralized configuration.
    """
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)
