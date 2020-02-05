# pylint: disable=too-few-public-methods, unused-import
#too-few-public-methods flags on the classes -- however this is fundamental to the peewee structure
#unused-import flags on DoesNotExist, however that's necessary to allow downstream exception
#catching in basic_operations (where it also flags)

"""This module defines the structure of the Customer database."""

from peewee import (SqliteDatabase, Model, DecimalField, CharField, BooleanField, DoesNotExist,
                    IntegrityError)

customer_db = SqliteDatabase('customers.db')
customer_db.connect()

class BaseModel(Model):
    """Peewee BaseModel"""
    class Meta:
        """Peewee Meta class"""
        database = customer_db

class Customer(BaseModel):
    """This class defines the Customer DB schema."""
    customer_id = DecimalField(primary_key=True)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=100)
    phone_number = DecimalField(max_digits=10)
    email_address = CharField(max_length=40)
    is_active = BooleanField(default=True)
    credit_limit = DecimalField(max_digits=7, decimal_places=2)
