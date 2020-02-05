from customer_model import *
import logging


def add_customer(
    customer_id,
    name,
    lastname,
    home_address,
    phone_number,
    email_address,
    status,
    credit_limit,
):
    """
    This function adds a new customer to the sqlite3 database.
    """
    logging.debug(f"Adding new customer, {name} {lastname}, to database")
    pass


def search_customer(customer_id):
    """
    This function will return a dictionary object with name, lastname, email address 
    and phone number of a customer or an empty dictionary object if no customer was found.
    """
    pass


def delete_customer(customer_id):
    """
    This function deletes a customer from the sqlite3 database.
    """
    logging.warning(f"Deleting customer {customer_id}")
    pass


def update_customer_credit(customer_id, credit_limit):
    """
    This function searches an existing customer by customer_id and update their credit limit
    or raise a ValueError exception if the customer does not exist.
    """
    logging.debug(f"Changing {customer_id} credit limit to {credit_limit:.2f}")
    pass


def list_active_customers():
    """
    This function returns an integer with the number of customers whose status is currently active.
    """
    pass
