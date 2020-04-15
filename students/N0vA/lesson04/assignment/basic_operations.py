"""
Basic operations module for database functionality.
"""

# pylint:disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=too-many-arguments
# pylint: disable=singleton-comparison
# pylint: disable=broad-except

import logging
from peewee import *
from customer_model import *

# Set up logger for program.
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler('db.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

logger.info('Logger is active.')

def add_customer(customer_id, first_name, last_name,
                 home_address, phone_number, email_address,
                 credit_limit, active_status):
    """Adds a new customer to the customer database."""

    try:
        with database.transaction():
            logger.info('Adding customer: %s, %s to the database...', last_name, first_name)
            new_customer = Customer.create(customer_id=customer_id,
                                           first_name=first_name,
                                           last_name=last_name,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           credit_limit=credit_limit,
                                           active_status=active_status)
            new_customer.save()

            logger.info('Customer: %s %s added to Customers database.', last_name, first_name)

    except TypeError:
        logger.info('Unable to add customer: %s, %s to the database.  Check input data. ', last_name, first_name)

def add_customers(customers):
    """Adds a list of customers to the database."""

    logger.info('Adding new customers to database...')
    new_customers = [add_customer(*customer) for customer in customers]
    logger.info('New customers upload complete.')
    return new_customers

def search_customer(customer_id):
    """Search for a customer in the database by customer_id and return their information."""

    try:
        logger.info('Searching for customer_id: %s', customer_id)
        query = Customer.get(Customer.customer_id == customer_id)

        result = {'first_name': query.first_name,
                  'last_name': query.last_name,
                  'email_address': query.email_address,
                  'phone_number': query.phone_number}
        return result

    except DoesNotExist as e:
        logger.info(e)
        logger.info('Customer ID %s does not exist.', customer_id)

        return {}

def search_customers(customer_ids):
    """Searchers for a list of customers in the database and returns that list."""
    logger.info('Searching for customer ids %s', customer_ids)
    query = [search_customer(customer_id) for customer_id in customer_ids]
    logger.info('Customer ids found with query.')
    return query

def delete_customer(customer_id):
    """Deletes a customer from a given customer id."""

    try:
        with database.transaction():
            logger.info('Deleting customer_id: %s...', customer_id)
            query = Customer.get(Customer.customer_id == customer_id)
            query.delete_instance()
            logger.info('Customer ID %s has been delted.', customer_id)
    except IndexError:
        logger.info('Customer ID %s does not exist.  Please try again.', customer_id)
        raise ValueError

def delete_customers(customer_ids):
    """Deletes customers from database from a list of ids."""

    logger.info('Dewleting customer_ids %s', customer_ids)
    return [delete_customer(customer_id) for customer_id in customer_ids]

def update_customer_credit(customer_id, credit_limit):
    """Updates the credit limit of a customer found by their customer id."""

    try:
        with database.transaction():
            logger.info('Finding customer ID: %s...', customer_id)
            query = Customer.get(Customer.customer_id == customer_id)
            query.credit_limit = credit_limit
            query.save()
            logger.info('Credit limit has been updated for customer ID %s.', customer_id)
    except IndexError:
        logger.info('Customer ID %s does not exist. Please enter valid customer ID.', customer_id)

def list_active_customers():
    """Function that returns an integer of the number of active customers."""

    query = Customer.select().where(Customer.active_status == True).count()

    return query
