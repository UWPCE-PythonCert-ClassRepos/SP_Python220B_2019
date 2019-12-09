""" Creating the customer class model that customers are based off of """

# pylint: disable=too-few-public-methods

import peewee as pw

DATABASE = pw.SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')


# creating classes
class BaseModel(pw.Model):
    """ Base Model Class Setup """
    class Meta:
        """ Meta Class Setup """
        database = DATABASE


class Customer(BaseModel): # creating new customer
    """ Creating the customer attributes """
    customer_id = pw.CharField(primary_key=True, max_length=4)
    customer_firstname = pw.CharField(max_length=15)
    customer_lastname = pw.CharField(max_length=15)
    customer_address = pw.CharField(max_length=50)
    customer_phone = pw.CharField(max_length=12)
    customer_email = pw.CharField(max_length=30)
    customer_status = pw.BooleanField(default=True)
    customer_credit = pw.DecimalField(decimal_places=2)
