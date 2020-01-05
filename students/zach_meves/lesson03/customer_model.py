"""
Customer model definition.
"""

import peewee as pw

DB_NAME = 'customers.db'
DB = pw.SqliteDatabase(DB_NAME)


class Customer(pw.Model):
    """Customer model.

    Fields:
    Customer ID: int
    Name: str
    Lastname: str
    Home address: str
    Phone number: str
    Email address: str
    Status: bool
    Credit limit: float"""

    id = pw.IntegerField(primary_key=True)
    name = pw.CharField(max_length=255)
    last_name = pw.CharField(max_length=255)
    address = pw.CharField(max_length=255)
    phone = pw.CharField(max_length=12)
    email = pw.CharField(max_length=255)
    status = pw.BooleanField()
    credit_limit = pw.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        database = DB


# Create tables if required
DB.connect()
DB.create_tables([Customer])
