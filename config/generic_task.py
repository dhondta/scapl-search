import os


GENERIC_TASK_LOG_LEVEL = 0
GENERIC_TASK_CONFIG = {
#    'PROXY_FILE': os.path.join(os.path.dirname(__file__), 'proxy_settings'),
    'LOG_LEVEL_MAPPING': {
        0: 40,  # logging.ERROR
        1: 30,  # logging.WARNING
        2: 20,  # logging.INFO
        3: 10,  # logging.DEBUG
    },
}
