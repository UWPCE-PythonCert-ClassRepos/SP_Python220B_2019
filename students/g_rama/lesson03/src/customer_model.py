"""Database schema class"""
from peewee import *

DB = SqliteDatabase('customers.db')
#logging.info("Connecting to the customer database")
DB.connect()
DB.execute_sql('PRAGMA foreign_keys = ON;')
# db.close()


class BaseModel(Model):
    """Base model class using peewee"""
    class Meta:
        database = DB


class Customer(BaseModel):
    """Customer class to create the customer table"""
    customer_id = CharField
    name = CharField
    last_name = CharField
    home_address = CharField
    phone_number = CharField
    email_address = CharField
    status = CharField
    credit_limit = CharField


