# Advanced Programming In Python - Lesson 3 Assigmnet 1: Relational Databases
# RedMine Issue - SchoolOps-13
# Code Poet: Anthony McKeever
# Start Date: 11/06/2019
# End Date: 11/09/2019

"""
The schema of the Customers DB (customer.db)
"""

import datetime

from peewee import SqliteDatabase
from peewee import Model

from peewee import CharField
from peewee import DecimalField
from peewee import DateTimeField

DATABASE = SqliteDatabase("customers.db")
DATABASE.connect()
DATABASE.execute_sql("PRAGMA foreign_keys = ON;")


class BaseModel(Model):
    """ The base model for the customer database """

    class Meta:
        """ The meta class """

        database = DATABASE


class Customers(BaseModel):
    """
    The model representing the customers table.
    """

    # pylint: disable=arguments-differ

    customer_id = CharField(primary_key=True, unique=True, max_length=30)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=200, null=True)
    phone_number = CharField(max_length=20, null=True)
    email_address = CharField(max_length=30, null=True)
    status = CharField(max_length=8, default="active")
    credit_limit = DecimalField(max_digits=10, decimal_places=2, null=True)
    date_created = DateTimeField(default=datetime.datetime.now)
    date_modified = DateTimeField(default=datetime.datetime.now)

    def save(self, **kwargs):
        """
        Saves changes to the customer and updates the date modified.

        :self:      The model
        :**kwargs:  Any additional kwargs to pass to Peewee's BaseModel.save
        """
        self.date_modified = datetime.datetime.now()
        super().save(**kwargs)

    def as_dictionary(self):
        """
        Return the customer as a dictionary containing all values.
        """
        return {"customer_id":   self.customer_id,
                "first_name":    self.first_name,
                "last_name":     self.last_name,
                "home_address":  self.home_address,
                "phone_number":  self.phone_number,
                "email_address": self.email_address,
                "status":        self.status,
                "credit_limit":  self.credit_limit,
                "date_created":  self.date_created,
                "date_modified": self.date_modified}

    def as_contact_info_dictionary(self):
        """
        Return the customer's contact info as a dictionary including
        first_name, last_name, phone_number, and email_address
        """
        return {"first_name":    self.first_name,
                "last_name":     self.last_name,
                "phone_number":  self.phone_number,
                "email_address": self.email_address}
