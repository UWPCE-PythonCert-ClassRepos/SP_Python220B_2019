#!/usr/bin/env python3
"""
Basic operations
"""


def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    """
    This function will add a new customer to the sqlite3 database.
    """
    pass


def search_customer(customer_id):
    """
    This function will return a dictionary object with name, lastname, email address
    and phone number of a customer or an empty dictionary object if no customer was found.
    """
    pass


def delete_customer(customer_id):
    """
    This function will delete a customer from the sqlite3 database.
    """
    pass


def update_customer_credit(customer_id, credit_limit):
    """
    This function will search an existing customer by customer_id and update
    their credit limit or raise a ValueError exception if the customer does not exist.
    """
    pass


def list_active_customers():
    """
    This function will return an integer with the number of customers whose status is
    currently active.
    """
    pass
