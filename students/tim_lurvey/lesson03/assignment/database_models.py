#!/usr/env/bin python
"""This file contains the database models for storing
customer data."""

from peewee import Model, CharField, IntegerField, BooleanField, FloatField, SqliteDatabase

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    """Base class for establishing database"""

    class Meta:
        """This is a mystery to me"""
        database = database


class Customer(BaseModel):
    """This class holds all the definitions for a customer entry"""
    # http://docs.peewee-orm.com/en/latest/peewee/models.html#field-initialization-arguments
    customer_id = CharField(primary_key=True, max_length=10)
    name = CharField(max_length=20)
    lastname = CharField(max_length=20)
    home_address = CharField(max_length=200)
    phone_number = IntegerField()
    email_address = CharField(max_length=40)
    active = BooleanField(default=False)
    credit_limit = FloatField()


if __name__ == '__main__':
    # Create a new empty database
    database.create_tables([Customer])
    database.close()
