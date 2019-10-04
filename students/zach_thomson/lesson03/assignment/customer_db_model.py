"""
Database model file for HP Norton Customer database
"""

from peewee import *

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """
    Customer class that contain data about HP Norton customers
    """
    customer_id = AutoField() #maybe IntergerField(unique=TRUE)
    name = CharField(max_length=40)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=40)
    phone_number = CharField(min_length=10, max_length=10)
    email_address = CharField(max_length=40)
    status = BooleanField()
    credit_limit = DecimalField(max_digits=7, decimal_places=2)
