#!/usr/bin/env python3

"""
Script for handling data within Customer Model database
"""

# pylint: disable= W0614, R0913, C0103, W0401

import logging
import peewee
from Customer_Model_DB import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Started logger")


def add_customer(customer_id, customer_name, customer_last_name, customer_address,
                 customer_phone_number, customer_email, customer_status, customer_credit_limit):
    """ Adds customer to the database """

    try:
        logging.debug("Adding new customer: %s %s", customer_name, customer_last_name)
        with data.transaction():
            Customer.create(customer_id=customer_id,
                            customer_name=customer_name,
                            customer_last_name=customer_last_name,
                            customer_address=customer_address,
                            customer_phone_number=customer_phone_number,
                            customer_email=customer_email,
                            customer_status=customer_status,
                            customer_credit_limit=customer_credit_limit)
        logging.debug("%s %s added successfully", customer_name, customer_last_name)
    except IntegrityError:
        logging.error("Error adding customer: %s %s", customer_name, customer_last_name)
        raise IntegrityError


def search_customer(customer_id):
    """Finds customer in database"""

    try:
        return Customer.get(Customer.customer_id == customer_id)
    except peewee.DoesNotExist:
        logger.error("Customer does not exist")
        raise DoesNotExist

def delete_customer(customer_id):
    """Deletes a customer"""

    result = Customer.delete_by_id(customer_id)
    return result


def update_customer_credit(customer_id, customer_credit_limit):
    """Updates credit limit"""
    with data.transaction():
        try:
            customer_credit = Customer.get(Customer.customer_id == customer_id)
            customer_credit.customer_credit_limit = customer_credit_limit
            logger.info('Customer credit limit updated')
            customer_credit.save()
        except peewee.DoesNotExist as error:
            logger.info("Customer %s does not exist", customer_id)
            raise ValueError(error)


def list_active_customers():
    """Checks statuses of customers"""
    active_count = Customer.select().where(Customer.customer_status == 'active').count()
    logger.info("There are %s active customers in the database", active_count)
    return active_count


if __name__ == "__main__":
    data.create_tables([Customer])
