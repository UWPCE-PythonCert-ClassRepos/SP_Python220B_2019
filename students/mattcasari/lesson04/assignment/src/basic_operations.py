"""Basic Operations for the HP Norton Database"""

# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=too-many-arguments
# pylint: disable=broad-except

import logging
from src.customer_model import Customers

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = "db.log"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.INFO)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(logging.DEBUG)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


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
    LOGGER.info("Adding new customer, %s %s to database", name, last_name)
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
        LOGGER.info("Added new customer %s %s to database", name, last_name)
    except Exception as e_val:
        LOGGER.warning("Customer %s already exists", customer_id)
        LOGGER.warning(e_val)


def search_customer(customer_id):
    """
    This function returns a dictionary object with name, last_name, email address
    and phone number of a customer or an empty dictionary object if no customer was found.
    """
    LOGGER.info("Searching for customer ID# %s", customer_id)
    try:
        db_customer = Customers.get(Customers.customer_id == customer_id)
        data = {
            "name": db_customer.name,
            "last_name": db_customer.last_name,
            "email_address": db_customer.email_address,
            "phone_number": db_customer.phone_number,
        }
        LOGGER.info("Returning: {data}")
        return data
    except Exception as e_val:
        LOGGER.warning("No customer: %s", customer_id)
        LOGGER.warning(e_val)
        return {}


def delete_customer(customer_id):
    """
    This function deletes a customer from the sqlite3 database.
    """
    LOGGER.info("Deleting customer %s", customer_id)
    try:
        db_customer = Customers.get(Customers.customer_id == customer_id)
        db_customer.delete_instance()
        LOGGER.info("Customer %s deleted", customer_id)
    except Exception as e_val:
        LOGGER.warning(
            "Customer %s does not exist: Delete operation ignored", customer_id
        )
        LOGGER.warning(e_val)


def update_customer_credit(customer_id, credit_limit):
    """
    This function searches an existing customer by customer_id and update their credit limit
    or raise a ValueError exception if the customer does not exist.
    """
    LOGGER.info("Changing %s credit limit to %.2f", customer_id, credit_limit)
    try:
        db_customer = Customers.get(Customers.customer_id == customer_id)
        db_customer.credit_limit = credit_limit
        db_customer.save()
        LOGGER.info(
            "Successfully changed %s credit limit to %.2f", customer_id, credit_limit
        )
    except Exception as e_val:
        LOGGER.warning("Error updating %s credit limit", customer_id)
        LOGGER.warning(e_val)


def list_active_customers():
    """
    This function returns an integer with the number of customers whose status is currently active.
    """
    db_customers = Customers.select()
    LOGGER.debug("Calculating number of active customers")
    # Technically used this in Lesson 03, but it is a comprehension.  Another method added below.
    number_active = sum([int(x.status) for x in db_customers])
    LOGGER.info("There are %d active customers", number_active)

    return number_active


def list_active_emails():
    """
    This function returns a list of emails of only active customers in the database
    """
    db_customers = Customers.select().where(Customers.status)
    LOGGER.debug("Returning list of active customer emails")
    email_list = [x.email_address for x in db_customers]
    LOGGER.info("Email list: %s", email_list)
    return email_list
