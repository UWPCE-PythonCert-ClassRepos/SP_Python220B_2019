'''Customer model for HP Norton database'''

# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name

from peewee import *

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreing_keys = ON;')

class BaseModel(Model):
    '''BaseModel class for sqlite'''
    class Meta:
        '''Meta class for sqlite'''
        database = database

class Customer(BaseModel):
    '''
    Customer class defines Customer, containing necessary customer information
    '''
    c_id = CharField(primary_key=True, max_length=3)
    c_firstname = CharField(max_length=15)
    c_lastname = CharField(max_length=20)
    c_home_address = CharField(max_length=40)
    c_phone_number = CharField(max_length=10)
    c_email_address = CharField(max_length=40)
    c_status = CharField(max_length=8)
    c_credit_limit = DecimalField(decimal_places=2)
