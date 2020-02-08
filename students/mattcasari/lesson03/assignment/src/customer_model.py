"""
    Customer model for HP Norton database using Peewee ORM,
    sqlite and Python.

    Schema defined below
"""
#pylint: disable=unused-wildcard-import
#pylint: disable=wildcard-import
#pylint: disable=too-few-public-methods

from peewee import *


# Set up Database
DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    """ The database model for the base model class"""
    class Meta:
        """Meta class for peewee database"""
        database = DATABASE

class Customers(BaseModel):
    """
        This class defines the customer
    """
    customer_id = CharField(primary_key=True, max_length=10)
    name = CharField(max_length=30)
    last_name = CharField(max_length=30, null=True)
    home_address = CharField(max_length=300, null=True)
    phone_number = CharField(max_length=13, null=True)
    email_address = CharField(max_length=320, null=True) # Valid email length
    status = BooleanField(default=True)
    credit_limit = DecimalField(max_digits=9, decimal_places=2)
