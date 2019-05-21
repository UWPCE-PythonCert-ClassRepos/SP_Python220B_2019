"""Creates a customer database with peewee ORM, sqlite and python"""

from customer_model import *
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Creating the Customer table")
db.create_tables([Customer])
logging.info("Closing the customer database")
db.close()


def before_request_handler():
    db.connect()


def after_request_handler():
    db.close()