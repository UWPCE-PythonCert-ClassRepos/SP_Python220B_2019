""" This module defines a customer model and database that can be used at
    HP Norton.
"""
from peewee import Model, AutoField, CharField, BooleanField, DecimalField
from peewee import SqliteDatabase


# create an instance of a sqlite database
database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    """ This is a base model """
    class Meta:
        """ This is a Meta model """
        database = database

class Customer(BaseModel):
    """ This class defines  all the details related to the customer. """
    customer_id = AutoField() # Auto-incrementing primary key.
    name = CharField(max_length=50)
    lastname = CharField(max_length=30)
    home_address = CharField(max_length=300)
    phone_number = CharField()
    email_address = CharField()
    status = BooleanField(default=False)
    credit_limit = DecimalField(max_digits=7, decimal_places=2, default=0)

# create the tables based on the modules we built.
# database.create_tables([Customer])
