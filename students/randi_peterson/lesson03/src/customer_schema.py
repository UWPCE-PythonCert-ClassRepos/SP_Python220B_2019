"""Defines the schema for the HP Norton customer database"""

import peewee

database = peewee.SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON')

class BaseModel(peewee.Model):
    """Set up database"""
    class Meta:
        database = database


class Customer(BaseModel):
    """Creates a customer with details about a customer"""
    customer_id = peewee.CharField(primary_key = True, max_length = 30)
    first_name = peewee.CharField(max_length = 30)
    last_name = peewee.CharField(max_length = 30)
    address = peewee.CharField(max_length = 100)
    phone = peewee.CharField(max_length = 30)
    email = peewee.CharField(max_length = 30)
    status = peewee.BooleanField()
    credit_limit = peewee.IntegerField()
