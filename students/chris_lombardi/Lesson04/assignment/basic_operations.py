"""Module for unit testing the methods of the basic_operations and customer_model modules"""

#pylint: disable=unused-wildcard-import
#pylint: disable=wildcard-import
#pylint: disable=too-many-arguments

import logging
import peewee
from customer_model import *

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler('db.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

LOGGER = logging.getLogger()
LOGGER.addHandler(file_handler)
LOGGER.addHandler(console_handler)

def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    """
    Add a new customer to the customer database using the provided params.
    """

    try:
        with database.transaction():
            logging.info('Trying to add customer %s...', customer_id)
            new_cust = Customer.create(
                cust_id=customer_id,
                cust_firstname=name,
                cust_lastname=lastname,
                cust_address=home_address,
                cust_phone=phone_number,
                cust_email=email_address,
                cust_status=status,
                cust_credit_limit=credit_limit
                )
            new_cust.save()
            LOGGER.info('Added new customer %s %s', name, lastname)

    except peewee.IntegrityError as error_1:
        LOGGER.info(error_1)
        LOGGER.info('Non-unique customer id: %s', customer_id)

def search_customer(customer_id):
    """
    Search the database for the primary key, customer id, and returns
    information about the requested customer if the customer id exists in the
    database. Otherwise returns an empty dictionary.
    """
    try:
        LOGGER.info('Looking for %s', customer_id)
        acustomer = Customer.get(Customer.cust_id == customer_id)
        return {'name': acustomer.cust_firstname, 'lastname': acustomer.cust_lastname,
                'email address': acustomer.cust_email, 'phone number': acustomer.cust_phone}
    except peewee.DoesNotExist:
        LOGGER.info('Customer ID %s does not exist in database.', customer_id)
        return {}

def delete_customer(customer_id):
    """
    Search the database for the requested customer and deletes the customer
    from the database if found.
    """
    try:
        acustomer = Customer.get(Customer.cust_id == customer_id)
        acustomer.delete_instance()
        LOGGER.info('%s deleted from database', customer_id)
    except peewee.DoesNotExist as error_1:
        LOGGER.info(error_1)
        LOGGER.info('%s was not in the database.', customer_id)

def update_customer_credit(customer_id, credit_limit):
    """
    Update the credit limit for the requested customer.

    Params:
    cust_id = primary key identifying customer in the database
    credit_limit = new credit limit to be set for the customer
    """
    try:
        with database.transaction():
            acust = Customer.get(Customer.cust_id == customer_id)
            acust.cust_credit_limit = credit_limit
            acust.save()
            LOGGER.info('Customer credit for %s limit updated to %s', customer_id, credit_limit)
    except peewee.DoesNotExist:
        LOGGER.info('%s is not in the database.', customer_id)
        raise ValueError

def list_active_customers():
    """
    Return the number of customers in the database who have a current status
    of active.
    """
    active_custs = Customer.select().where(Customer.cust_status == 'Active').count()
    LOGGER.info('There are %i active customers in the database.', active_custs)
    return active_custs
