'''
Peewee ORM, sqlite and Python
Define schema
Use logging for messages
'''
# C:\Users\v-ollock\AppData\Local\Programs\Python\Python37-32\Lib\sqlite3

from peewee import *
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Connecting to db.')

DB = SqliteDatabase('customer.db')
DB.connect()
DB.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only


class BaseModel(Model):
    """
        Peewee BaseModel class.
    """
    class Meta:
        """Peewee meta class.  Assignes db."""
        database = DB


class Customer(BaseModel):
    """
        This class defines Customer, which maintains details of HP Norton's
        customers.
    """
    # customer_id = IdentityField() or AutoField()
    # the videos said use your 'business sense' for primary key
    name = CharField(primary_key=True, max_length=50)
    last_name = CharField(max_length=50)
    home_address = CharField(max_length=50)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=50)
    status = BooleanField()
    poverty_score = DecimalField(max_digits=3, decimal_places=0)


LOGGER.info('Creating Customer Table.')
DB.create_tables([Customer])
DB.close()
