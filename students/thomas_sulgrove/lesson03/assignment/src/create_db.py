"""
Create the DB
"""

import logging
from cust_schema import Customer, DATABASE

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Creating a DB')
DATABASE.create_tables([Customer])
DATABASE.close()
