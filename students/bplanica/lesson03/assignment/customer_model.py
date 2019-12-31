"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import peewee as pw

DATABASE = pw.SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(pw.Model):
    """BaseModel class"""
    class Meta:
        """Meta class"""
        database = DATABASE

class Customer(BaseModel):
    """
        This class defines Customer, which maintains details of someone
        for whom we want to retain information for business purposes
    """
    customer_id = pw.AutoField()
    name = pw.CharField(max_length=20)
    lastname = pw.CharField(max_length=20)
    home_address = pw.CharField(max_length=100)
    phone_number = pw.IntegerField() # no characters or country code
    email_address = pw.CharField(max_length=30, unique=True)
    status = pw.BooleanField()
    credit_limit = pw.DecimalField(max_digits=7, decimal_places=2)
