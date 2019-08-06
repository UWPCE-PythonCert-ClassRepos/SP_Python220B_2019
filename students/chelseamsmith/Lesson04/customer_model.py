# pylint: disable=W0401, W0614, R0903
"""Customer Model definition file"""
from peewee import *

DB = SqliteDatabase(None)

class Customer(Model):
    """defines fields for Customer model"""
    customer_id = IntegerField(primary_key=True)
    name = CharField()
    last_name = CharField()
    home_address = CharField()
    phone_number = CharField()
    email_address = CharField()
    status = BooleanField()
    credit_limit = IntegerField()

    class Meta:
        """define the database being used"""
        database = DB
