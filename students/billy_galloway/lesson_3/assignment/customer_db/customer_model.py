from peewee import *

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    customer_id = CharField(primary_key = True, max_length = 4)
    name = CharField(max_length = 30)
    last_name = CharField(max_length = 30)
    home_address = CharField(max_length = 40, null = False)
    phone_number = CharField(max_length = 12, null = False)
    email_address = CharField(max_length = 40, null = True)
    status = BooleanField(default = False)
    credit_limit = IntegerField(default = 0)