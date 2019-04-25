"""Creates Customers class in the database"""

import logging

from customer_model_schema import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Creates Customers class in the database')

DATABASE.create_tables([Customers])

DATABASE.close()
