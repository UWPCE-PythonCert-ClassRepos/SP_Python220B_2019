"""Creates a customer database with peewee ORM, sqlite and python"""

from customer_model import *
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Creating the Customer table")
DB.create_tables([Customer])
logging.info("Closing the customer database")
DB.close()


def before_request_handler():
    DB.connect()


def after_request_handler():
    DB.close()