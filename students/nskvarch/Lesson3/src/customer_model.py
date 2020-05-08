"""Schema file for a SQLite3 customer database for a point of sale system"""

from peewee import *

# define database and connect
database = SqliteDatabase("customers.db")
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    """Base model class to inherit from peewee"""
    class Meta:
        database = database


class Customer(BaseModel):
    """define the customer database table fields"""
    customer_id = CharField(primary_key=True, max_length=7)
    first_name = CharField(max_length=15)
    last_name = CharField(max_length=20)
    mailing_address = CharField(max_length=50)
    phone_number = CharField(max_length=9)
    email_address = CharField(max_length=40)
    active_status = BooleanField()
    credit_limit = DecimalField(max_digits=7, decimal_places=2)
