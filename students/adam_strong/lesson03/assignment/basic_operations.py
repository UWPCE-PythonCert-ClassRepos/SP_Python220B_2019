#!/usr/bin/env python
"""
Model to interact with customers.db
for use by all departments at HP Norton
pylintrc file: disabled - invalid-name(for snake casing), wildcard-import,
unused-wildcard-import, too-few-public-methods, not-an-iterable
"""

import logging
import pathlib
import peewee
from playhouse.shortcuts import model_to_dict
from customer_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('basic_operations.py is at work')

FIRST_NAME = 0
LAST_NAME = 1
HOME_ADDRESS = 2
PHONE_NUMBER = 3
EMAIL_ADDRESS = 4
IS_ACTIVE = 5
CREDIT_LIMIT = 6

REPORT_STRING = 'ID#{:5}:::{:20} P: {:9}, E: {:20}, Active:{:1}, Limit:{:8}'

def add_customer(customer_tuple):
    ''' This function will add a new customer to the sqlite3 database.'''
    logger.info('In add customer function')

    with database.transaction():
        new_customer = Customers.create(first_name=customer_tuple[FIRST_NAME],
                                        last_name=customer_tuple[LAST_NAME],
                                        home_address=customer_tuple[HOME_ADDRESS],
                                        phone_number=customer_tuple[PHONE_NUMBER],
                                        email_address=customer_tuple[EMAIL_ADDRESS],
                                        is_active=customer_tuple[IS_ACTIVE],
                                        credit_limit=customer_tuple[CREDIT_LIMIT])

        new_customer.save()
        logger.info('Adding new customer: %s', str(new_customer))
        logger.info('Added %s %s to database', new_customer.first_name, new_customer.last_name)
        return model_to_dict(new_customer)


def search_customer(customer_id):
    ''' This function will return customer info based on a customer_id.'''
    logger.info('Searching for customer #%s', str(customer_id))

    with database.transaction():
        try:
            c = Customers.get(Customers.customer_id == customer_id)
            logger.info(model_to_dict(c))
            return {'first_name': c.first_name, 'last_name': c.last_name,
                    'email_address': c.email_address, 'phone_number': c.phone_number}
        except (IndexError, peewee.DoesNotExist):
            return {}


def delete_customer(customer_id):
    '''This function will delete a customer from the sqlite3 database.'''
    logger.info('Deleting customer #%s', str(customer_id))

    with database.transaction():
        c = Customers.get(Customers.customer_id == customer_id)
        logger.info('Deleting %s %s from the database', c.first_name, c.last_name)
        c.delete_instance()



def update_customer(customer_id, credit_limit):
    '''This function will search an existing customer by customer_id and update
    their credit limit or raise a ValueError exception if the customer does not exist.'''
    logger.info('Modifying customer #%s credit limit to %s', customer_id, credit_limit)

    with database.transaction():
        try:
            c = Customers.get(Customers.customer_id == customer_id)
            logger.info('%s %slimit is now %s', c.first_name, c.last_name, credit_limit)
            c.credit_limit = credit_limit
            c.save()
            return {'first_name': c.first_name, 'last_name': c.last_name,
                    'email_address': c.email_address, 'credit_limit': c.credit_limit}
        except:
            raise ValueError('No customer with this ID, use list_all_customers()')


def list_active_customers():
    '''This function will return an integer with the current number of active customers.'''
    query = Customers.select(fn.COUNT(Customers.customer_id)).where(Customers.is_active == 1)
    count = query.scalar()
    logger.info('There are a total of %s active customers', str(count))
    return count


def list_all_customers():
    '''This function returns a list of lists of all the customers'''
    cust_list = []
    for c in Customers:
        fullname = c.first_name + ' ' + c.last_name + ','
        formlist = REPORT_STRING.format(c.customer_id, fullname, c.phone_number,
                                        c.email_address, c.is_active, c.credit_limit)
        logger.info(formlist)
        cust_list.append([formlist])
    return cust_list


if __name__ == '__main__':
    testpth = pathlib.Path('./')
    testdest = testpth.absolute() / 'customers.db'
    logging.info('Creating Database')
    database.create_tables([Customers])
    #database.close()
