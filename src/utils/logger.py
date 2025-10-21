import logging
import os

LOG_FILE = "app.log"

def setup_logger():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w'):
            pass

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message):
    logging.error(message)

def log_debug(message):
    logging.debug(message)