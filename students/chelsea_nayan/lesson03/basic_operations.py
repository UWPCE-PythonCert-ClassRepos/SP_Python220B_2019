'''Basic Operations for the HP Norton database'''

# pylint: disable=too-many-arguments
# pylint: disable=wildcard-import
# pylint: unused-wildcard-import

import logging
import peewee
from customer_model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Logger is active!')

def add_customer(customer_id, firstname, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    '''Add a new customer to the sqlite3 database'''
    try:
        with database.transaction():
            logging.info('Attempting to add customer [%s] to the database!', customer_id)
            new_customer = Customer.create(c_id=customer_id,
                                           c_firstname=firstname,
                                           c_lastname=lastname,
                                           c_home_address=home_address,
                                           c_phone_number=phone_number,
                                           c_email_address=email_address,
                                           c_status=status,
                                           c_credit_limit=credit_limit)
            new_customer.save()
            LOGGER.info('Added the new customer, [%s %s]!', firstname, lastname)

    except peewee.IntegrityError as error_1:
        LOGGER.info(error_1)
        LOGGER.info('Tried adding customer. Customer id [%s] cannot be added!', customer_id)

def search_customer(customer_id):
    '''
    Return a dictionary object with firstname, lastname,
    email address, and phone number of a customer...
    or an empty dictionary if no costumer was found
    '''
    try:
        LOGGER.info('Searching for customer id, [%s]!', customer_id)
        some_customer = Customer.get(Customer.c_id == customer_id)
        return {'firstname': some_customer.c_firstname,
                'lastname': some_customer.c_lastname,
                'email_address': some_customer.c_email_address,
                'phone_number': some_customer.c_phone_number}
    except peewee.DoesNotExist:
        LOGGER.info(' Tried searching for customer. Customer id [%s] was not found.', customer_id)
        return {}

def delete_customer(customer_id):
    ''' Delete a customer from the sqlite3 database'''
    try:
        some_customer = Customer.get(Customer.c_id == customer_id)
        some_customer.delete_instance()
    except peewee.DoesNotExist as error_1:
        LOGGER.info(error_1)
        LOGGER.info('Tried deleting customer. Customer id [%s] was not found.', customer_id)

def update_customer_credit(customer_id, credit_limit):
    '''
    Search as existing customer by id and update their credit limit...
    Or raise a ValueError exception if the customer does not exist
    '''
    try:
        with database.transaction():
            some_customer = Customer.get(Customer.c_id == customer_id)
            some_customer.c_credit_limit = credit_limit
            some_customer.save()
            LOGGER.info('Customer [%s]\'s credit limit updated!', customer_id)
    except peewee.DoesNotExist:
        LOGGER.info(' Tried updating credit limit. Customer id [%s] was not found.', customer_id)

def list_active_customers():
    '''
    Return an integer with the number of customers whose status is currently active
    '''
    active_customers = Customer.select().where(Customer.c_status == 'Active').count()
    LOGGER.info('Currently [%i] active customers in the database.', active_customers)
    return active_customers

def close_database():
    '''Closes the database'''
    database.close()
    LOGGER.info('Database is closed!')
