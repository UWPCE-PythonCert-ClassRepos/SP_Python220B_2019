# pylint: disable=wildcard-import, unused-wildcard-import
# pylint: disable=too-few-public-methods
"""
Module to define and create sqllite3 database
and tables for customer data
"""
from peewee import *
# create a peewee database instance -- our models will use this database to
# persist information
database = SqliteDatabase("customer.db")
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    """Class to peewee base model."""
    class Meta:
        """
        Meta configuration is passed on to subclasses,
        so our project’s models will all subclass BaseModel
        """
        database = database


class Customer(BaseModel):
    """Class to create table to store customer information."""
    customerid = CharField(primary_key=True, max_length=30)
    name = CharField(max_length=50)
    lastname = CharField(max_length=50)
    status = BooleanField()
    creditlimit = IntegerField()


class CustomerContact(BaseModel):
    """Class to create table to store customer contact information."""
    id = AutoField()  # Event.event_id will be auto-incrementing PK.
    homeaddress = CharField(max_length=100)
    phonenumber = CharField(max_length=20)
    emailaddress = CharField(max_length=100)
    contactid = ForeignKeyField(Customer, backref='customercontacts', null=False)
