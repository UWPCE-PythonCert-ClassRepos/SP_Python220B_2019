"""Module for customer model"""

# pylint: disable=too-few-public-methods

import peewee as pw

DATABASE = pw.SqliteDatabase('customers.db')  # Global variable
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')  # Needed for sqlite only


class BaseModel(pw.Model):
    """Base model class for sqlite"""
    class Meta:
        """Meta class for sqlite"""
        database = DATABASE


class Customer(BaseModel):
    """Create customer details"""
    # CharField field that has characters or numbers
    # primary_key = True, means everything has to be unique
    customer_id = pw.CharField(primary_key=True, max_length=3)
    first_name = pw.CharField(max_length=20)
    last_name = pw.CharField(max_length=20)
    home_address = pw.CharField(max_length=50)
    phone_number = pw.CharField(max_length=10)
    email_address = pw.CharField(max_length=50)
    status = pw.BooleanField(default=True)  # True=active/false=inactive
    credit_limit = pw.DecimalField(decimal_places=2)
