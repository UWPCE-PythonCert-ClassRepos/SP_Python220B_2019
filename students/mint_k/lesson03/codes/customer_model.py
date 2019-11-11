"""
    Database for customer model with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
from peewee import Model, CharField, BooleanField, DecimalField, SqliteDatabase

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Here we define our data (the schema)')
LOGGER.info('First name and connect to a database (sqlite here)')

LOGGER.info('The next 3 lines of code are the only database specific code')

#To create db in the same folder as the basic_operation.py file.
DATABASE = SqliteDatabase('./codes/customer.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

LOGGER.info('Enable the Peewee magic! This base class does it all')

class BaseModel(Model):
    """This is to setup Pewee and database"""
    class Meta:
        """this is to set up meta"""
        database = DATABASE

class Customer(BaseModel):
    """
        This class defines Customer, which maintains details of customer
        for whom we want to search detail customer information.
    """
    customer_id = CharField(primary_key=True, max_length=10)
    customer_name = CharField(max_length=40)
    lastname = CharField(max_length=40)
    home_address = CharField(max_length=40) #1234 ST SE, Seattle, WA 99082
    phone_number = CharField(max_length=12) #123-456-7894
    email_address = CharField(max_length=40)
    customer_status = BooleanField() #active or inactive
    credit_limit = DecimalField(max_digits=7, decimal_places=2)
