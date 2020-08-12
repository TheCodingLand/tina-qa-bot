
import logging
import logstash
import sys
import os

LOGLEVEL = os.getenv('LOGLEVEL')
if LOGLEVEL == None:
    LOGLEVEL="INFO"

def setup_custom_logger(name):
    #TODO: config with env
    host = 'elk_logstash'
    logger = logging.getLogger(name)
    logger.setLevel(LOGLEVEL)
    
    formatter = logging.Formatter('{ "class": "%(name)s", "level": "%(levelname)s", "message": "%(message)s" }')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    if os.getenv('ELK') == "enabled":
        logger.addHandler(logstash.LogstashHandler(host, 5959, version=1))
    return logger
