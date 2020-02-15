import logging
from peewee import *
from customer_model import Customer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with Customer class')

CUST_ID = 0
NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
PHONE = 4
EMAIL_ADDRESS = 5
STATUS = 6
CREDIT_LIMIT = 7

customers = [
    ('A500', 'Andrew', 'Smith',
     '23 Railroad Street Matthews, NC 28104', '202-555-0134',
     'andrew@hpnorton.com', True, 1000),
    ('A501', 'David', 'Nelson',
     '7 Blackburn Drive Tualatin, OR 97062', '202-555-0169',
     'david@hpnorton.com', True, 0),
    ('B200', 'Kate', 'Harris',
     '638 Cactus St. Wilmington, MA 01887', '202-555-0169',
     'kate@hpnorton.com', False, 1000)
    ]


def add_customer(customer_id, name, lastname,
                 home_address, phone_number,
                 email_address, status, credit_limit):
    ''' add new customers to the database '''
    for customer in customers:
        try:
            with database.transaction():
                new_customer = Customer.create(
                    customer_id = customer[CUST_ID],
                    name = customer[NAME],
                    last_name = customer[LAST_NAME],
                    home_address = customer[HOME_ADDRESS],
                    email_address = customer[EMAIL_ADDRESS],
                    phone_number = customer[PHONE],
                    status = customer[STATUS],
                    credit_limit = customer[CREDIT_LIMIT])
                new_customer.save()

        except Exception as e:
            logger.info(f'Error creating customer id {customer[CUST_ID]}')
            logger.info(e)

def search_customer(self):
    pass
def delete_customer(self):
    pass
def update_customer_credit(self):
    pass
def list_active_customers(self):
    pass

add_customer(customers[0][CUST_ID], customers[0][NAME], customers[0][LAST_NAME],
             customers[0][HOME_ADDRESS], customers[0][EMAIL_ADDRESS],
             customers[0][PHONE], customers[0][STATUS], customers[0][CREDIT_LIMIT])