# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:47:37 2019

@author: Laura.Fiorentino
"""


import logging
from customer_model import *

logging.basicConfig(level=logging.WARNING)
LOGGER = logging.getLogger(__name__)

DATABASE = SqliteDatabase('customers.db')


def add_customer(customer_id, first_name, last_name, home_address,
                 phone_number, email_address, status, credit_limit):
    """ adds customer to database"""
    try:
        Customer.get_by_id(customer_id)
        return 'This customer ID is already in use'
    except Exception:
        try:
            with DATABASE.transaction():
                new_customer = Customer.create(customer_ID=customer_id,
                                               first_name=first_name,
                                               last_name=last_name,
                                               home_address=home_address,
                                               phone_number=phone_number,
                                               email_address=email_address,
                                               status=status,
                                               credit_limit=credit_limit)
                new_customer.save()
        except Exception as ex:
            if "CHECK constraint failed: customer" in str(ex):
                return 'Invalid Format'

def search_customer(customer_id):
    """ returns customer information from database"""
    try:
        customer_search = Customer.get_by_id(customer_id)
        if customer_search.status is True:
            status = 'Active'
        else:
            status = 'Inactive'
        customer_dict = {'Customer ID': customer_id,
                         'First Name': customer_search.first_name,
                         'Last Name': customer_search.last_name,
                         'Home Address': customer_search.home_address,
                         'Phone Number': customer_search.phone_number,
                         'Email Address': customer_search.email_address,
                         'Status': status,
                         'Credit Limit': customer_search.credit_limit}
        return customer_dict
    except Exception as ex:
        if "instance matching query does not exist" in str(ex):
            return('No record of customer with Customer ID {}'
                   .format(customer_id))


def delete_customer(customer_id):
    """ deletes customer from database"""
    customer_delete = Customer.get_by_id(customer_id)
    customer_delete.delete_instance()


def update_customer_credit(customer_id, new_credit_limit):
    """update credit limit"""
    customer_credit_update = Customer.get_by_id(customer_id)
    customer_credit_update.credit_limit = new_credit_limit
    customer_credit_update.save()


def list_active_customers():
    """return number of active customers"""
    customer_active = Customer.select().where(Customer.status == 'Active')
    print('{} Active Customers'.format(len(customer_active)))
    return len(customer_active)
