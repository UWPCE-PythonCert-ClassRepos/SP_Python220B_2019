"""Defines the customer schema for the DB"""

import peewee as pw

DATABASE = pw.SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON')


# pylint: disable=too-few-public-methods
class BaseModel(pw.Model):
    """init the DB"""

    class Meta:
        """META"""
        database = DATABASE


class Customer(BaseModel):
    """Customer with all the details"""
    customer_id = pw.IntegerField(primary_key=True)
    customer_first_name = pw.CharField(max_length=25)
    customer_last_name = pw.CharField(max_length=25)
    customer_home_address = pw.CharField(max_length=100)
    customer_phone_number = pw.CharField(max_length=20)
    customer_email = pw.CharField(max_length=50)
    customer_status = pw.BooleanField()
    customer_credit_limit = pw.IntegerField()
