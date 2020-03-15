"""
HP Norton database using Peewe ORM, sqlite3 and python.

Defines schema for basic customer data.
"""

# pylint: disable=W0614, W0401, C0103

from peewee import *

# Use Peewee to establish our customer_info database
db = SqliteDatabase('customers.db') # we could use a different RDBMS
db.connect()
db.execute_sql('PRAGMA foreign_keys = ON;') # unique to sqlite


class BaseModel(Model):
    """
    Peewee requires a BaseModel to be established as the parent class
    for all its DB classes.
    """

    class Meta: # pylint: disable=C0115, R0903
        database = db


class Customer(BaseModel):
    """
    This class defines the Customer database fields, which contains
    key info for employees to use.
    """

    customer_id = CharField(primary_key=True, max_length=30)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    home_address = CharField(max_length=100)
    phone_number = CharField(max_length=10) # How can we enforce an input format?
    email_address = CharField(max_length=50) # How can we enforce an input format?
    active_customer = BooleanField()
    credit_limit = DecimalField(max_digits=10, decimal_places=2, default=0)
