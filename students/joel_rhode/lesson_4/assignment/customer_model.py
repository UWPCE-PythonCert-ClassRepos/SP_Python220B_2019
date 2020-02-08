"""Database model for customers"""

from peewee import SqliteDatabase, Model, CharField, BooleanField, DecimalField

DATABASE = SqliteDatabase(None)


class BaseModel(Model):
    """Base model class specifying database."""
    class Meta:
        """Meta class for database."""
        database = DATABASE


class Customer(BaseModel):
    """This class defines Customer, which represents a current or past customer."""
    customer_id = CharField(primary_key=True, max_length=20)
    name = CharField(max_length=30)
    lastname = CharField(max_length=30)
    home_address = CharField(max_length=50)
    phone_number = CharField(max_length=10)
    email_address = CharField(max_length=50)
    active_status = BooleanField()
    credit_limit = DecimalField(max_digits=9, decimal_places=2)
