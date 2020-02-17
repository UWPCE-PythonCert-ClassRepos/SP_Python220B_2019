'''
basic operations for employees to perform 
for customer data
'''

import logging
from peewee import *
from customer_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Working with Customer class')

CUST_ID = 0
NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
EMAIL_ADDRESS = 4
PHONE = 5
STATUS = 6
CREDIT_LIMIT = 7

def add_customer(customer_id, name, last_name,
                 home_address, email_address,
                 phone_number, status, credit_limit):
    ''' add new customers to the database '''
    customer = (customer_id, name, last_name,
                home_address, email_address,
                phone_number, status, credit_limit)
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
            logger.info(f'{name} {last_name} added to database')
    except Exception as e:
        logger.info(f'Error creating customer id {customer_id}')
        logger.info(f'Exception: {e}')


def search_customer(customer_id):
    try:
        customer = Customer.get(Customer.customer_id == customer_id)

    except DoesNotExist:
        raise ValueError(f'{customer_id} not found in database')

    return {'name': customer.name, 
            'last_name': customer.last_name,
            'email_address': customer.email_address, 
            'phone_number': customer.phone_number}

def delete_customer(customer_id):
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.delete_instance()
        logger.info(f'{customer.name} has been deleted')

    except DoesNotExist:
        raise ValueError(f'{customer.customer_id} not found in database')

def update_customer_credit(customer_id, credit_limit):
    ''' update customers credit limit '''
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
        logger.info(f'{customer.credit_limit}')

    except DoesNotExist:
        raise ValueError(f'{customer.customer_id} not found in database')
    
def list_active_customers():
    active_customers = Customer.select().where(Customer.status).count()
    logger.info(f'active customer count is {active_customers}')

    return active_customers

## testing search customer
# database.create_tables([Customer])
# database.close()
# customer = ('A500', 'Andrew', 'Smith',
#             '23 Railroad Street Matthews, NC 28104', 'andrew@hpnorton.com',
#             '202-555-0134', True, 1000)

# add_customer(customer[0],customer[1],customer[2],customer[3],
#              customer[4],customer[5],customer[6],customer[7])
# search_customer('C200')
