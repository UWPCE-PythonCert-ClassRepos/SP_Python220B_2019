#!/usr/bin/env python3
"""Create a customer model and database that can be used at HP Norton. """

import logging
from peewee import SqliteDatabase, Model,\
    CharField, BooleanField,\
    IntegerField, AutoField #, DecimalField

# set up logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# set up database
DB = SqliteDatabase('customers.db')
DB.connect()
DB.execute_sql('PRAGMA foreign_keys = ON;')
LOGGER.info("connected to database.")

class BaseModel(Model):
    """ Base Model Class"""
    class Meta:
        """ Meta Model Class"""
        database = DB

class Customer(BaseModel):
    """Creates class that defines all the customer information required"""
    LOGGER.info("create customer class to store details in database")

    customer_id = AutoField()
    firstname = CharField(max_length=30, null=False)
    lastname = CharField(max_length=30, null=False)
    home_address = CharField(max_length=200, null=False)
    phone_number = IntegerField()
    email_address = CharField(max_length=50, null=False)
    status = BooleanField(default=False) #False for inactive True for active
    credit_limit = IntegerField()
    #credit_limit = DecimalField(max_digits=10, decimal_places=2)
    #https://github.com/encode/django-rest-framework/issues/1263

    LOGGER.info("Customer class created. Fields defined")
