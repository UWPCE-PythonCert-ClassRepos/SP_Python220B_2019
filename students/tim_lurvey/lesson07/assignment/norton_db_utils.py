"""this file contains database functions for creating and retrieving documents
from Norton's MongoDB database of products, customers, and rental data"""

#pylint: disable=logging-fstring-interpolation,line-too-long

import logging
import motor.motor_asyncio
from types import coroutine
from pymongo import MongoClient
from misc_utils import func_timer

# FILE_LOG_LEVEL = logging.NOTSET         # 0
# FILE_LOG_LEVEL = logging.DEBUG          # 10
# FILE_LOG_LEVEL = logging.INFO           # 20
FILE_LOG_LEVEL = logging.ERROR          # 50

logging.basicConfig(format="%(asctime)s "
                           "%(levelname)s "
                           "%(filename)s.%(funcName)s():%(lineno)d "
                           "> %(message)s")

logger = logging.getLogger(__name__)
if logger.getEffectiveLevel() > FILE_LOG_LEVEL:
    logger.setLevel(FILE_LOG_LEVEL)


class MongoDBConnection:
    """"MongoDB Connection
    must use 127.0.0.1 on windows
    pip install pymongo
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        logger.debug(f"Database connected at {self.connection.address}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug(f"Database closed at {self.connection.address}")
        self.connection.close()


class MongoDBConnectionAsync:
    """"MongoDB Connection
    must use 127.0.0.1 on windows
    pip install pymongo
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = motor.motor_asyncio.AsyncIOMotorClient(self.host, self.port)
        logger.debug(f"Database connected at {self.connection.address}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug(f"Database closed at {self.connection.address}")
        self.connection.close()

