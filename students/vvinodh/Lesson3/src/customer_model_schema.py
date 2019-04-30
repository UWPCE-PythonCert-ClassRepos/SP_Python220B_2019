"""
    This file defines the schema of the data stored
    in the database
"""
# pylint: disable=W0614, W0401, C0103, R0903
from peewee import *

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    """This class establishes the base model"""
    class Meta:
        """This class establishes the database meta"""
        database = DATABASE

class Customers(BaseModel):
    """
        This class defines Customer, which maintains all information,
        of someone for whom we want to research
    """

    customer_id = CharField(primary_key=True, max_length=30)
    name = CharField(max_length=40)
    lastname = CharField(max_length=20, null=True)
    home_address = CharField(max_length=20, null=True)
    phone_number = CharField(max_length=10, null=True)
    email_address = CharField(max_length=20, null=True)
    status = CharField(max_length=20, null=True)
    credit_limit = DecimalField(max_digits=20, decimal_places=2)
