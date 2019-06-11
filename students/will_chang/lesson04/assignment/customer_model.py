"""
Define the schema
"""

from peewee import *

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database

class Customer(BaseModel):
    """
    This class defines Customer, which maintains details of someone
    to help HP Norton's salesperson, accountant, and manager.
    """
    customer_id = CharField(primary_key = True, max_length = 30)
    name = CharField(max_length = 30)
    lastname = CharField(max_length = 30)
    home_address = CharField(max_length = 30)
    phone_number = CharField(max_length = 30)
    email_address = CharField(max_length = 30)
    status = BooleanField()
    credit_limit = IntegerField()
