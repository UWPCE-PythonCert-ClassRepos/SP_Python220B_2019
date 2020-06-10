"""
    Customer database schema model
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
