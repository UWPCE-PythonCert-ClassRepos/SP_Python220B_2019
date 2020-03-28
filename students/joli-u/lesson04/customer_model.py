"""
customer_model.py
Assignment 4
Joli Umetsu
PY220
"""
from peewee import SqliteDatabase, Model, IntegerField, CharField, BooleanField, DecimalField


DB = SqliteDatabase('customers.db')
DB.connect()
DB.execute_sql('PRAGMA foreign_keys = ON')


class BaseModel(Model):
    """ Establishes/defines database """

    class Meta:
        """ Defines model-specific configuration """
        database = DB


class Customer(BaseModel):
    """ Defines customer database table """

    customer_id = IntegerField(primary_key=True)
    name = CharField(max_length=20, null=False)
    lastname = CharField(max_length=20, null=False)
    home_address = CharField(max_length=40)
    phone_number = IntegerField()
    email_address = CharField(max_length=40, null=False)
    status = BooleanField()
    credit_limit = DecimalField()


# create tables
DB.create_tables([Customer])
DB.close()
