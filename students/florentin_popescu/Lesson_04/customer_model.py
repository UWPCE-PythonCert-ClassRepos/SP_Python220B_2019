# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 09:35:14 2019
@author: Florentin Popescu
"""
#pylint: disable-msg=too-many-arguments
#pylint: disable=W0401  #disable 'Wildcard import peewee'
#pylint: disable=W0614
#pylint: disable=R0903

#imports
import datetime
from peewee import *

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_key = ON;')
# ========================================


class BaseModel(Model):
    """
        set base model
    """
    class Meta:
        """
            set meta class
        """
        database = DATABASE
# ========================================


class Customer(BaseModel):
    """
        defines customer schema and formating
    """
    customer_id = CharField(primary_key=True, unique=True,
                            max_length=50, collation=False)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50, null=True)
    home_address = CharField(max_length=50, null=True)
    email_address = CharField(max_length=50, null=True)
    phone_number = CharField(max_length=50, null=True)
    status = CharField(max_length=50, null=True)
    credit_limit = DecimalField(max_digits=20, decimal_places=2, default=0)
    join_date = DateField(default=datetime.datetime.now)
    insertion_date = DateTimeField(default=datetime.datetime.now)
    time_stamp = DateTimeField(default=datetime.datetime.now)
    hobby = TextField()
# ========================================
