"""
    Defines the basic operations needed to operate and maintain a customer database in sqlite3.
        -add new customers to the database
        -search customers in the database
        -delete existing customers from the database
        -update customers credit
        -list the number of active customers in the database

    Uses logging to capture messages.
"""

from peewee import *
import logging


def add_customer(customer_id, name, lastname, home_address, phone_number, email_address, status,
                 credit_limit):
    """
        Adds a new customer to the database. Throw an exception if the customer already exists.
        Checks the input data to ensure its valid.
        Customer ID is used as the primary  key.
    """
    pass


def search_customer(customer_id):
    """
        Searches the database of existing customers. Returns a dictionary with customer information.
        An empty dictionary is returned if the customer does not exist in the database.

        :param customer_id: primary key used to search the database
        :return: dict{name, lastname, email_address, phone_number}
    """
    pass


def delete_customer(customer_id):
    """
        Deletes an existing customer from the database. A warning message is printed if the
        customer does not exist in the databse.
    """
    pass


def update_customer_credit(customer_id):
    """
        Updates a customers credit limit in the database. A ValueError expection is thrown if the
        customer does not exist in the database.
    """
    pass


def list_active_customers():
    """
        Returns an integer with the number of customers whose status is active in the database.
    """
    pass
