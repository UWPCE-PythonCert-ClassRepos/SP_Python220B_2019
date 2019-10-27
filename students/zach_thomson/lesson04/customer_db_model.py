# pylint: disable=W0614, W0401, R0903
"""
Database model file for HP Norton Customer database
"""

from peewee import *

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    '''initializing class'''
    class Meta:
        '''initializing class'''
        database = DATABASE


class Customer(BaseModel):
    """
    Customer class that contain data about HP Norton customers
    """
    customer_id = IntegerField(primary_key=True)
    name = CharField(max_length=40)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=40)
    phone_number = CharField(max_length=10)
    email_address = CharField(max_length=40)
    status = BooleanField()
    credit_limit = DecimalField(max_digits=7, decimal_places=2)
