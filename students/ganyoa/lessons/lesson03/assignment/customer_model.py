import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Define data (the schema) for Customer table in customers.db')

db = SqliteDatabase('customers.db') # tell peewee which database to use
db.connect() # connect to customers.db


class BaseModel(Model):
    class Meta:
        database = db


class Customer(BaseModel):
    """
        This class/table defines Customer, which maintains details of someone
        for whom we want to research contact info, credit limit, and activity status
    """

    logger.info('Specify the fields in Customer model/table')

    customer_id = CharField(primary_key = True, max_length = 30)
    first_name = CharField(max_length = 30, null = False)
    last_name = CharField(max_length = 30, null = False)
    home_address = CharField(max_length = 50)
    phone_number = CharField(max_length = 12)
    email_address = CharField(max_length = 40, null = True)
    customer_status= BooleanField(null=False, default=True)
    credit_limit = DecimalField(max_digits = 7, decimal_places = 2)

db.create_tables([Customer])

db.close()