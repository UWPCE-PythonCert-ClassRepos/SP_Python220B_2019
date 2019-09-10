"""
Create a customer database in the sqlite3 database and use peewee model to
manipulate the data
"""
import os
import peewee

#pylint: disable = too-few-public-methods

PATH, FOLDER = os.path.split(os.getcwd())
DATABASE_FILE = os.path.join(PATH, 'database', 'customer.db')
DATABASE = peewee.SqliteDatabase(DATABASE_FILE)
DATABASE.connect()

class BaseModel(peewee.Model):
    """This is a base model class that defines the database."""
    class Meta:
        """Definition of the database"""
        database = DATABASE


class Customer(BaseModel):
    """
    This model class corresponds to the Customer table in sqlite3. The table
    columns define the attribute of Customer table.
    """
    customer_id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(max_length=30)
    last_name = peewee.CharField(max_length=30)
    home_address = peewee.CharField(max_length=100)
    phone_number = peewee.TextField()
    email_address = peewee.CharField(max_length=50)
    status = peewee.BooleanField(default=False)
    credit_limit = peewee.DecimalField(max_digits=8, decimal_places=2)
