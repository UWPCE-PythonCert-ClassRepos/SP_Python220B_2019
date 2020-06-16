from peewee import *

db = SqliteDatabase('customers.db')
db.connect()
db.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    """
    BaseModel for Peewee as parent class
    """
    class Meta:
        database = db


class Customer(BaseModel):
    """
    This class defines Customer, which maintains details of customer info.
    """
    customer_id = CharField(primary_key=True, max_length=30)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=200)
    phone_number = CharField(max_length=10)
    email_address = CharField(max_length=50)
    active_status = BooleanField(default=True)
    credit_limit = DecimalField(max_digits=10, decimal_places=2, default=0)





