"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
from peewee import SqliteDatabase, Model, CharField, IntegerField
# noqa # pylint: disable=too-few-public-methods

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Here we define our data (the schema)')
LOGGER.info('The next 3 lines of code are the only database specific code')

DATABASE = SqliteDatabase('customer.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only


LOGGER.info('This means we can easily switch to a different database')
LOGGER.info('Enable the Peewee magic! This base class does it all')


class BaseModel(Model):
    """
        This class defines the DATABASE
    """
    class Meta:
        """
        This class defines the DATABASE
        """
        database = DATABASE

LOGGER.info('By inheritance only we keep our model \
            (almost) technology neutral')


class Customer(BaseModel):
    """
        This class defines Customer, which store customer data from HP Norton.
    """
    LOGGER.info('Note how we defined the class')

    LOGGER.info('Specify the fields in our model, their lengths and if mandatory')
    LOGGER.info('Must be a unique identifier for each person')
    name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=30)
    phone_number = CharField(max_length=30)
    email = CharField(max_length=30, null=True)
    status = CharField(max_length=30)
    credit_limit = IntegerField()
