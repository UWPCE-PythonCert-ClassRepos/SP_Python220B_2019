"""This program builds the Customers class in the database"""

import logging

from customer_model_schema import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('One off program to build the Customers class in the database')

DATABASE.create_tables([Customers])

DATABASE.close()
