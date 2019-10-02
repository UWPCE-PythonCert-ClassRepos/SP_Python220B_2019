"""
    Definition of the customer model that is needed for the HP Norton database.
    As the project grows in scope we can expand the models (tables) needed for the database.
"""

from peewee import *
import logging

database = SqliteDatabase('customer_database.db')


class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """
        Defines the customer table for the database.
        Customer ID will be used as the primary key.

        Fields
            -Customer ID (primary key)
            -Name
            -Last name
            -Home address
            -Phone number
            -Email address
            -Status (active or inactive)
            -Credit limit
    """
    customer_id = CharField(primary_key=True, max_length=30)
    name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField()
    phone_number = CharField(max_length=10)
    email_address = CharField()
    status = CharField(null=False)
    credit_limit = CharField(null=False)

database.create_tables([Customer])
