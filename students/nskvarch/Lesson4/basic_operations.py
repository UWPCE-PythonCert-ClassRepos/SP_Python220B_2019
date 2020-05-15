# Lesson 3 Assignment HP Norton Furniture customer database, created by Niels Skvarch
"""Module for manipulation of the database created from the customer model.
 Includes functions for adding, removing, searching through and updating the records"""

import logging
import datetime
from peewee import *
from customer_model import Customer

# Logging set up to log only defined information statements as the program runs
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+"error.log"
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER2 = logging.FileHandler("db.log")
FILE_HANDLER2.setLevel(logging.INFO)
FILE_HANDLER2.setFormatter(FORMATTER)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(FILE_HANDLER2)


def add_customer(customer_id, first_name, last_name, mailing_address, phone_number,
                 email_address, active_status, credit_limit):
    """Add a new customer to the database"""
    try:
        new_customer = Customer.create(customer_id=customer_id, first_name=first_name,
                                       last_name=last_name, mailing_address=mailing_address,
                                       phone_number=phone_number, email_address=email_address,
                                       active_status=active_status, credit_limit=credit_limit)
        new_customer.save()
        logging.info("Add new customer with id %s -OK", customer_id)
    except TypeError as oops:
        logging.debug("Add new customer with id of %s failed", customer_id)
        logging.debug(oops)
        raise oops


def search_customer(customer_id):
    """use customer ID to return a dictionary object with the first name,
     last name, email address and phone number of that customer"""
    try:
        customer_found = Customer.get(Customer.customer_id == customer_id)
        logging.info("Customer found with id of %s", customer_id)
        return {"first_name": customer_found.first_name,
                "last_name": customer_found.last_name,
                "email_address": customer_found.email_address,
                "phone_number": customer_found.phone_number}
    except DoesNotExist:
        logging.debug("Customer id %s does not exist", customer_id)
        logging.debug(DoesNotExist)
        return {}


def delete_customer(customer_id):
    """use customer ID to find and delete a customer from the database"""
    try:
        remove_customer = Customer.get(Customer.customer_id == customer_id)
        remove_customer.delete_instance()
        logging.info("Customer %s was found, deleting from the database", customer_id)
    except DoesNotExist:
        logging.debug("Customer with id %s does not exist", customer_id)
        logging.debug(DoesNotExist)
        raise DoesNotExist


def update_customer_credit(customer_id, credit_limit):
    """Use customer ID to update the customer credit limit record"""
    try:
        update_customer = Customer.get(Customer.customer_id == customer_id)
        update_customer.credit_limit = credit_limit
        update_customer.save()
        logging.info("Customer with id of %s has had their credit limit changed to %s",
                     customer_id, credit_limit)
    except DoesNotExist:
        logging.debug("Customer with id %s does not exist", customer_id)
        logging.debug(DoesNotExist)
        raise DoesNotExist


def list_active_customers():
    """Give a count of only active status customers in the database"""
    active_customers = Customer.select().where(Customer.active_status).count()
    logging.info("The number of active customers is %s", active_customers)
    return active_customers


def active_customer_sales_calls():
    """Return a list of active customer names and phone numbers for sales calls"""
    customers_to_call = Customer.select().where(Customer.active_status)
    customer_count = list_active_customers()
    logging.info("Getting %s records for sales call query", customer_count)
    return [f"{i.first_name} {i.last_name} {i.phone_number}" for i in customers_to_call]


def active_customer_credit_query(credit_limit_min):
    """Return a list of customers at or above a certain credit limit"""
    customer_credit_list = Customer.select().where(Customer.active_status)
    logging.info("Getting records for a credit query with a limit at or above %s", credit_limit_min)
    return [f"{i.first_name} {i.last_name} {i.phone_number}" for i in customer_credit_list
            if i.credit_limit >= credit_limit_min]
