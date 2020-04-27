"""
Create Customers database
"""

from peewee import *

database = SqliteDatabase('customers.db')
database.connect()

class BaseModel(Model):
    class Meta:
        database = database


class Customers(BaseModel):
    pass