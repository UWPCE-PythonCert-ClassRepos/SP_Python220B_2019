"""Customer database model for Furniture store"""
from peewee import *
db = SqliteDatabase('customers.db')
db.connect()
db.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    """ This is the base model class for the database """
    class Meta:
        """ Defines database name """
        database = db


class Customer(BaseModel):
    """ This class contains customer information """
    customer_id = IntegerField(primary_key=True)
    firstname = CharField(max_length=40, null=False)
    lastname = CharField(max_length=40, null=False)
    address = CharField(max_length=200)
    phone_no = CharField(max_length=10)
    email = CharField(max_length=40)
    status = BooleanField()
    credit_limit = IntegerField(default=0)
