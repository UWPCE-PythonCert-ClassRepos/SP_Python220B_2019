"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
from peewee import Model, CharField, BooleanField, DecimalField, SqliteDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Here we define our data (the schema)')
logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('customer.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

logger.info('This means we can easily switch to a different database')
logger.info('Enable the Peewee magic! This base class does it all')

class BaseModel(Model):
    class Meta:
        database = database

logger.info('By inheritance only we keep our model (almost) technology neutral')

class Customer(BaseModel):
    """
        This class defines Customer, which maintains the details of a customer
        at HP Norton
    """
    logger.info('Note how we defined the class')
    logger.info('Specify the fields in our model, their lengths and if mandatory')
    logger.info('The customer ID must be a unique identifier for each customer')

    id = CharField(primary_key = True, max_length = 5)
    firstname = CharField(max_length = 30)
    lastname = CharField(max_length = 30)
    address = CharField(max_length = 30)
    phone = CharField(max_length = 12) # Format is XXX-XXX-XXXX
    email = CharField(max_length = 30)
    status = BooleanField()
    credit_limit = DecimalField(max_digits = 7, decimal_places = 2)
