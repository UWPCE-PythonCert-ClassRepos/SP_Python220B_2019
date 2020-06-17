"""Here we define the database and customers schema.
Creates Base Model and customer class """


import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')
logger.info("connected to the customer database.")

class BaseModel(Model):
    """Base Model Class"""
    class Meta:
        """Meta class"""
        database = database

class Customer(BaseModel):
    """Creates class to store customer data for database"""
    logger.info("create customer class to store info for database")

    customer_id = IntegerField(primary_key=True)
    first_name = CharField(max_length=20, null=False)
    last_name = CharField(max_length=20, null=False)
    home_address = CharField(max_length=80, null=False)
    phone_number = IntegerField()
    email_address = CharField(max_length=50, null=False)
    status = BooleanField()
    credit_limit = DecimalField(max_digits=10, decimal_places=2)
    logger.info("Customer class created. Fields created. ")
