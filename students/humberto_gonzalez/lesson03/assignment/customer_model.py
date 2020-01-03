# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 18:43:47 2019

@author: Humberto
"""
# pylint: disable=too-many-arguments,too-few-public-methods,logging-format-interpolation

from peewee import Model
from peewee import SqliteDatabase
from peewee import CharField
from peewee import DecimalField

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(Model):
    """Base Model Class which other classes will be based off of"""
    class Meta:
        """Meta Class where the database is established"""
        database = DATABASE


class Customer(BaseModel):
    """Customer Model and the fields found in the model"""
    customer_id = CharField(primary_key=True, max_length=40)
    first_name = CharField(max_length=40)
    last_name = CharField(max_length=40)
    home_address = CharField(max_length=40)
    phone_number = CharField(max_length=40)
    email_address = CharField(max_length=40)
    status = CharField(max_length=40)
    credit_limit = DecimalField(max_digits=3)
    