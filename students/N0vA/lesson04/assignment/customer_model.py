"""
Module for the customer model.  Creates base model and customer class.
"""

# pylint:disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Connecting to database....')

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

logger.info('Connected to Customers database.')

class BaseModel(Model):
    """Base mmodel class for our database."""

    class Meta:
        """Meta class for database."""
        database = database

class Customer(BaseModel):
    """Creates class to store customer data for our database."""

    logger.info('Create customer class to store customer information for database.')
    logger.info('Specify fields for Customer class')
    logger.info('customer_id will be primary key for the Customer class.')

    customer_id = IntegerField(primary_key=True)
    first_name = CharField(max_length=30, null=False)
    last_name = CharField(max_length=50, null=False)
    home_address = CharField(max_length=75, null=False)
    phone_number = CharField(max_length=15, null=False)
    email_address = CharField(max_length=50, null=False)
    credit_limit = DecimalField(max_digits=10, decimal_places=2)
    active_status = BooleanField(default=False, null=False) # True for active customers

    logger.info('Customer class fields created.')
