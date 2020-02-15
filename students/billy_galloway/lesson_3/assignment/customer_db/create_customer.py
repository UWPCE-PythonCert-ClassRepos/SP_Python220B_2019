"""
    Create database examle with Peewee ORM, sqlite and Python
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .customer_model import Customer

logger.info('Build classes from the model in the database')

database.create_tables([
        Customer
    ])

database.close()