"""
Basic operations for HP Norton database
"""
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=too-many-arguments
# pylint: disable=logging-fstring-interpolation

import logging
import peewee
from customer_model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("Started logger")


def add_customer(**kwargs):
    """Adding customer to database"""
    try:
        with database.transaction():
            new_customer = Customer.create(**kwargs)
            new_customer.save()
            LOGGER.info(f"New customer {kwargs['customer_id']} saved.")
    except peewee.IntegrityError:
        LOGGER.error("Customer id {kwargs['customer_id']} is already in use.")
        raise
    except Exception as ex:
        LOGGER.error(ex)
        raise
    return new_customer


def search_customer(customer_id):
    """Find customer in database and return dictionary or empty dictionary"""

    try:
        query = Customer.get(Customer.customer_id == customer_id)
        return {'customer_name': query.customer_name,
                'customer_last_name': query.customer_last_name,
                'customer_email': query.customer_email,
                'customer_phone_number': query.customer_phone_number}

    except peewee.DoesNotExist:
        LOGGER.error("Customer does not exist")
        return {}


def delete_customer(customer_id):
    """Delete a customer"""

    result = Customer.delete_by_id(customer_id)
    return result


def update_customer_credit(customer_id, customer_credit_limit):
    """Updates customer credit limit)"""
    with database.transaction():
        try:
            cust = Customer.get(Customer.customer_id == customer_id)
            cust.customer_credit_limit = customer_credit_limit
            LOGGER.info('Customer credit limit updated')
            cust.save()
        except peewee.DoesNotExist as ex:
            LOGGER.info(f"Customer {customer_id} does not exist")
            raise ValueError(ex)


def list_active_customers():
    """Checks for active customer status"""
    result = Customer.select().where(Customer.customer_status).count()
    LOGGER.info(f"There are {result} active customers in the database")
    return result
