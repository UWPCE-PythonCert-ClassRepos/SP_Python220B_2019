"""
    Schema for customer database.
"""
# pylint: disable=unused-import,too-few-public-methods, unused-wildcard-import, wildcard-import

from peewee import *

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    """
        Class inheriting from Model, adding Meta
    """
    class Meta:
        """
            Class assigning DATABASE to class attribute DATABASE.
        """
        database = DATABASE


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
