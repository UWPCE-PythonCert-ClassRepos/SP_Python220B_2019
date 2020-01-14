"""Basic Operations of the customer database"""

#pylint: disable=unused-wildcard-import
#pylint: disable=wildcard-import
#pylint: disable=too-many-arguments

import logging
import peewee
from customer_model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def add_customer(customer_id, first_n, last_n, h_address, phone_num,
                 e_address, status, credit_limit):
    """given all the filds for a customer, this function will add the customer
    as an entry into the database"""
    try:
        with DATABASE.transaction():
            logging.info("Attempt to add customer %s", customer_id)
            new_customer = Customer.create(
                cust_id=customer_id,
                f_name=first_n,
                l_name=last_n,
                cust_h_address=h_address,
                cust_phone_num=phone_num,
                cust_e_address=e_address,
                cust_status=status,
                cust_credit_limit=credit_limit
                )
            new_customer.save()
            LOGGER.info('Added new customer %s %s', first_n, last_n)

    except peewee.IntegrityError as e_1:
        LOGGER.info(e_1)
        LOGGER.info('Customer id currently exists: %s', customer_id)
        raise IntegrityError

def search_customer(customer_id):
    """search the database by customer ID. return with rest of the data
    except DoesNotExist error and return blank dictionary"""
    try:
        LOGGER.info("Looking for %s in the Database", customer_id)
        acustomer = Customer.get(Customer.cust_id == customer_id)
        cust_info = {'first name': acustomer.f_name, 'last name': acustomer.l_name,
                     'email address': acustomer.cust_e_address,
                     'phone number': acustomer.cust_phone_num}
        return cust_info
    except peewee.DoesNotExist as e_2:
        LOGGER.info(e_2)
        LOGGER.info('Customer ID: %s, does not exist yet', customer_id)
        return {}

def delete_customer(customer_id):
    """get the customer with the id specified and remove it"""
    try:
        LOGGER.info("Looking for %s to delete in the Database", customer_id)
        acustomer = Customer.get(Customer.cust_id == customer_id)
        acustomer.delete_instance()

    except peewee.DoesNotExist as e_2:
        LOGGER.info(e_2)
        LOGGER.info('Customer ID %s, is not available to be deleted', customer_id)

def update_customer_credit(customer_id, credit_limit):
    """
    Update the credit limit for the requested customer.
    Params:
    cust_id = primary key identifying customer in the database
    credit_limit = new credit limit to be set for the customer
    """
    try:
        with DATABASE.transaction():
            acustomer = Customer.get(Customer.cust_id == customer_id)
            acustomer.cust_credit_limit = credit_limit
            acustomer.save()
            LOGGER.info('Customer credit limit updated to %s.', acustomer.cust_credit_limit)
    except peewee.DoesNotExist:
        LOGGER.info('%s is not in the database.', customer_id)
        raise ValueError

def list_active_customers():
    """
    This function will return an integer with the number of
    customers whose status is currently active
    """
    active_custs = Customer.select().where(Customer.cust_status == 'Active').count()
    LOGGER.info('There are %i active customers in the database.', active_custs)
    return active_custs
