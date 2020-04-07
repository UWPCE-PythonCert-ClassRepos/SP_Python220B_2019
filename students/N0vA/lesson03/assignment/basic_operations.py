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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
