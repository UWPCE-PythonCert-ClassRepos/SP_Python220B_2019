#!/usr/bin/env python3

"""
Script for handling data within Customer Model database
"""

# pylint: disable= W0614, R0913, C0103, W0401, W0621

import logging
import peewee
from Customer_Model_DB import *


def logger_setup():
    """A function to format the logging parameters"""

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = "db.log"
    formatter = logging.Formatter(log_format)
    logger = logging.getLogger()

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.ERROR)


def add_customer(customer_id, customer_name, customer_last_name, customer_address,
                 customer_phone_number, customer_email, customer_status, customer_credit_limit):
    """ Adds customer to the database """

    try:
        logging.info("Adding new customer: %s %s", customer_name, customer_last_name)
        with data.transaction():
            Customer.create(customer_id=customer_id,
                            customer_name=customer_name,
                            customer_last_name=customer_last_name,
                            customer_address=customer_address,
                            customer_phone_number=customer_phone_number,
                            customer_email=customer_email,
                            customer_status=customer_status,
                            customer_credit_limit=customer_credit_limit)
        logging.info("%s %s added successfully", customer_name, customer_last_name)
    except peewee.IntegrityError:
        logging.error("Error adding customer: %s %s", customer_name, customer_last_name)
        raise peewee.IntegrityError


def search_customer(customer_id):
    """Finds customer in database"""

    try:
        return Customer.get(Customer.customer_id == customer_id)
    except peewee.DoesNotExist:
        logging.error("Customer does not exist")
        raise peewee.DoesNotExist


def delete_customer(customer_id):
    """Deletes a customer"""
    try:
        logging.info("Deleting customer with customer_id: %s", customer_id)
        result = Customer.delete_by_id(customer_id)
        return result
    except peewee.DoesNotExist:
        logging.debug("Cannot find customer with ID: %s", customer_id)
        raise peewee.DoesNotExist


def update_customer_credit(customer_id, customer_credit_limit):
    """Updates credit limit"""
    with data.transaction():
        try:
            customer_credit = Customer.get(Customer.customer_id == customer_id)
            customer_credit.customer_credit_limit = customer_credit_limit
            logging.info('Customer credit limit updated for customer ID: %s', customer_id)
            customer_credit.save()
        except peewee.DoesNotExist as error:
            logging.info("Customer %s does not exist", customer_id)
            raise ValueError(error)


def list_active_customers():
    """Checks statuses of customers"""
    # New version of active_count for week 4
    # active_count= Customer.select().where(Customer.customer_status == 'active').count()
    active_count = sum(1 for x in Customer.select().where(Customer.customer_status == 'active'))
    logging.info("There are %s active customers in the database", active_count)
    return active_count


if __name__ == "__main__":
    logger_setup()
    data.create_tables([Customer])
