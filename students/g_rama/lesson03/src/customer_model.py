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
    customer_id = CharField(primary_key=True)
    name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    home_address = CharField(max_length=255)
    phone_number = CharField(max_length=255)
    email_address = CharField(max_length=255)
    status = CharField(max_length=255)
    credit_limit = CharField(max_length=255)


