"""Basic Operations for the HP Norton Database"""

# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=too-many-arguments
# pylint: disable=broad-except

import logging
from src.customer_model import Customers, DATABASE

try:
    logging.info("Creating tables in database")
    DATABASE.create_tables([Customers])
except Exception as e_val:
    logging.info("Could not create tables")
    logging.info(e_val)


def add_customer(
        customer_id,
        name,
        last_name,
        home_address,
        phone_number,
        email_address,
        status,
        credit_limit,
):
    """
    This function adds a new customer to the sqlite3 database.
    """
    logging.debug("Adding new customer, %s %s to database", name, last_name)
    try:
        Customers.create(
            customer_id=customer_id,
            name=name,
            last_name=last_name,
            home_address=home_address,
            phone_number=phone_number,
            email_address=email_address,
            status=status,
            credit_limit=credit_limit,
        )
    except Exception as e_val:
        logging.warning("Customer %s already exists", customer_id)
        logging.warning(e_val)


def search_customer(customer_id):
    """
    This function returns a dictionary object with name, last_name, email address
    and phone number of a customer or an empty dictionary object if no customer was found.
    """
    logging.info("Searching for customer ID# %s", customer_id)
    try:
        db_customer = Customers.get(Customers.customer_id == customer_id)
        return {
            "name": db_customer.name,
            "last_name": db_customer.last_name,
            "email_address": db_customer.email_address,
            "phone_number": db_customer.phone_number,
        }
    except Exception as e_val:
        logging.warning("No customer: %s", customer_id)
        logging.warning(e_val)
        return {}


def delete_customer(customer_id):
    """
    This function deletes a customer from the sqlite3 database.
    """
    logging.info("Deleting customer %s", customer_id)
    try:
        logging.info("Customer %s deleted", customer_id)
        db_customer = Customers.get(Customers.customer_id == customer_id)
        db_customer.delete_instance()
    except Exception as e_val:
        logging.warning(
            "Customer %s does not exist: Delete operation ignored", customer_id
        )
        logging.warning(e_val)


def update_customer_credit(customer_id, credit_limit):
    """
    This function searches an existing customer by customer_id and update their credit limit
    or raise a ValueError exception if the customer does not exist.
    """
    logging.info("Changing %s credit limit to %.2f", customer_id, credit_limit)
    try:
        db_customer = Customers.get(Customers.customer_id == customer_id)
        db_customer.credit_limit = credit_limit
        db_customer.save()
    except Exception as e_val:
        logging.warning("Error updating %s credit limit", customer_id)
        logging.warning(e_val)


def list_active_customers():
    """
    This function returns an integer with the number of customers whose status is currently active.
    """
    db_customers = Customers.select()

    return sum([int(x.status) for x in db_customers])
