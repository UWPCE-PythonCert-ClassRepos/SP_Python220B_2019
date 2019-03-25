from personjob_model import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from customer_model_schema import *

logger.info('One off program to build the customer class in the database')

database.create_tables([Customer])

database.close()