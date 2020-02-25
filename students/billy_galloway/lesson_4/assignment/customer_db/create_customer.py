"""
    Create database examle with Peewee ORM, sqlite and Python
"""

import logging
from customer_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


logger.info(f'Build customer.db database and create customer tables')

database.create_tables([Customer], safe=True)
database.close()
