#!/usr/bin/env python3

# Russell Felts
# Assignment 3

""" Basic database functionality """

# pylint: disable=too-many-arguments

import logging
from peewee import IntegrityError, DoesNotExist
from customer_model import DATABASE, Customer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(customer_id, name, last_name, home_address, phone_number,
                 email, status, credit_limit):
    """
    This function will add a new customer to the sqlite3 database.
    :param customer_id: integer representing a unique value that identifies a customer
    :param name: string containing the customer's first name
    :param last_name: string containing the customer's last name
    :param home_address: string containing the customer's address
    :param phone_number: string containing the customer's phone number
    :param email: string containing the customer's email address
    :param status: boolean representing the customer's status
    :param credit_limit: float containing the customer's credit limit
    :return:
    """
    try:
        with DATABASE.transaction():
            new_customer = Customer.create(customer_id=customer_id, name=name,
                                           last_name=last_name,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email=email,
                                           status=status,
                                           credit_limit=credit_limit)
            new_customer.save()
            LOGGER.info("A new customer record, %s %s, was added", name, last_name)
    except IntegrityError as integrity_error:
        LOGGER.error("A IntegrityError occurred %s", integrity_error)


def search_customer(customer_id):
    """
    Look up for a customer
    :param customer_id: Integer representing the customer ID
    :return: A dictionary object with name, last name, email address and phone number of a customer
    or an empty dictionary object if no customer was found.
    """
    LOGGER.info("Looking up customer ID %s:", customer_id)
    try:
        result_customer = Customer.get_by_id(customer_id)
        LOGGER.info("Found customer ID %s, %s %s", customer_id, result_customer.name,
                    result_customer.last_name)
        return {"name": result_customer.name, "last_name": result_customer.last_name,
                "email": result_customer.email,
                "phone_number": result_customer.phone_number}
    except DoesNotExist:
        LOGGER.info("Customer ID %s was not found.", customer_id)
        return {}


def delete_customer(customer_id):
    """
    Delete a customer from the database
    :param customer_id: Integer representing the customer id to be deleted
    """
    LOGGER.info("Deleting customer ID %s:", customer_id)
    if Customer.delete_by_id(customer_id):
        LOGGER.info("Customer ID %s was deleted.", customer_id)
    else:
        LOGGER.info("Customer ID %s was not found to be deleted.", customer_id)


def update_customer_credit(customer_id, credit_limit):
    """
    Search an existing customer by customer_id and update their credit limit or
    raise a ValueError exception if the customer does not exist
    :param customer_id: Integer representing the customer id
    :param credit_limit: Float representing the credit limit dollar amount
    :raise ValueError: Raised if the customer id does not exist
    """
    LOGGER.info("Updating credit limit for Customer ID %s", customer_id)
    try:
        result_customer = Customer.get_by_id(customer_id)
        with DATABASE.transaction():
            result_customer.credit_limit = credit_limit
            result_customer.save()
            LOGGER.info("Updating customer, %s %s's credit limit to %s",
                        result_customer.name, result_customer.last_name,
                        credit_limit)
    except DoesNotExist:
        LOGGER.info("Can not modify credit limit because customer ID %s doesn't exist.",
                    customer_id)
        raise ValueError


def list_active_customers():
    """
    Get the number of customers whose status is currently active
    :return Integer: The number of active customers
    """
    LOGGER.info("Fetching the number of active customers")
    return Customer.select().where(Customer.status).count()
