"""
    This file is called to initialize the database...
    A bit redundant at the moment since we aren't making a front end to this...
"""

import logging
import peewee as pw
from customer_model import Customer

# set up logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# init database
database = pw.SqliteDatabase('customer_database.db')
database.create_tables([Customer])
LOGGER.info('Database initialized.')
