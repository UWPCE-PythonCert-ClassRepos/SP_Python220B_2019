""" Creates a Customer SQLite database and defines the schema/model """

import peewee

# pylint: disable=too-many-arguments, too-few-public-methods

DATABASE = peewee.SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(peewee.Model):
    """ Define the Base Model to establish database connectivity """

    class Meta:
        """ Define reference to database """
        database = DATABASE

class Customer(BaseModel):
    """ Define the fields for the Customer table """

    customer_id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(max_length=40)
    lastname = peewee.CharField(max_length=40)
    home_address = peewee.CharField(max_length=100)
    phone_number = peewee.CharField(max_length=20)
    email_address = peewee.CharField(max_length=100)
    status = peewee.CharField(max_length=8)
    credit_limit = peewee.DecimalField(max_digits=10, decimal_places=2)
