#!/usr/bin/env python
"""
Lesson 04 - Assingment
Model to interact with customers.db
for use by all departments at HP Norton
pylintrc file: disabled - wildcard-import,
unused-wildcard-import, too-few-public-methods

v2 - Refactored code to implement modified logging,
     iterators and comprehensions
"""

import logging
import pathlib
import peewee
from playhouse.shortcuts import model_to_dict
from customer_model import *

logger = logging.getLogger()
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('db.log')
file_handler.setLevel(logging.INFO)

file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.debug('basic_operations.py has been run')


FIRST_NAME = 0
LAST_NAME = 1
HOME_ADDRESS = 2
PHONE_NUMBER = 3
EMAIL_ADDRESS = 4
IS_ACTIVE = 5
CREDIT_LIMIT = 6

REPSTR = 'ID#{:5}:::{:20} P: {:9}, E: {:20}, Active:{:1}, Limit:{:8}'

def add_customer(customer_tuple):
    ''' This function will add a new customer to the sqlite3 database.'''
    logger.debug('In add customer function')

    with database.transaction():
        new_customer = Customers.create(first_name=customer_tuple[FIRST_NAME],
                                        last_name=customer_tuple[LAST_NAME],
                                        home_address=customer_tuple[HOME_ADDRESS],
                                        phone_number=customer_tuple[PHONE_NUMBER],
                                        email_address=customer_tuple[EMAIL_ADDRESS],
                                        is_active=customer_tuple[IS_ACTIVE],
                                        credit_limit=customer_tuple[CREDIT_LIMIT])

        new_customer.save()
        logger.debug('Adding new customer: %s', str(new_customer))
        logger.info('Added %s %s (ID: %d) to database', new_customer.first_name,
                    new_customer.last_name, new_customer.customer_id)
        return model_to_dict(new_customer)


def search_customer(customer_id):
    ''' This function will return customer info based on a customer_id.'''
    logger.debug('Searching for customer #%s', str(customer_id))
    try:
        record = Customers.get(Customers.customer_id == customer_id)
        return {'first_name': record.first_name, 'last_name': record.last_name,
                'email_address': record.email_address, 'phone_number': record.phone_number}
    except (IndexError, peewee.DoesNotExist):
        return {}


def delete_customer(customer_id):
    '''This function will delete a customer from the sqlite3 database.'''
    logger.debug('Deleting customer #%s', str(customer_id))

    with database.transaction():
        record = Customers.get(Customers.customer_id == customer_id)
        logger.info('Deleting %s %s (ID: %d) from the database',
                    record.first_name, record.last_name, record.customer_id)
        record.delete_instance()



def update_customer(customer_id, credit_limit):
    '''This function will search an existing customer by customer_id and update
    their credit limit or raise a ValueError exception if the customer does not exist.'''
    logger.debug('Modifying customer #%s credit limit to %s', customer_id, credit_limit)

    with database.transaction():
        try:
            record = Customers.get(Customers.customer_id == customer_id)
            logger.info("%s %s's (ID: %d) credit limit is now $%s",
                        record.first_name, record.last_name, record.customer_id, credit_limit)
            record.credit_limit = credit_limit
            record.save()
            return {'first_name': record.first_name, 'last_name': record.last_name,
                    'email_address': record.email_address, 'credit_limit': record.credit_limit}
        except:
            raise ValueError('No customer with this ID, use list_all_customers()')


def list_active_customers():
    '''This function will return an integer with the current number of active customers.'''
    query = Customers.select(fn.COUNT(Customers.customer_id)).where(Customers.is_active == 1)
    return query.scalar()

def list_all_customers():
    '''This function returns a list of lists of all the customers'''
    query = Customers.select()
    return [REPSTR.format(x.customer_id, x.first_name + ' ' + x.last_name + ',', x.phone_number,
                          x.email_address, x.is_active, x.credit_limit) for x in query]

if __name__ == '__main__':
    testpth = pathlib.Path('./')
    testdest = testpth.absolute() / 'customers.db'
    logging.debug('Creating Database')
    database.create_tables([Customers])
