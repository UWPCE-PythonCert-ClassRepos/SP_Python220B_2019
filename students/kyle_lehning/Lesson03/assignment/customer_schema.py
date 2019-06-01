#!/usr/bin/env python3
"""
Schema for defining a customer for HP Norton Furniture
"""
import peewee

DB = peewee.SqliteDatabase('customers.db')  # Set name of SqliteDatabase
DB.connect()  # Connect to the database
DB.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only. See part 2 video


class BaseModel(peewee.Model):
    """
    Base class that establishes connection to database
    """
    class Meta:  # pylint: disable=R0903
        """Meta class provides info passed on to each implementation of BaseModel"""
        database = DB


class Customer(BaseModel):
    """
    This class defines the details of a customer
    """
    customer_id = peewee.CharField(primary_key=True, max_length=7)
    name = peewee.CharField(max_length=50)
    lastname = peewee.CharField(max_length=50)
    home_address = peewee.CharField(max_length=100)
    phone_number = peewee.CharField(max_length=15)
    email_address = peewee.CharField(max_length=254)
    status = peewee.BooleanField()
    credit_limit = peewee.DecimalField(decimal_places=2)
