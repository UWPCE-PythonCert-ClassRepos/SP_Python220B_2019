"""
Defining the schema for the Customer model.
"""
# pylint: disable=W0614, W0401, C0103, R0903
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('customers.db')
logger.info('Created database customers.db')
database.connect()
logger.info('Connected to database')
database.execute_sql('PRAGMA foreign_keys = ON;')
logger.info('Setting up Models')

class BaseModel(Model):
    """Base for the customer class"""
    class Meta:
        """Sets database variable"""
        database = database

class Customer(BaseModel):
    """
        This class defines Customer and the attributes associated
        with a customer.
    """
    logger.info('Setting up Customer model attributes/columns')
    customer_id = CharField(primary_key=True, max_length=30)
    customer_name = CharField(max_length=20, null=True)
    customer_last_name = CharField(max_length=20, null=True)
    customer_address = CharField(max_length=50, null=True)
    customer_phone = CharField(max_length=10, null=True)
    customer_email = CharField(max_length=30, null=True)
    customer_status = BooleanField()
    customer_limit = FloatField(default=1000.00)
