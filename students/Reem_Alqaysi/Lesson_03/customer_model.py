"""
    Here we define thedatabase and customers schema
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
        This class defines Customers' related inforamtion table schema
    """
    customer_id = pw.AutoField()
    name = pw.CharField(max_length=20)
    lastname = pw.CharField(max_length=20)
    home_address = pw.CharField(max_length=100)
    phone_number = pw.IntegerField()
    email_address = pw.CharField(max_length=50, unique=True)
    status = pw.BooleanField()
    credit_limit = pw.DecimalField(max_digits=10, decimal_places=2)
