#!/usr/env/bin python
"""This file contains basic operations for interaction with an sqlite3 database"""

import logging
import re
from database_models import Customer, database

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def _validate_phone_number(num: any) -> int:
    """validate the phone_number variable"""
    if not isinstance(num, int) and len(str(num)) != 10:
        m = re.findall(pattern=r'\D', string=str(num))
        if m:
            logger.error(f"The phone number should be exactly 10 digits.  Invalid chars: {m}")

        if len(str(num)) != 10:
            logger.error(f"The phone number should be exactly 10 digits.  Actual length: {len(num)}")

    try:
        return int(num)
    except Exception as e:
        logger.error(f"The phone number is invalid type.  Type={type(num)}.\n{e}")
        return 0


def _validate_active(active: any):
    """validate is type bool"""
    if isinstance(active, bool):
        return active
    else:
        logger.error(f"Invalid parameter: 'active' should be bool, got {type(active)} instead.")
        return False


def _validate_credit_limit(limit):
    try:
        return float(limit)
    except Exception as e:
        logger.error(f"Invalid parameter: 'credit_limit' is not numeric. {e}")
        return 0.


def add_customer(customer_id: str,
                 name: str,
                 lastname: str,
                 home_address: str,
                 phone_number: int,
                 email_address: str,
                 active: bool,
                 credit_limit: float) -> None:
    """This function will add a new customer to the sqlite3 database."""
    try:
        with database.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=_validate_phone_number(phone_number),
                email_address=email_address,
                active=_validate_active(active),
                credit_limit=_validate_credit_limit(credit_limit),
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
    except Exception:
        logger.error(f"Customer record not found: '{customer_id}'")

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
        cust = Customer.get_by_id(customer_id)
        cust.credit_limit = credit_limit
        cust.save()
        logger.info(f"Customer record {customer_id} credit limit updated to {credit_limit}")


def list_active_customers() -> tuple:
    """This function will return an integer with the number of
    customers whose status is currently active."""
    test = []
    try:
        with database.transaction():
            # NOTE:  MUST USE "==" (operator style testings).  Pythonic "is" fails
            for cust in Customer.select().where(Customer.active == True):
                test.append(search_customer(cust.customer_id))
                logger.info(f"Customer record is active for: {cust.customer_id}")

    except Exception as e:
        logger.error("Error searching records")
        logger.error(e)

    return tuple(test)
