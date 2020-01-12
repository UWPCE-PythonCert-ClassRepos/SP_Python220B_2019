"""
    Schema for customer database.
"""

from peewee import *

database = SqliteDatabase('customer.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """
        This class defines Customer.
    """
    customer_id = CharField(primary_key=True, max_length=15)
    name = CharField(max_length=15)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=40, null=True)
    phone_number = CharField(max_length=15, null=True)
    email_address = CharField(max_length=40, null=True)
    status = CharField(max_length=15, null=False)
    credit_limit = DecimalField(max_digits=7, decimal_places=2, null=False)
