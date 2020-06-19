"""Basic op. module for database functionality"""
# pylint: disable=pointless-string-statement,too-many-arguments

import logging
from peewee import *
from customer_model import *

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("logger is set up")


def add_customer(customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit):
    """Create a new customer object in database"""
    try:
        with database.transaction():
            logger.info("adding customer: %s, %s to the database...", last_name, first_name)
            new_customer = Customer.create(customer_id=customer_id,
                                           first_name=first_name,
                                           last_name=last_name,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           status=status,
                                           credit_limit=credit_limit)
            new_customer.save()
            logger.info("adding customer: %s was successfull", first_name)

    except TypeError:
        logger.info("unable to add customer %s, %s to database", last_name, first_name)


def search_customer(customer_id):
    """search for customer in the database by their id number"""
    try:
        logger.info('searching for customer id: %s', customer_id)
        customer = Customer.get(Customer.customer_id == customer_id)
        customer_info = {'first_name': customer.first_name,
                         'last_name': customer.last_name,
                         'phone_number': customer.phone_number,
                         'email_address': customer.email_address}
        logger.info(customer_info)
        return customer_info
    except DoesNotExist as ex:
        logger.info(ex)
        logger.info('Customer ID %s does not exist', customer_id)
        return {}


def delete_customer(customer_id):
    """Deletes a customer from a given ID"""
    try:
        with database.transaction():
            logger.info("deleting customer id: %s....", customer_id)
            info = Customer.get(Customer.customer_id == customer_id)
            info.delete_instance()
            logger.info("customer ID %s has been deleted", customer_id)
    except IndexError:
        logger.info('Customer ID %s does not exist', customer_id)
        raise ValueError

def update_customer_credit(customer_id, credit_limit):
    """Update the credit limit of an existing customer"""
    try:
        with database.transaction():
            customer = Customer.get(Customer.customer_id == customer_id)
            customer.credit_limit = credit_limit
            customer.save()
            logger.info("Datatbase updated successfully")
    except IndexError:
        logger.info("customer ID provided does not exist")


def list_active_customers():
    """list all active customers"""
    active_count = Customer.select().where(Customer.status==True).count()
    return active_count
