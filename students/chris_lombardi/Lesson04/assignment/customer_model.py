"""A customer model to be used in a database."""

#pylint: disable=unused-wildcard-import
#pylint: disable=wildcard-import
#pylint: disable=too-few-public-methods

from peewee import *

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreing_keys = ON;')

class BaseModel(Model):
    """Establish the database to be used by the Customer class"""
    class Meta:
        """Meta class for peeweee to interpret database."""
        database = database

class Customer(BaseModel):
    """
    This class defines a customer, which maintains details of somone
    for whom we want to retain information and history about.
    """
    cust_id = CharField(primary_key=True, max_length=3)
    cust_firstname = CharField(max_length=15)
    cust_lastname = CharField(max_length=20)
    cust_address = CharField(max_length=40)
    cust_phone = CharField(max_length=10)
    cust_email = CharField(max_length=40)
    cust_status = CharField(max_length=8)
    cust_credit_limit = DecimalField(decimal_places=2)
