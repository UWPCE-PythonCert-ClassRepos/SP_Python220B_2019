'''
    Basic operations for the HP Norton Database
'''
# pylint Disable=wildcard-import, unused-wildcard-import, too-many-arguments

import logging
from hp_norton_model import *

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
LOGGER.info('customers.db database initialized')
database.create_tables([Customer])
LOGGER.info('Customer schema created in database')


def add_customer(customer_id, first_name, last_name, home_address, phone_number,
                 email_address, activity_status, credit_limit):
    '''adds a new customer to the database'''
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
            LOGGER.info('%s %s added to database', customer[1], customer[2])
    except IntegrityError as exc:
        LOGGER.error(exc)
        LOGGER.info('Was not able to add customer to the database')


def search_customer(customers_id):
    '''
        returns a dictionary object with first name, last name, email address
        and phone number of a customer or an empty dictionary object if no
        customer was found
    '''
    try:
        customer = Customer.get(Customer.customer_id == customers_id)
        customer_dict = {'first_name': customer.first_name,
                         'last_name': customer.last_name,
                         'email_address': customer.email_address,
                         'phone_number': customer.phone_number}
    except DoesNotExist:
        raise ValueError('Customer id is not in the database')

    return customer_dict


def delete_customer(customers_id):
    '''deletes a customer from the database'''
    try:
        customer = Customer.get(Customer.customer_id == customers_id)
        LOGGER.info('%s %s will be deleted from the database',
                    customer.first_name, customer.last_name)
        customer.delete_instance()
        LOGGER.info('This customer has been deleted')

    except DoesNotExist:
        raise ValueError('Customer id is not in the database')


def update_customer_credit(customers_id, new_credit_limit):
    '''
        search an existing customer by customer_id and update their credit limit
        or raise a ValueError exception if the customer does not exists
    '''
    try:
        customer = Customer.get(Customer.customer_id == customers_id)
        customer.credit_limit = new_credit_limit
        customer.save()
        LOGGER.info(customer.credit_limit)
    except DoesNotExist:
        raise ValueError('Customer id is not in the database')


def list_active_customers():
    '''
        returns an integer with the number of customers whose status
        is currently active
    '''
    active_count = 0
    for customer in Customer.select():
        if customer.activity_status is True:
            active_count += 1
    return active_count


def close_database():
    '''Closes the customers.db database'''
    database.close()
    LOGGER.info('database closed')
