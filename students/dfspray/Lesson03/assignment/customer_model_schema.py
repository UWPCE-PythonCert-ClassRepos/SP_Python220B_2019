"""
    This file defines the schema of the data stored
    in the database
"""

from peewee import *

database = SqliteDatabase('cutomer_data.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database

class Customer(BaseModel):
    """
        This class defines Customer, which maintains all information,
        of someone for whom we want to research
    """

    customer_id = CharField(primary_key = True, max_length = 30)
    name = CharField(max_length = 40)
    lastname = CharField(max_length = 20, null = True)
    home_address = CharField(max_length = 20, null = True)
    phone_number = CharField(max_length = 20, null = True)
    email_address = CharField(max_length = 20, null = True)
    status = CharField(max_length = 20, null = True)
    credit_limit = CharField(max_length = 20, null = True)