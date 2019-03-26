from customer_model_schema import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the Customers class in the database')

database.create_tables([Customers])

database.close()