# Stella Kim
# Assignment 4: Iterables, Iterators & Generators

"""Customer schema using Peewee ORM, SQLite and Python"""

import logging
from peewee import (Model, SqliteDatabase, IntegerField, CharField,
                    BooleanField, DecimalField)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

CUSTOMER_DB = SqliteDatabase('customers.db')
CUSTOMER_DB.connect()
CUSTOMER_DB.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    """Peewee base model"""
    class Meta:
        """Peewee meta class"""
        database = CUSTOMER_DB


class Customer(BaseModel):
    """Class to define customer information for HP Norton"""
    customer_id = IntegerField(primary_key=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    home_address = CharField(max_length=100)
    phone = CharField(max_length=10)
    email = CharField(max_length=50)
    status = BooleanField(default=True)
    credit_limit = DecimalField(max_digits=7, decimal_places=2)
