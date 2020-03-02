"""
customer_model.py
Joli Umetsu
PY220
"""
import logging
from peewee import SqliteDatabase, Model, IntegerField, CharField, BooleanField, DecimalField

# logger setup
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DB = SqliteDatabase('customers.db')
LOGGER.info("created instance of a database...")

DB.connect()
DB.execute_sql('PRAGMA foreign_keys = ON')
LOGGER.info("connected to database...")

class BaseModel(Model):
    """ Establishes/defines database """

    class Meta:
        """ Defines model-specific configuration """
        database = DB


class Customer(BaseModel):
    """ Defines customer database table """

    customer_id = IntegerField(primary_key=True)
    name = CharField(max_length=20, null=False)
    lastname = CharField(max_length=20, null=False)
    home_address = CharField()
    phone_number = IntegerField()
    email_address = CharField(max_length=40, null=False)
    status = BooleanField()
    credit_limit = DecimalField()
