#!/usr/bin/env python3


"""
This script creates the base model for customer
"""

# pylint: disable= W0614, W0401, C0103, R0903

from peewee import *

data = SqliteDatabase('customers.db')
data.connect()
data.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    """
    Creates the base model class for initializing database
    """

    class Meta:
        """
        Meta class for database init
        """
        database = data


class Customer(BaseModel):
    """
    Class to create fields for customer model
    """
    customer_id = IntegerField(primary_key=True)
    customer_name = CharField(max_length=50)
    customer_last_name = CharField(max_length=30)
    customer_address = CharField(max_length=180, null=True)
    customer_phone_number = CharField(max_length=10)
    customer_email = CharField(max_length=30, null=True)
    customer_status = CharField(max_length=8)
    customer_credit_limit = DecimalField(decimal_places=2, default=0)
