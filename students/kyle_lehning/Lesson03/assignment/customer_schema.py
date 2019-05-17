#!/usr/bin/env python3
"""
Schema for defining a customer for HP Norton Furniture
"""
from peewee import *

DB = SqliteDatabase('customers.db')  # Set name of SqliteDatabase
DB.connect()  # Connect to the database
DB.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only. See part 2 video


class BaseModel(Model):
    """
    Base class that establishes connection to database
    """
    class Meta:
        """Meta class provides info passed on to each implementation of BaseModel"""
        database = DB


class Customer(BaseModel):
    """
    This class defines the details of a customer
    """
    customer_id = CharField(primary_key=True, max_length=7)
    name = CharField(max_length=50)
    lastname = CharField(max_length=50)
    home_address = CharField(max_length=100)
    phone_number = CharField(max_length=15)
    email_address = CharField(max_length=254)
    status = BooleanField()
    credit_limit = DecimalField(decimal_places=2)

