#!/usr/bin/env python3
"""
Basic operations
"""
import logging
import peewee
from customer_schema import Customer
import datetime

log_file = 'basic_operations' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
log_format = "%(asctime)s%(filename)s:%(lineno)-3d%(levelname)s %(message)s"
formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.WARNING)
file_handler.setLevel(logging.WARNING)
console_handler.setLevel(logging.WARNING)


def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    """
    This function will add a new customer to the sqlite3 database.
    """
    try:
        new_customer = Customer.create(
            customer_id=customer_id,
            name=name,
            lastname=lastname,
            home_address=home_address,
            phone_number=phone_number,
            email_address=email_address,
            status=status,
            credit_limit=credit_limit
        )
        new_customer.save()
    except peewee.IntegrityError:
        logger.warning("Tried to add a customer_id that already exists")


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
