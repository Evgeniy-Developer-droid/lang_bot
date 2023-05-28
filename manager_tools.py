import logging
import os
from django.core.cache import cache


def markdown_filter(message):
    symbols = ['_', '*', '[', ']', '(', ')', '~', '`', 
               '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for symbol in symbols:
        message = message.replace(symbol, f'\{symbol}')
    return message

# This function increase value by one
def incrKey(key, value, timeout=None):
    return cache.incr(key, delta=value)


# This function set value
def setKey(key, value, timeout=None):
    return cache.set(key, value, timeout=timeout)


# This function set value if key exist then give error
def addKey(key, value, timeout=None):
    return cache.add(key, value, timeout=timeout)


# this function get value by key
def getKey(key):
    return cache.get(key)


# this function delete value by key
def deleteKey(key):
    return cache.delete(key)


# this function delete value by pattern
def getAllKey(pattern):
    return cache.keys(pattern)


def logs_autoclear():
    try:
        sz = os.path.getsize("logs.log")
        if int(sz) > 1024 * 1024 * 10: # 10 MB
            os.remove("logs.log")
    except FileNotFoundError:
        pass


class Logger:
    
    def __init__(self, name) -> None:
        file = 'logs.log'
        logging.basicConfig(
            filename=file,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filemode='a'
        )
        self.logger = logging.getLogger(name=name)
        self.logger.setLevel(logging.DEBUG)
    
    def get_logger(self):
        return self.logger