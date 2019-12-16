"""Create Customer model and save it as 'customers.db' file"""

from peewee import *

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(Model):
    """ This class defines the base model for database setup """
    class Meta:
        """ Assign database variable """
        database = database

class Customer(BaseModel):
    """ This defines a customer with detail info to be saved in the database """
    customer_id = IntegerField(primary_key=True, verbose_name="Customer ID")
    name = CharField(verbose_name="Name", max_length=50)
    lastname = CharField(verbose_name="Lastname", max_length=50)
    home_address = CharField(verbose_name="Home address", max_length=120)
    phone_number = FixedCharField(verbose_name="Phone number", help_text="Phone number format: xxx-xxx-xxxx", max_length=12, constraints=[Check('length(phone_number) == 12')])
    email_address = CharField(verbose_name="Email address", max_length=40)
    status = BooleanField(verbose_name="Status", help_text="True for active customer, or False for inactive customer")
    credit_limit = DecimalField(verbose_name="Credit limit", max_digits=20, decimal_places=2)
    