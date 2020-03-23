"database format"
# pylint: disable=unused-import, unused-wildcard-import,
# pylint: disable=too-few-public-methods, too-many-arguments, wildcard-import
# pylint: disable=logging-format-interpolation, pointless-string-statement
from peewee import *

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    """base model"""
    class Meta:
        """meta"""
        database = DATABASE


class Customer(BaseModel):
    """various database fields"""
    customer_id = CharField(unique=True)
    name = CharField()
    last_name = CharField()
    home_address = CharField()
    phone_number = IntegerField(max)
    email_address = CharField()
    status = BooleanField()
    credit_limit = IntegerField()
