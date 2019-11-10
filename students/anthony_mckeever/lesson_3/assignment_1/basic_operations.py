# Advanced Programming In Python - Lesson 3 Assigmnet 1: Relational Databases
# RedMine Issue - SchoolOps-13
# Code Poet: Anthony McKeever
# Start Date: 11/06/2019
# End Date: 11/09/2019

"""
Basic Operations for working with the Customers Database (customers.db)
"""

import logging

from peewee import IntegrityError
from peewee import OperationalError

from customer_db_schema import Customers


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(customer_id, first_name, last_name, address,
                 phone_number, email, status, credit_limit):
    """
    Add a customer to the database.

    :customer_id:       String representing the customer's ID
    :first_name:        String representing the customer's first name
    :last_name:         String representing the customer's last name
    :home_address:      String representing the customer's home address
    :phone_number:      String representing the customer's phone number
    :email_address:     String representing the customer's email address
    :status:            String representing the customer's state
                        (Accepted values "active" or "inactive")
    :credit_limit:      A decimal representing the customer's credit limit
    """
    if status.lower() not in ["active", "inactive"]:
        msg = "A customer's status can only be\"active\" or \"inactive\""
        raise ValueError(msg)

    try:
        current = Customers.get_or_create(customer_id=customer_id,
                                          first_name=first_name,
                                          last_name=last_name,
                                          home_address=address,
                                          phone_number=phone_number,
                                          email_address=email,
                                          status=status.lower(),
                                          credit_limit=credit_limit)
        LOGGER.info("Saved customer with ID: %s", current[0].customer_id)

    except (IntegrityError, OperationalError) as error:
        debug_dict = {"customer_id":   customer_id,
                      "first_name":    first_name,
                      "last_name":     last_name,
                      "home_address":  address,
                      "phone_number":  phone_number,
                      "email_address": email,
                      "status":        status,
                      "credit_limit":  credit_limit}

        LOGGER.info("Unable to save customer.")
        LOGGER.info("Parameters used: %s", debug_dict)
        LOGGER.error(error)


def search_customer(customer_id):
    """
    Look up a customer in the DB and return a dictionary of their contact
    information including first name, last_name, phone number, and email
    address.

    :customer_id:   String representing the customer's ID
    """
    cust_dict = {}
    try:
        customer = Customers.get_or_none(Customers.customer_id == customer_id)

        if customer is not None:
            cust_dict = customer.as_contact_info_dictionary()
        else:
            LOGGER.info("No customer exists with customer_id: %s", customer_id)
    except OperationalError as op_error:
        LOGGER.info("Failed look up of customer with customer_id: %s",
                    customer_id)
        LOGGER.error(op_error)

    return cust_dict


def delete_customer(customer_id):
    """
    Delete a customer from the database.

    :customer_id:   String representing the customer's ID
    """
    try:
        Customers.delete_by_id(customer_id)
        LOGGER.info("Customer deleted successfully.")
    except OperationalError as op_error:
        LOGGER.info("Failed to delete customer with customer_id: %s",
                    customer_id)
        LOGGER.error(op_error)


def update_customer_credit(customer_id, credit_limit):
    """
    Update a customer's credit limit.

    :customer_id:   String representing the customer's ID
    :credit_limit:  A decimal representing the customer's credit limit
    """
    try:
        customer = Customers.get_or_none(Customers.customer_id == customer_id)

        if customer is not None:
            limit = customer.credit_limit
            customer.credit_limit = credit_limit
            customer.save()

            msg = str("Credit limit updated from " +
                      f"{limit} to {customer.credit_limit}")
            LOGGER.info(msg)
        else:
            msg = f"No customer exists with customer_id: {customer_id}"
            LOGGER.info(msg)
            raise ValueError(msg)
    except (IntegrityError, OperationalError) as error:
        raise ValueError(error)


def list_active_customers():
    """
    Retur a count of active customers.
    """
    return Customers.select().where(Customers.status == "active").count()
