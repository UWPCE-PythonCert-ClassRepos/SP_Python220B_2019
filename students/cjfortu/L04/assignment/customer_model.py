#!/usr/bin/env python
"""
Model for Customer class.

Uses customized fields, from customized_fields module.
"""

import logging
from peewee import SqliteDatabase, CharField, Model
from customized_fields import ActiveField, CustIDField, PhoneField, CreditField

# Start logging parameters here vvv
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'db.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
CONSOLE_HANDLER = logging.StreamHandler()
LOGGER = logging.getLogger()
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.INFO)
CONSOLE_HANDLER.setLevel(logging.INFO)
LOGGER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(FILE_HANDLER)
CONSOLE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(CONSOLE_HANDLER)
# End logging parameters here ^^^

LOGGER.info('Logger initialized')

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

LOGGER.info('Database initialized')


class BaseModel(Model):
    """
    Establish the base model.
    """

    class Meta:
        """
        Meta subclass for database.
        """
        database = database


class Customer(BaseModel):
    """
    Establish the customer model.
    """

    customer_id = CustIDField(primary_key=True)
    name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=255)
    phone_number = PhoneField()
    email_address = CharField(max_length=30)
    status = ActiveField()
    credit_limit = CreditField()


database.create_tables([Customer])
database.close()
