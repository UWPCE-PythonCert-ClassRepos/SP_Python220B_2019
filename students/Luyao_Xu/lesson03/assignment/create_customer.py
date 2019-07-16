"""
    Create database example with Peewee ORM, sqlite and Python
"""

from customer_model import DATABASE, Customer

import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('One off program to build the classes from the model '
            'in the database')

DATABASE.create_tables([Customer])
DATABASE.close()
