#!/usr/bin/env python
"""
Customer model to generate and define the schema of customer.db
"""
from peewee import *

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(Model):
    """This class is the superclass for all models"""
    class Meta:
        '''Defining database'''
        database = database

class Customers(BaseModel):
    """
        This class defines the customers of HP Norton
    """
    customer_id = AutoField()
    first_name = CharField(max_length=30, null=False)
    last_name = CharField(max_length=30, null=False)
    home_address = CharField(max_length=100, null=False)
    phone_number = CharField(max_length=12, null=False)
    email_address = CharField(max_length=30, null=False, unique=True)
    is_active = DecimalField(max_digits=1, null=False) # 1 for active, 0 for inactive
    credit_limit = DecimalField(max_digits=12, decimal_places=2, null=False)
