"""
customer database, to store required data for each customer
"""
from peewee import *

database = SqliteDatabase('customer.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class Basemodel(Model):
    class Meta:
        database = database

class Customer(Basemodel):
    """
    This class defines Customer, which maintains details of
    a customer
     """

    name = CharField(max_length=20)
    lastname = CharField(max_length=30)
    home_address = CharField(max_length=50)
    phone_number = IntegerField()
    email_address = CharField(max_length=40)
    status = BooleanField(default=True)
    credit_limit = DecimalField()
