""" Define the Customer DB model """

# Russell Felts
# Assignment 3 - DB Model

# pylint: disable=too-few-public-methods

import logging
from peewee import SqliteDatabase, CharField, \
    BooleanField, DecimalField, Model, AutoField

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info("Create and connect to the DB.")
DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON')


class BaseModel(Model):
    """ Define the DB to be used """
    class Meta:
        """ Peewee interpreter class """
        database = DATABASE


class Customer(BaseModel):
    """ Defines the customer table of the DB """
    LOGGER.info("Specify the fields and their attributes.")

    customer_id = AutoField(primary_key=True)
    name = CharField(max_length=40, null=False)
    last_name = CharField(max_length=40, null=False)
    home_address = CharField(max_length=100, null=True)
    phone_number = CharField(max_length=11, null=False)
    email = CharField(max_length=35, null=False)
    status = BooleanField(default=True)
    credit_limit = DecimalField(decimal_places=2)
