"""
    Customer model for HP Norton database using Peewee ORM, 
    sqlite and Python.

    Schema defined below
"""

from peewee import *

database = SqliteDatabase('customer.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database

class Person(BaseModel):
    """
        This class defines the customer
    """
    id = CharField(primary_key = True, max_length = 10)
    name = CharField(max_length = 30, null = False)
    last_name = CharField(max_length = 30, null = False)
    home_address = CharField(max_length = 300, null = False)
    phone_number = CharField(max_length = 13, null = False)
    email_address = CharField(max_length = 100, null = False)
    status = BooleanField(default = True)
    credit_limit = DecimalField(decimal_places = 2, auto_rounding = True
