"""Creates a customer database with peewee ORM, sqlite and python"""
# pylint: disable=unused-wildcard-import,wildcard-import,too-many-arguments,wrong-import-position
import logging
from customer_model import Customer, DB

logging.basicConfig(level=logging.INFO)

logging.info("Creating the Customer table")
DB.create_tables([Customer])
logging.info("Closing the customer database")
#DB.close()
