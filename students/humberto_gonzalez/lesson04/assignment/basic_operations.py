# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 18:19:10 2019

@author: Humberto
"""
# pylint: disable=too-many-arguments,too-few-public-methods,logging-format-interpolation

import logging
import peewee
from assignment.customer_model import DATABASE as database
from assignment.customer_model import Customer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

LOG_FILE = 'db.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(FILE_HANDLER)

def add_customer(customer_id, first_name, last_name, home_address,
                 phone_number, email_address, status, credit_limit):
    """funcion that adds a customer to the database with the given info"""
    try:
        with database.transaction():
            new_customer = Customer.create(customer_id=customer_id,
                                           first_name=first_name,
                                           last_name=last_name,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           status=status,
                                           credit_limit=credit_limit)
            new_customer.save()
            LOGGER.info(f'Customer added to database, {customer_id}')
    except peewee.IntegrityError:
        LOGGER.info(f'Error adding {customer_id} : {first_name} {last_name}')
        LOGGER.info(f'{customer_id} already exists in database')
        raise ValueError
    finally:
        database.close()

def search_customer(customer_id):
    """Given a customer_id, searches the database for the customer's info"""
    try:
        selected_customer = Customer.get(Customer.customer_id == customer_id)
        customer_info = {'first_name':selected_customer.first_name,
                         'last_name':selected_customer.last_name,
                         'email_address':selected_customer.email_address,
                         'phone_number':selected_customer.phone_number}
    except peewee.DoesNotExist:
        LOGGER.info(f'Error occured searching for {customer_id}')
        LOGGER.info(f'{customer_id} not found in database')
        customer_info = {}
    return customer_info

def delete_customer(customer_id):
    """Given a customer ID, deletes customer from database"""
    try:
        selected_customer = Customer.get(Customer.customer_id == customer_id)
        selected_customer.delete_instance()
        LOGGER.info(f'Customer deleted from database, {customer_id}')
    except peewee.DoesNotExist:
        LOGGER.info(f'Error occured deleting {customer_id}')
        LOGGER.info(f'{customer_id} not found in database')
        raise ValueError

def update_customer_credit(customer_id, credit_limit):
    """Given a customer id, updates the customer's credit limit"""
    try:
        with database.transaction():
            selected_customer = Customer.get(Customer.customer_id == customer_id)
            selected_customer.credit_limit = float(credit_limit)
            selected_customer.save()
            LOGGER.info(f'Customers credit limit updated, {customer_id}')
    except peewee.DoesNotExist:
        LOGGER.info(f'Error occured updating credit limit for {customer_id}')
        LOGGER.info(f'{customer_id} not found in database')
        raise ValueError

def list_active_customers():
    """returns the count of the number of active customers"""
    return Customer.select().where(Customer.status == 'Active').count()

if __name__ == "__main__":
    database.init('customers.db')
    database.create_tables([Customer])
