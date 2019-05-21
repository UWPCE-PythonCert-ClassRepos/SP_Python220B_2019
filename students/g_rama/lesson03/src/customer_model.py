import sqlite3
import logging
from peewee import *


db = SqliteDatabase('customers.db')
#logging.info("Connecting to the customer database")
db.execute_sql('PRAGMA foreign_keys = ON;')
db.connect()
#database.close()

class BaseModel(Model):
    """Base model class using peewee"""
    class Meta:
        database = db


class Customer(BaseModel):
    """Customer class to create the customer table"""
    customer_id = IntegerField
    name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = TextField
    phone_number = TextField
    email_address = TextField
    status = BooleanField
    credit_limit = IntegerField

