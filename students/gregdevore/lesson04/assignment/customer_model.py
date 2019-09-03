"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
from peewee import Model, CharField, BooleanField, DecimalField, SqliteDatabase
import logging

database = SqliteDatabase('customer.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(Model):
    class Meta:
        database = database

class Customer(BaseModel):
    """
        This class defines Customer, which maintains the details of a customer
        at HP Norton
    """
    
    id = CharField(primary_key = True, max_length = 5)
    firstname = CharField(max_length = 30)
    lastname = CharField(max_length = 30)
    address = CharField(max_length = 30)
    phone = CharField(max_length = 12) # Format is XXX-XXX-XXXX
    email = CharField(max_length = 30)
    status = BooleanField()
    credit_limit = DecimalField(max_digits = 7, decimal_places = 2)
