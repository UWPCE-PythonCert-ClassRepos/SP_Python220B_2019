"""
Define the schema for the customer database.
Create table Customers

"""

#pylint: disable=unused-wildcard-import
#pylint: disable=wildcard-import
#pylint: disable=invalid-name
#pylint: disable=too-few-public-methods

from peewee import *

database = SqliteDatabase('customer.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    """
    Basemodal class for database init
    """

    class Meta:
        """
        Meta class for database init.
        """
        database = database


class Customer(BaseModel):
    """
    Defines the Customer table for customer.db
    """
    customer_id = CharField(primary_key=True, max_length=4)
    customer_name = CharField(max_length=30)
    customer_last_name = CharField(max_length=30)
    customer_address = CharField(max_length=180, null=True)
    customer_phone_number = CharField(max_length=10)
    customer_email = CharField(max_length=30, null=True)
    customer_status = BooleanField()
    customer_credit_limit = DecimalField(decimal_places=2, default=0)
