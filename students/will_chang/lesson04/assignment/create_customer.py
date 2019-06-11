"""
Create customers.db database
"""

from customer_model import *

import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

from customer_model import *

LOGGER.info('Building the customers.db database.')

database.create_tables([
        Customer
    ])

database.close()
