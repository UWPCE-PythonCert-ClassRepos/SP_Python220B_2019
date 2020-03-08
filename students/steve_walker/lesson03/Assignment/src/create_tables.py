"""









DO I NEED THIS IF I USE THE FAIL_SILENTLY OPTION FOR CREATING TABLES IN BASIC_OPS?










Creates the tables for the customer database.
"""

import logging
from peewee import *
from customer_model import Customer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SqliteDatabase("customers.db")
db.execute_sql('PRAGMA foreign_keys = ON;')
db.connect()

logger.info("Creating the Customer table in customers.db.")
db.create_tables([Customer])

db.close()
