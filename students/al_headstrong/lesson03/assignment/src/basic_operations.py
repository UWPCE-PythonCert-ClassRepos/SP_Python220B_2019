"""
    This module contains functions to use and manipulate the customer database.
"""
# pylint: disable=unused-import, unused-wildcard-import,
# pylint: disable=too-few-public-methods, too-many-arguments, wildcard-import

import logging
from customer_model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(customer_id,
                 name,
                 lastname,
                 home_address,
                 phone_number,
                 email_address,
                 status,
                 credit_limit):
    """This function adds customer data to 'customer.db' database."""

    try:
        with DATABASE.transaction():
            new_customer = Customer.create(customer_id=customer_id,
                                           name=name,
                                           lastname=lastname,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           status=status,
                                           credit_limit=credit_limit)
            new_customer.save()
            LOGGER.info('Database add successful')

    except Exception as error:
        LOGGER.info('Error creating = Customer %s', customer_id)
        LOGGER.info(error)
        raise error


def search_customer(customer_id):
    """Return dict with customer data based on customer_id."""
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer_dict = {'customer_id': customer.customer_id,
                         'name': customer.name,
                         'lastname': customer.lastname,
                         'home_address': customer.home_address,
                         'phone_number': customer.phone_number,
                         'email_address': customer.email_address,
                         'status': customer.status,
                         'credit_limit': customer.credit_limit}
    except DoesNotExist as error:
        LOGGER.info('Could not find = Customer %s', customer_id)
        LOGGER.info(error)
        customer_dict = {}

    return customer_dict


def delete_customer(customer_id):
    """Delete customer from database from customer_id."""
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.delete_instance()
    except DoesNotExist as error:
        LOGGER.info('Could not find = Customer %s', customer_id)
        LOGGER.info(error)
        raise error


def update_customer_credit(customer_id, new_credit_limit):
    """Change credit_limit at customer_id to new_credit_limit."""
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.credit_limit = new_credit_limit
        customer.save()
    except DoesNotExist as error:
        LOGGER.info('Could not find = Customer %s', customer_id)
        LOGGER.info(error)
        raise ValueError


def list_active_customers():
    """Return integer value of number of active customers in list."""
    query = Customer.select().where(Customer.status == 'active')
    return len(query)
