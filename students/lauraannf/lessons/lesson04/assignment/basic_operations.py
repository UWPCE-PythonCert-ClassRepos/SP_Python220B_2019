# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:47:37 2019

@author: Laura.Fiorentino
"""

import logging
from customer_model import Customer

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setFormatter(FORMATTER)
LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.INFO)


def add_customer(customer_id, first_name, last_name, home_address,
                 phone_number, email_address, status, credit_limit):
    """ adds customer to database"""
    print('Adding new customer, Customer ID {}...'.format(customer_id))
    try:
        Customer.get_by_id(customer_id)
        print('Customer ID {} is already in use'.format(customer_id))
    except Exception:
        try:
            new_customer = Customer.create(customer_ID=customer_id,
                                           first_name=first_name,
                                           last_name=last_name,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           status=status,
                                           credit_limit=credit_limit)
            new_customer.save()
            LOGGER.info('Added new customer, Customer ID %s', customer_id)
        except Exception as ex:
            if "CHECK constraint failed: customer" in str(ex):
                print('Incorrect format, customer {} not saved'
                      .format(customer_id))


def search_customer(customer_id):
    """ returns customer information from database"""
    print('Searching for customer, Customer ID {}...'.format(customer_id))
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
        print('Info for Customer ID {}'.format(customer_id))
        return customer_dict
    except Exception as ex:
        if "instance matching query does not exist" in str(ex):
            print('No record of customer with Customer ID {}'
                  .format(customer_id))
        else:
            print('unknown error')


def delete_customer(customer_id):
    """ deletes customer from database"""
    print('Deleting customer with ID {}...'.format(customer_id))
    try:
        customer_delete = Customer.get_by_id(customer_id)
        customer_delete.delete_instance()
        LOGGER.info('Customer with Customer ID %s has been deleted',
                    customer_id)
    except Exception as ex:
        if "instance matching query does not exist" in str(ex):
            print('No record of customer with Customer ID {}'
                  .format(customer_id))
            print('No customer deleted')
        else:
            print('unknown error')


def update_customer_credit(customer_id, new_credit_limit):
    """update credit limit"""
    print('Updating customer with ID {}...'.format(customer_id))
    try:
        customer_credit_update = Customer.get_by_id(customer_id)
        customer_credit_update.credit_limit = new_credit_limit
        customer_credit_update.save()
        LOGGER.info('Customer with ID %s has been updated', customer_id)
    except Exception as ex:
        if "instance matching query does not exist" in str(ex):
            print('No record of customer with Customer ID {}'
                  .format(customer_id))
            print('No customer updated')
        else:
            print('unknown error')


def list_active_customers():
    """return number of active customers"""
    customer_active = Customer.select().where(Customer.status == 'Active')
    print('{} Active Customers'.format(len(customer_active)))
    return len(customer_active)
