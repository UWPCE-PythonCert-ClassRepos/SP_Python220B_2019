"""
    Database for Assignment 3 with Peewee ORM, sqlite and Python
    Here we define the schema
"""
# pylint Disable=too-few-public-methods, wildcard-import,
#                unused-wildcard-import, invalid-name

from peewee import *

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    '''BaseModel class for sqlite database init'''
    class Meta:
        '''Meta class for sqlite database init'''
        database = database


class Customer(BaseModel):
    '''
        This class defines Customer, which contains customer data.
    '''
    customer_id = CharField(primary_key=True, max_length=10)
    first_name = CharField(max_length=15)
    last_name = CharField(max_length=15)
    home_address = CharField(max_length=40, null=True)
    phone_number = IntegerField(null=True)
    email_address = CharField(max_length=40, null=True)
    activity_status = BooleanField()
    credit_limit = DecimalField(max_digits=7, decimal_places=2, null=True)
