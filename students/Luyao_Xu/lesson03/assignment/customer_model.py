"""
customer model for database use
"""
import logging
from peewee import SqliteDatabase, Model, CharField, BooleanField,\
    DecimalField, IntegerField


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Here we define our data (the schema)')
LOGGER.info('First name and connect to a database (sqlite here)')

LOGGER.info('The next 3 lines of code are the only database specific code')

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    """
    This class defines the database
    """
    class Meta:
        """
        Inheritance only keep the model
        """
        database = DATABASE


class Customer(BaseModel):
    """
    This class defines Customer, which maintains details of
    customer data for use of HP Norton.
    """

    customer_id = IntegerField(primary_key=True)
    first_name = CharField(max_length=80, null=False)
    last_name = CharField(max_length=80, null=False)
    home_address = CharField(max_length=40, null=True)
    phone_number = CharField(max_length=12, null=True)  # 206-xxx-xxxx
    email_address = CharField(max_length=150, null=True)
    credit_limit = DecimalField(max_digits=5, decimal_places=2)  # 745.67
    is_active = BooleanField(null=False, default=False)
