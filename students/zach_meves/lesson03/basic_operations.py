"""
Basic database operations.
"""

import peewee


def add_customer(customer_id: int, name: str, lastname: str, home_address: str,
                 phone_number: str, email_address: str, status: bool, credit_limit: float):
    """
    Add a new customer to the database.

    :param customer_id: int, Customer ID
    :param name: str, First name
    :param lastname: str, Last name
    :param home_address: str, Home address
    :param phone_number: str, Phone number
    :param email_address: str, Email address
    :param status: bool, True for "active", False for "inactive"
    :param credit_limit: float, credit limit
    """

    pass


def search_customer(customer_id: int) -> dict:
    """
    Return a dictionary representing the customer with the given ID.
    :param customer_id: int, customer ID
    :return: dict
    """

    pass


def delete_customer(customer_id: int):
    """
    Delete customer from database.

    :param customer_id: int, customer ID
    """

    pass


def update_customer_credit(customer_id: int, credit_limit: float):
    """
    Updates an existing customer's credit limit. Raises a ValueError if no such
    customer exists.

    :param customer_id: int, customer ID
    :param credit_limit: float, new credit limit
    """

    pass


def list_active_customers() -> int:
    """
    Return number of customers whose status is currently active.

    :return: int
    """

    pass
