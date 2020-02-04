from peewee import SqliteDatabase, Model, DecimalField, CharField, BooleanField

customer_db = SqliteDatabase('customers.db')
customer_db.connect()

class BaseModel(Model):
    class Meta:
        database = customer_db

class Customer(BaseModel):
    """This class defines the Customer DB schema."""
    customer_id = DecimalField(primary_key=True)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=100)
    phone_number = DecimalField(max_digits=10)
    email_address = CharField(max_length=40)
    is_active = BooleanField(default=True)
    credit_limit = DecimalField(max_digits=7, decimal_places=2)
