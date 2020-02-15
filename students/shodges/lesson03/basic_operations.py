# pylint: disable=unused-import, singleton-comparison

"""This module defines the standard set of CRUD operations for the Customer database."""

import logging
from customer_model import CUSTOMER_DB, Customer, DoesNotExist, IntegrityError

CUSTOMER_DB.create_tables([Customer])

def add_customer(**kwargs):
    """
    This takes the specified dictionary and attempts to create a new customer record.

    Returns True on successful creation; otherwise, returns False.
    """
    with CUSTOMER_DB.transaction():
        try:
            new_customer = Customer.create(**kwargs)
        except IntegrityError:
            return False
        else:
            new_customer.save()
            return True

def search_customer(customer_id):
    """
    This function returns the Customer record for the specified customer_id, if found.

    If no Customer record is found, it will raise a ValueError.
    """
    customer = Customer.select().where(Customer.customer_id == customer_id).dicts()
    customer_record = customer.first()
    if customer_record is None:
        return {}

    return customer_record

def delete_customer(customer_id):
    """
    This function will attempt to delete the Customer record for the specified customer_id.

    Returns True if successful; otherwise, returns False.
    """
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.delete_instance()
        return True
    except (IndexError, DoesNotExist):
        return False

def update_customer_credit(customer_id, credit_limit):
    """
    This function will attempt to update the credit_limit value for the specified customer_id.

    Returns True if successful; otherwise, returns False.
    """
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
        return True
    except (IndexError, DoesNotExist):
        return False


def list_active_customers():
    """
    This function will return the count of active customers.
    """
    return Customer.select().where(Customer.is_active == True).count()


CUSTOMER_DB.close()
