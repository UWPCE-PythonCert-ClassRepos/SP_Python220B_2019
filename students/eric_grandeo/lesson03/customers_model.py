"""
Create Customers database
"""

from peewee import *

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database


class Customers(BaseModel):
    customer_id = CharField(primary_key = True, max_length = 5)
    name = CharField(max_length = 30)
    lastname = CharField(max_length = 30)
    home_address = CharField(max_length = 50)
    phone_number = CharField(max_length = 10)
    email_address = CharField(max_length = 30)
    status = BooleanField()
    credit_limit = DecimalField(max_digits = 7, decimal_places = 2)
    
'''
remove this when added to basic_operations
database.create_tables([Customers])
database.close()
'''    
