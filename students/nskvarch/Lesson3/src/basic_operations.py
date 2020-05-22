# Lesson 3 Assignment HP Norton Furniture customer database, created by Niels Skvarch
"""Module for manipulation of the database created from the customer model.
 Includes functions for adding, removing, searching through and updating the records"""

import logging
import datetime
from peewee import *
from src.customer_model import Customer

# Logging set up to log only defined information statements as the program runs
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)
log_file = datetime.datetime.now().strftime("%Y-%m-%d")+"bas_op.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


def add_customer(customer_id, first_name, last_name, mailing_address, phone_number,
                 email_address, active_status, credit_limit):
    """Add a new customer to the database"""
    try:
        new_customer = Customer.create(customer_id=customer_id, first_name=first_name,
                                       last_name=last_name, mailing_address=mailing_address,
                                       phone_number=phone_number, email_address=email_address,
                                       active_status=active_status, credit_limit=credit_limit)
        new_customer.save()
        logging.info(f"Add new customer with id {customer_id} -OK")
    except TypeError as oops:
        logging.info(f"Add new customer with id of {customer_id} failed")
        logging.info(oops)
        raise oops


def search_customer(customer_id):
    """use customer ID to return a dictionary object with the first name,
     last name, email address and phone number of that customer"""
    try:
        customer_found = Customer.get(Customer.customer_id == customer_id)
        logging.info(f"Customer found with id of {customer_id}")
        return {"first_name": customer_found.first_name,
                "last_name": customer_found.last_name,
                "email_address": customer_found.email_address,
                "phone_number": customer_found.phone_number}
    except DoesNotExist:
        logging.info(f"Customer id {customer_id} does not exist")
        logging.info(DoesNotExist)
        return {}


def delete_customer(customer_id):
    """use customer ID to find and delete a customer from the database"""
    try:
        remove_customer = Customer.get(Customer.customer_id == customer_id)
        remove_customer.delete_instance()
        logging.info(f"Customer {customer_id} was found, deleting from the database")
    except DoesNotExist:
        logging.info(f"Customer with id {customer_id} does not exist")
        logging.info(DoesNotExist)
        raise DoesNotExist


def update_customer_credit(customer_id, credit_limit):
    """Use customer ID to update the customer credit limit record"""
    try:
        update_customer = Customer.get(Customer.customer_id == customer_id)
        update_customer.credit_limit = credit_limit
        update_customer.save()
        logging.info(f"Customer with id of {customer_id} has had their credit limit changed to {credit_limit}")
    except DoesNotExist:
        logging.info(f"Customer with id {customer_id} does not exist")
        logging.info(DoesNotExist)
        raise DoesNotExist


def list_active_customers():
    """Give a count of only active status customers in the database"""
    active_customers = Customer.select().where(Customer.active_status).count()
    logging.info(f"The number of active customers is {active_customers}")
    return active_customers
