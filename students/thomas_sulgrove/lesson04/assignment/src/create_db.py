"""
Create the DB
"""

import logging
from cust_schema import Customer, database

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Creating a DB')
database.create_tables([Customer])
database.close()
