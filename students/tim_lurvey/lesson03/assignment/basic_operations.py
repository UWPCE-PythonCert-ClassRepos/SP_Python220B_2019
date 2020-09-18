#!/usr/env/bin python
""" Documentation for {file}
This file contains basic operations for interaction with an sqlite3 database""".format(file=__file__)

import logging
from peewee import *
from database_models import *

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def add_customer(customer_id, name, lastname, home_address, phone_number, email_address, status, credit_limit):
    """This function will add a new customer to the sqlite3 database."""
    try:
        with database.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status,
                credit_limit=credit_limit,
            )
            new_customer.save()
            logger.info(f'Customer record created: {customer_id}')

    except Exception as e:
        logger.info(f'Customer record creation failed: {customer_id}')
        logger.info(e)

    
def search_customer(customer_id: str) -> dict:
    """This function will return a dictionary object with name, lastname, email address
    and phone number of a customer or an empty dictionary object if no customer was found."""
    answer = {}
    try:
        with database.transaction():
            customer_record = Customer.get_by_id(customer_id)
            answer = customer_record.__dict__.get("__data__")
    except Exception as e:
        logger.error(f"Customer record not found: {customer_id}")
        logger.error(e)

    return answer


def delete_customer(customer_id: str) -> None:
    """This function will delete a customer from the sqlite3 database."""
    # test if customer exists, simplify logic below
    if search_customer(customer_id):
        Customer.get_by_id(customer_id).delete_instance()
        logger.info(f"Customer record deleted for: {customer_id}")


def update_customer_credit(customer_id: str, credit_limit: float) -> None:
    """This function will search an existing customer by customer_id
    and update their credit limit or raise a ValueError exception if
    the customer does not exist."""
    if search_customer(customer_id):
        Customer.get_by_id(customer_id).credit_limit = credit_limit
        logger.info(f"Customer record credit limit updated to {credit_limit} for: {customer_id}")


def list_active_customers() -> tuple:
    """This function will return an integer with the number of
    customers whose status is currently active."""
    test = []
    try:
        with database.transaction():
            test.append(Customer.select().where(Customer.status is True))
            for cust in Customer.select().where(Customer.status is True):
                logger.info(f"Customer record is active for: {cust.customer_id}")

    except Exception as e:
        logger.error(f"Error searching records")
        logger.error(e)

    return tuple(test)
