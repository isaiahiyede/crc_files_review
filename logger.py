import time
import logging
import logging.handlers
import os

def iLog(message):
    path = os.getcwd()+"/"+"logs"+"/"+"review.logs"
    log_handler = logging.handlers.TimedRotatingFileHandler(path, when="h",  interval=12, backupCount=1)
    formatter = logging.Formatter("%(asctime)s %(message)s")
    formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        logger.handlers = []
    logger.addHandler(log_handler)
    logging.info(message)
    return True