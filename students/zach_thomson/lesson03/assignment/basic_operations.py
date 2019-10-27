# pylint: disable=W0401, W0614, R0913
'''
basic operations for database
'''

import logging
from peewee import *
from customer_db_model import Customer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def add_customer(customer_id, name, last_name, home_address, phone_number,
                 email_address, status, credit_limit):
    '''function to add a new customer to the database'''
    new_customer = Customer.create(
        customer_id=customer_id,
        name=name,
        last_name=last_name,
        home_address=home_address,
        phone_number=phone_number,
        email_address=email_address,
        status=status,
        credit_limit=credit_limit
    )
    LOGGER.info('Added %s to the customer database', new_customer.name)
    new_customer.save()


def search_customer(customer_id):
    '''return a dictionary with customer information based on customer id'''
    search_dict = {}
    try:
        search = Customer.get(Customer.customer_id == customer_id)
        search_dict['name'] = search.name
        search_dict['last_name'] = search.last_name
        search_dict['email_address'] = search.email_address
        search_dict['phone_number'] = search.phone_number
        LOGGER.info('search_customer: Search completed')
        return search_dict
    except DoesNotExist:
        LOGGER.info('search_customer: Customer is not in the system')
        return search_dict


def delete_customer(customer_id):
    '''deletes a customer based on customer id'''
    try:
        deletion = Customer.get(Customer.customer_id == customer_id)
        LOGGER.info('Deleting %s from the customer database', deletion.customer_id)
        deletion.delete_instance()
        LOGGER.info('delete_customer: Customer successfully deleted')
    except DoesNotExist:
        LOGGER.info('Customer does not exist in the system')
        raise ValueError


def update_customer_credit(customer_id, credit_limit):
    '''updated customer credit limit based on customer id'''
    try:
        update_limit = Customer.get(Customer.customer_id == customer_id)
        update_limit.credit_limit = credit_limit
        LOGGER.info("%s's credit has succesfully been updated to %s",
                    update_limit.customer_id, update_limit.credit_limit)
        update_limit.save()
    except DoesNotExist:
        LOGGER.info('Customer does not exist in the system')
        raise ValueError


def list_active_customers():
    '''return an integer for the number of active customers'''
    count = 0
    for customer in Customer:
        if customer.status is True:
            count += 1
    return count
