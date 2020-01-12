"""
Basic database operations.
"""

import peewee as pw
from customer_model import Customer, DB
import logging

# Set up log file
logging.basicConfig(filename="db.log", format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M %p')


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

    # Create a new customer object
    with DB.transaction():
        try:
            cust = Customer.create(id=customer_id, name=name, last_name=lastname,
                                   address=home_address, phone=phone_number, email=email_address,
                                   status=status, credit_limit=credit_limit)
        except pw.IntegrityError as err:
            raise ValueError(err)
        else:
            cust.save()
            logging.info(f"Added customer with ID={customer_id}")


def search_customer(customer_id: int) -> dict:
    """
    Return a dictionary representing the customer with the given ID.
    :param customer_id: int, customer ID
    :return: dict
    """

    try:
        res = _get_by_id(customer_id)
    except pw.DoesNotExist:
        return {}
    else:
        return {'name': res.name, 'last_name': res.last_name, 'email': res.email,
                'phone': res.phone}


def delete_customer(customer_id: int):
    """
    Delete customer from database.

    :param customer_id: int, customer ID
    """

    try:
        res = _get_by_id(customer_id)
    except pw.DoesNotExist:
        pass
    else:
        res.delete_instance()
        logging.info(f"Deleted customer with ID={customer_id}")


def update_customer_credit(customer_id: int, credit_limit: float):
    """
    Updates an existing customer's credit limit. Raises a ValueError if no such
    customer exists.

    :param customer_id: int, customer ID
    :param credit_limit: float, new credit limit
    """

    try:
        res = _get_by_id(customer_id)
    except pw.DoesNotExist:
        raise ValueError(f"No customer with ID {customer_id}")
    else:
        with DB.transaction():
            res.credit_limit = credit_limit
            res.save()
        logging.info(f"Updated credit for customer with ID={customer_id")


def list_active_customers() -> int:
    """
    Return number of customers whose status is currently active.

    :return: int
    """

    return Customer.select().where(Customer.status).count()


def _get_by_id(cid: int) -> Customer:
    return Customer.get(Customer.id == cid)
