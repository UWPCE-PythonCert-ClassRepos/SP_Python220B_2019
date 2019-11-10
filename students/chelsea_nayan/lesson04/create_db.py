'''Create customers'''

# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=undefined-variable

import logging
from customer_model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Logger is active!')

database.create_tables([Customer])
LOGGER.info('Intialized customer schema in database...')

database.close()
LOGGER.info('Database closed!')
