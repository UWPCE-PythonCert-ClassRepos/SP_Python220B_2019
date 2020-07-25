"""
    Simple database examle with Peewee ORM, sqlite and Python
    Here we define the schema for the Customer
"""

from peewee import *

database = SqliteDatabase('customer.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    """Base Model"""
    class Meta:
        """Meta"""
        database = database


class Customer(BaseModel):
    """
        This class defines Customer, which maintains details of
        a rental store customer
    """
    customer_id = CharField(primary_key=True, max_length=30)
    name = CharField(max_length=40)
    lastname = CharField(max_length=40)
    home_address = CharField(max_length=60)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=60)
    status = BooleanField(default=True)
    credit_limit = DecimalField(max_digits=10, decimal_places=2)
