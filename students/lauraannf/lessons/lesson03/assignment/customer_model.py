# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 15:41:41 2019

@author: Laura.Fiorentino

Lesson3 Assignment
"""


from peewee import *


DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only


class BaseModel(Model):
    """ sets up model"""
    class Meta:
        """sets up model"""
        database = DATABASE


class Customer(BaseModel):
    """
        This class defines Customer, which maintains details of customers
    """
    customer_ID = CharField(primary_key=True,
                            constraints=[Check('length(customer_id)==5')])
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=100)
    phone_number = CharField(constraints=[Check('length(phone_number)==10')])
    email_address = CharField(max_length=30)
    status = BooleanField()
    credit_limit = IntegerField()


class Rentals(BaseModel):
    """ Rental Database"""
    rental_number = CharField(primary_key=True, max_length=10)
    renter = ForeignKeyField(Customer, null=False)

if __name__ == '__main__':

    models = [Customer, Rentals]
    DATABASE.create_tables(models)
