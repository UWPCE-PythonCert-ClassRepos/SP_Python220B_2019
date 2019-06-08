'''
    Basic operations for the HP Norton Database

    additions for lesson04: logging to db.log,
                            list_active_customers now uses a generator comprehension,
                            display_customers function added

    pylint Disable=wildcard-import, unused-wildcard-import, too-many-arguments
'''

import logging
from hp_norton_model import *

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.INFO)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

CUSTOMER_ID = 0
FIRST_NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
PHONE_NUMBER = 4
EMAIL_ADDRESS = 5
ACTIVITY_STATUS = 6
CREDIT_LIMIT = 7

LOGGER.info('Running basic_operations.py')
database.init('customers.db')
LOGGER.info('customers.db database initialized')
database.create_tables([Customer])
LOGGER.info('Database tables created if database is empty')

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
    LOGGER.info(customer_dict)
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
        LOGGER.info("%s %s's credit limit has been changed to %s",
                    customer.first_name, customer.last_name, customer.credit_limit)
    except DoesNotExist:
        raise ValueError('Customer id is not in the database')


def list_active_customers():
    '''
        Returns an integer with the number of customers whose status
        is currently active. Now uses a generator
    '''
    active_count = 0
    for status in (customer.activity_status for customer in Customer.select()):
        if status is True:
            active_count += 1
    LOGGER.info('There are %s active customers in the database.', active_count)
    return active_count


def display_customers():
    '''
        Uses a generator comprehension to loop through the customers in the database and display
        their names as log entries.
    '''
    LOGGER.info('Displaying the names of all the customers in the database.')
    gen = ((f'{customer.first_name}'+' '+f'{customer.last_name}') for customer in Customer.select())
    for name in gen:
        LOGGER.info(name)


def close_database():
    '''Closes the customers.db database'''
    database.close()
    LOGGER.info('database closed')
