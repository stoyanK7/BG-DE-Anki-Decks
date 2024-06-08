"""Universal logger for all scripts."""

import logging.config

config = {
    'version': 1,
    'formatters': {
        'simple': {'format': '[ %(levelname)s | %(module)20s ]: %(message)s'}
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {'root': {'level': 'INFO', 'handlers': ['stdout']}},
}

logging.config.dictConfig(config=config)

logger = logging.getLogger('universal_logger')
