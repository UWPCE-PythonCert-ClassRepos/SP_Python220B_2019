from customer_schema import *
import logging

logging.basicConfig(level = logging.INFO)
LOGGER = logging.getLogger(__name__)

database.create_tables([Customer])
LOGGER.info('Created customers.db database')
database.close()