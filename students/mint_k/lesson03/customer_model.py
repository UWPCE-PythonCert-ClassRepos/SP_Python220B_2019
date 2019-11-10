"""
    Database for customer model with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Here we define our data (the schema)')
LOGGER.info('First name and connect to a database (sqlite here)')

LOGGER.info('The next 3 lines of code are the only database specific code')

DATABASE = SqliteDatabase('customer.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

LOGGER.info('Enable the Peewee magic! This base class does it all')

class BaseModel(Model):
    """This is to setup Pewee and database"""
    class Meta:
        database = DATABASE

class Customer(BaseModel):
    """
        This class defines Customer, which maintains details of customer
        for whom we want to search detail customer information.
    """
    customer_id = AutoField(primary_key=True, max_length=5)
    customer_name = CharField(max_length=40)
    lastname = CharField(max_length=40)
    home_address = CharField(max_length=40) #1234 ST SE, Seattle, WA 99082
    phone_number = CharField(max_length=12) #123-456-7894
    email_address = CharField(max_length=40)
    customer_status = BooleanField(default=None) #active or inactive
    credit_limit = FloatField()
