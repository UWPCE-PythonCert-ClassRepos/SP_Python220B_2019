'''
Customer model for HP Norton Furniture DB
'''
from peewee import *

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(Model):
    '''Base Model for DB classes.'''
    class Meta:
        '''Assign database for BaseModel.'''
        database = database

class Customer(BaseModel):
    '''
    This class defines a Customer of HP Norton Furniture
    and includes important customer information.
    '''
    customer_id = DecimalField(primary_key=True, max_digits=7)
    name = CharField(max_length=20)
    lastname = CharField(max_length=20)
    home_address = CharField(max_length=40)
    phone_number = DecimalField(max_digits=10)
    email_address = CharField(max_length=30)
    status = CharField(max_length=8)
    credit_limit = DecimalField(max_digits=8, decimal_places=2)
