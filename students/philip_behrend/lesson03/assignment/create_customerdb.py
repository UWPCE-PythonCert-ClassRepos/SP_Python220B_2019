"""
Create customer database
"""

from customer_model import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One run program to build the classes from the model in the database')

db.create_tables([
        Customer
    ])

db.close()
