"""
    Customer database schema model
"""

# pylint: disable=too-few-public-methods
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
# pylint: disable=unnecessary-pass
# pylint: disable=no-self-use


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
