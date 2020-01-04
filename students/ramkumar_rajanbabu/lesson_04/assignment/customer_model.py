"""Module for customer model"""

# pylint: disable=too-few-public-methods

import logging
import peewee as pw

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DATABASE = pw.SqliteDatabase('customers.db')
LOGGER.info("Database initialized")
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
LOGGER.info("Connected to database")


class BaseModel(pw.Model):
    """Base model class"""
    class Meta:
        """Meta class"""
        database = DATABASE


class Customer(BaseModel):
    """Create customer details"""
    customer_id = pw.IntegerField(primary_key=True)
    first_name = pw.CharField(max_length=30)
    last_name = pw.CharField(max_length=30)
    home_address = pw.CharField(max_length=50)
    phone_number = pw.CharField(max_length=12)
    email_address = pw.CharField(max_length=50)
    status = pw.BooleanField(default=False)
    credit_limit = pw.DecimalField(decimal_places=2)
