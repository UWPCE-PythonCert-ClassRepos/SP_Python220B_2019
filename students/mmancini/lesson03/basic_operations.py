'''
    Basic operations for Customers Database
'''

# pylint: disable=too-few-public-methods
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
# pylint: disable=unnecessary-pass
# pylint: disable=no-self-use


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
    customer = (customer_id, first_name, last_name, home_address, phone_number,
                email_address, activity_status, credit_limit)
    try:
        with database.transaction():
            new_customer = Customer.create(
                customer_id=customer[CUSTOMER_ID],
                first_name=customer[FIRST_NAME],
                last_name=customer[LAST_NAME],
                home_address=customer[HOME_ADDRESS],
                phone_number=customer[PHONE_NUMBER],
                email_address=customer[EMAIL_ADDRESS],
                activity_status=customer[ACTIVITY_STATUS],
                credit_limit=customer[CREDIT_LIMIT])
            new_customer.save()
            LOGGER.info('added customer %s %s to db', first_name, last_name)
    except IntegrityError as exc:
        LOGGER.error(exc)
        LOGGER.info('Was not able to add customer to the database')



def search_customer(customers_id):
    '''
        search customer in db
        in: customer id
        out: dict of fount customer
    '''
    pass
    customer_found = "no"

    try:
        customer = Customer.get(Customer.customer_id == customers_id)
        customer_dict = {'first_name': customer.first_name,
                         'last_name': customer.last_name,
                         'email_address': customer.email_address,
                         'phone_number': customer.phone_number}
        customer_found = "yes"
    except DoesNotExist:
        raise ValueError('Customer id is not in the database')

    LOGGER.info('search of customer found == %s', customer_found)
    return customer_dict

def delete_customer(customers_id):
    '''deletes customer from database'''
    pass
    try:
        customer = Customer.get(Customer.customer_id == customers_id)
        customer.delete_instance()
        LOGGER.info('deleted customer %s %s from the database',
                    customer.first_name, customer.last_name)

    except DoesNotExist:
        raise ValueError('Customer not deleted id is not found in the database')

def update_customer_credit(customers_id, new_credit_limit):
    '''
        update customer in db
    '''
    pass
    try:
        customer = Customer.get(Customer.customer_id == customers_id)
        current_credit_limit = customer.credit_limit
        customer.credit_limit = new_credit_limit
        customer.save()
        LOGGER.info('updated customer %s %s credit limit from %s to %s',
                    customer.first_name, customer.last_name,
                    current_credit_limit, customer.credit_limit)
    except DoesNotExist:
        raise ValueError('update failed, customer id is not found in the database')

def list_active_customers():
    '''
        list active customers
        out:  number of active customers
    '''
    pass
    active_count = 0
    for customer in Customer.select():
        if customer.activity_status is True:
            active_count += 1
    LOGGER.info('Returning %s active customers', active_count)
    return active_count


def close_database():
    '''Closes the customers.db database'''
    database.close()
    LOGGER.info('database closed')
