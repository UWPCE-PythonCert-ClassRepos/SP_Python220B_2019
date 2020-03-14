'''Creates the database and elements for a customer class'''

# pylint disabled: R0903

from peewee import Model, SqliteDatabase, CharField, DecimalField

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    '''Database model setup'''
    class Meta:
        '''Meta class for database'''
        database = DATABASE

class Customer(BaseModel):
    '''Defines a customer's attributes'''
    cust_id = CharField(primary_key=True, max_length=5)
    f_name = CharField(max_length=20)
    l_name = CharField(max_length=20)
    address = CharField(max_length=20)
    phone = CharField(max_length=20)
    email = CharField(max_length=20)
    status = CharField(max_length=8)
    credit = DecimalField(decimal_places=2)
