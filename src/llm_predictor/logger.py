import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_filename='app.log'):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    os.makedirs('logs', exist_ok=True)
    log_path = os.path.join('logs', log_filename)

    file_handler = RotatingFileHandler(log_path, maxBytes=1_048_576, backupCount=5, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
