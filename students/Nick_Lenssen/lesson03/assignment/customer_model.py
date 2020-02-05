"""Creates the database entry and character fields"""

#pylint: disable=unused-wildcard-import
#pylint: disable=wildcard-import
#pylint: disable=too-few-public-methods

import logging
from peewee import *

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class BaseModel(Model):
    """Peewee batabase interaction"""
    class Meta():
        """docstring"""
        database = DATABASE

class Customer(BaseModel):
    """Class will define a customer Horton wants to keep a record of"""
    LOGGER.info('Unique ID for a customer')
    cust_id = CharField(primary_key=True, max_length=30)
    LOGGER.info('First Name and Last Name of Customer')
    f_name = CharField(max_length=15)
    l_name = CharField(max_length=20)
    LOGGER.info('Home address of customer')
    cust_h_address = CharField(max_length=50)
    LOGGER.info('Phone number of customer')
    cust_phone_num = CharField(max_length=20)
    LOGGER.info('Email address of customer')
    cust_e_address = CharField(max_length=40)
    LOGGER.info('Customer status (Acitve or deactive)')
    cust_status = CharField(max_length=8)
    cust_credit_limit = DecimalField(decimal_places=2)
