"""
    Schema is defined here
"""
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
    class Meta:
        database = database


class Customer(BaseModel):
    """
        This class defines Customer, which maintains details of customers
        and their info.
    """
    customer_id = IntegerField(primary_key=True, null=False)
    customer_name = CharField(max_length=30)
    customer_last_name = CharField(max_length=30)
    home_address = CharField(max_length=30)
    phone_number = CharField(max_length=30)
    email_address = CharField(max_length=30)
    status = CharField(max_length=30)
    credit_limit = IntegerField(default=200)
