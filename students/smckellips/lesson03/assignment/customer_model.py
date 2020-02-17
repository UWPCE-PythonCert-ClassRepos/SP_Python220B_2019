# pylint: disable=R0903,W0401,W0614
"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.debug('Connecting to db.')
DB = SqliteDatabase('customer.db')
DB.connect()
DB.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only


class BaseModel(Model):
    """
        Peewee BaseModel class.
    """
    class Meta:
        """Peewee meta class.  Assignes db."""
        database = DB


class Customer(BaseModel):
    """
        This class defines Customer, which maintains details of HP Norton's
        customers.
    """
    customer_id = CharField(primary_key=True, max_length=30)
    name = CharField(max_length=50)
    lastname = CharField(max_length=50)
    home_address = CharField(max_length=50)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=50)
    status = BooleanField()
    credit_limit = DecimalField(max_digits=7, decimal_places=2)


LOGGER.debug('Creating Customer Table.')
DB.create_tables([Customer])
DB.close()
