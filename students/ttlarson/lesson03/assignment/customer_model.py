"""
    general requirements for 3 user types:
    1. As a salesperson at HP Norton I need to be able to store details of
       customers so that I can manage how I contact them to sell furniture.
    2. As an accountant at HP Norton I need to be able to store and retrieve
       a customer’s credit limit.
    3. As a manager at HP Norton I need to be able to produce monthly counts of
       the total number of active customers so that I can assess if the business
       is growing or shrinking.
"""

# pylint: disable=too-few-public-methods

import logging
from peewee import SqliteDatabase, Model, AutoField, CharField, DecimalField, BooleanField, DoubleField

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SqliteDatabase('customers.db')
db.connect()
db.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    """ Base model for Customer """
    class Meta:
        """ Meta class for the model """
        database = db


class Customer(BaseModel):
    """
        This class defines Customer, which maintains
        the details of the customer's contact information.
    """
    customer_id = AutoField() # Auto-incrementing primary key.
    customer_name = CharField(max_length=50)
    customer_lastname = CharField(max_length=50)
    customer_address = CharField(max_length=300, null=True)
    customer_phone_number = CharField(max_length=20, null=True)
    customer_email = CharField(max_length=100, null=True)
    status = BooleanField(default=False)
    credit_limit = DoubleField(null=True)
    # credit_limit = DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        """ Meta class to name the table """
        table_name = 'customers'

if not db.table_exists(Customer):
    db.create_tables([Customer])
