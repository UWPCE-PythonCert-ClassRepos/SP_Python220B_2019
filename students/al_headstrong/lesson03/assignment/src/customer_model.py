"""
    Schema for customer database.
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
        This class defines Customer.
    """
    customer_id = CharField(primary_key=True, max_length=30)
    name = CharField(max_length=30)
    lastname = CharField(max_length=30)
    home_address = CharField(max_length=30, null=True)
    phone_number = CharField(max_length=30, null=True)
    email_address = CharField(max_length=30, null=True)
    status = CharField(max_length=30)
    credit_limit = IntegerField()
