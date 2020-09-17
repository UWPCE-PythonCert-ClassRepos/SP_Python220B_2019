#!/usr/env/bin python
""" Documentation for {file} 
This file contains the database models for storing
customer data.""".format(file=__file__)

from peewee import *

database = SqliteDatabase('personjob.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    """Base class for establishing database"""

    class Meta:
        """This is a mystery to me"""
        database = database


class Customer(BaseModel):
    """This class holds all the definitions for a customer entry"""
    customer_id = CharField(primary_key=True, max_length=10)
    name = CharField(max_length=20, required=True)
    name_last = CharField(max_length=20, required=True)
    address = CharField(max_length=200, required=True)
    phone = CharField(max_length=10, required=True)
    email = CharField(max_length=40, required=True)
    active = BooleanField(default=False)
    credit_limit = DecimalField(max_digits=8, decimal_places=2, required=True)
