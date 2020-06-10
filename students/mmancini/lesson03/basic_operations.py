'''
    Basic operations for Customers Database
'''
# pylint Disable=wildcard-import, unused-wildcard-import, too-many-arguments

import logging
from customers_model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Logger initialized')

CUSTOMER_ID = 0
FIRST_NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
PHONE_NUMBER = 4
EMAIL_ADDRESS = 5
ACTIVITY_STATUS = 6
CREDIT_LIMIT = 7

database.init('customers.db')
LOGGER.info('customers db database initialized')
database.create_tables([Customer])
LOGGER.info('Customer tables created in database')


def add_customer(customer_id, first_name, last_name, home_address, phone_number,
                 email_address, activity_status, credit_limit):
    '''adds new customer to the database'''
    pass
    LOGGER.info('added customer %s %s to db', first_name, last_name)


def search_customer(customers_id):
    '''
        search customer in db
        in: customer id
        out: dict of fount customer
    '''
    pass
    customer_found = "no"
    LOGGER.info('search of customer found == %s', customer_found)
    

def delete_customer(customers_id):
    '''deletes customer from database'''
    pass
    LOGGER.info('customer delete completed')


def update_customer_credit(customers_id, new_credit_limit):
    '''
        update customer in db
    '''
    pass
    LOGGER.info('customer update completed')

def list_active_customers():
    '''
        list active customers
        out:  number of active customers
    '''
    pass
    active_customers = 0
    LOGGER.info('Returning %s active customers', active_customers)

def close_database():
    '''Closes the customers.db database'''
    database.close()
    LOGGER.info('database closed')
