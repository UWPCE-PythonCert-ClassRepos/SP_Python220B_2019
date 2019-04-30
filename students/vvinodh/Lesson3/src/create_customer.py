"""Creates Customers class in the database"""
# pylint: disable=W0614, W0401, C0103, R0903
import logging

from customer_model_schema import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Creates Customers class in the database')

DATABASE.create_tables([Customers])

DATABASE.close()
