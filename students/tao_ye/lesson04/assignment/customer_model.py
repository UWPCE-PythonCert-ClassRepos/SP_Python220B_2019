"""
    Customer database with Peewee ORM, sqlite and Python
    Here we define the schema
"""

from peewee import SqliteDatabase, Model, CharField, BooleanField, DecimalField

DATABASE = 'customers.db'

# create a peewee database instance -- our models will use this database to
# persist information
database = SqliteDatabase(DATABASE)
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only


# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    """ This class is the superclass for all tables below """
    class Meta:
        """ Meta class """
        database = database


# the customer model specifies its fields (or columns) declaratively
class Customer(BaseModel):
    """ This class defines Customer table with its columns. """
    customer_id = CharField(primary_key=True)
    name = CharField()
    last_name = CharField()
    home_address = CharField()
    phone_number = CharField()
    email_address = CharField(unique=True)
    active = BooleanField(default=True)
    credit_limit = DecimalField(max_digits=15, decimal_places=2)
