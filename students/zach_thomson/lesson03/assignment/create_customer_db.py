# pylint: disable=W0614,W0401
'''
One off program to initialize and set up the Customer database as shown in the
video lesson/code
'''

import logging
from customer_db_model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('One off program to set up the customer database')

DATABASE.create_tables([Customer])

DATABASE.close()
