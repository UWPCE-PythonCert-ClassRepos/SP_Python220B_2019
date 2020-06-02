"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Here we define our data (the schema)')

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = database


class Identity(BaseModel):
    customer_id = CharField(max_length=6, primary_key=True)
    name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    credit_limit = DecimalField(max_digits=6)
    active = BooleanField()


class Contact(BaseModel):
    """
    This class Model establishes the Contact table, which contains all the information 
    """
    home_address = CharField(primary_key=True, max_length=75)
    email_address = CharField(max_length=50, null=False)
    phone_number = CharField(max_length=20)
    customer_id = ForeignKeyField(Identity, related_name='contact information for', null=False)
