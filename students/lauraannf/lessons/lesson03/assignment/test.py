# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 16:54:13 2019

@author: Laura.Fiorentino
"""

import logging
from peewee import *
from customer_model import *

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

new_customer = Customer.create(customer_ID='1')
