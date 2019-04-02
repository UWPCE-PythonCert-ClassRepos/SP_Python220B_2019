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
        LOGGER.warning('Error creating %s', customer_id)
        LOGGER.warning(ex)


def search_customer(customer_id):
    """ returns customer information from database"""
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
