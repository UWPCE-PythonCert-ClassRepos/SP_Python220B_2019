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
    """
    pass
