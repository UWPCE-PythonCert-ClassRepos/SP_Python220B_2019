"""Creates the table for the customer model database"""

#pylint: disable=unused-wildcard-import
#pylint: disable=wildcard-import
#pylint: disable=undefined-variable

import logging
from customer_model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Build the classes from the model in the database.')

database.create_tables([Customer])

database.close()
