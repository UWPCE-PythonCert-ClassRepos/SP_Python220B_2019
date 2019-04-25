"""
    A file called basic_operations.py in the src directory.
    This file will have functions to add, search, delete,
    update and list active customers.
"""

import logging
import sys


sys.path.append(r"C:\UW-Python-Advanced\SP_Python220B_2019\students\vvinodh\Lesson3\src")

import create_customer
from customer_model_schema import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def add_customer(id_number, first, last, address, phone, email, activity, credit):
    """Adding new customer to database"""

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
        LOGGER.info('Database connect established')
        with DATABASE.transaction():
            new_customer = Customers.create(customer_id=id_number,
                                            name=first,
                                            lastname=last,
                                            home_address=address,
                                            phone_number=phone,
                                            email_address=email,
                                            status=activity,
                                            credit_limit=float(credit))
            new_customer.save()
            LOGGER.info('Successfully added new customer')

    except IntegrityError as ex1:
        LOGGER.info('Error creating %s, Non-unique customer id', id_number)
        LOGGER.info(ex1)

    except Exception as ex2:
        LOGGER.info(ex2)

    finally:
        LOGGER.info('Closing database')
        DATABASE.close()

def search_customer(customer_id):
    """This function will return a dictionary object with name, lastname,
    email address and phone number of a customer or an empty dictionary
    object if no customer was found."""

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
        searched_customer = Customers.get(Customers.customer_id == customer_id)
        LOGGER.info('Customer Found!')
        return {'customer_id': searched_customer.customer_id,
                'name': searched_customer.name,
                'lastname': searched_customer.lastname,
                'home_address': searched_customer.home_address,
                'phone_number': searched_customer.phone_number,
                'email_address': searched_customer.email_address,
                'status': searched_customer.status,
                'credit_limit': searched_customer.credit_limit}

    except Exception as ex:
        LOGGER.info('Error finding %s', customer_id)
        LOGGER.info(ex)
        return {}

    finally:
        LOGGER.info('Closing database')
        DATABASE.close()

def delete_customer(customer_id):
    """This function will delete a customer from the sqlite3 database"""

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
        delete_customer = Customers.get(Customers.customer_id == customer_id)
        delete_customer.delete_instance()
        LOGGER.info('Successfully deleted customer %s', customer_id)

    except Exception as ex:
        LOGGER.info('Error finding %s', customer_id)
        LOGGER.info('Customer was not deleted')
        LOGGER.info(ex)

    finally:
        LOGGER.info('Closing database')
        DATABASE.close()

def update_customer_credit(customer_id, credit_limit):
    """This function will search an existing customer by customer_id and
    update their credit limit or raise a ValueError exception if the
    customer does not exist."""

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

        new_credit_customer = Customers.get(Customers.customer_id == customer_id)
        new_credit_customer.credit_limit = credit_limit
        LOGGER.info('Credit limit successfully updated')
        new_credit_customer.save()

    except Exception as ex:
        LOGGER.info('Error finding %s', customer_id)
        LOGGER.info('Credit limit not updated')
        LOGGER.info(ex)

    finally:
        LOGGER.info('Closing database')
        DATABASE.close()


def list_active_customers():
    """This function will return an integer with the number of customers
    whose status is currently active"""

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
        counter = 0
        customer_list = []
        for customer in Customers.select().where(Customers.status == 'active'):
            counter += 1
            customer_list.append(customer)
        LOGGER.info('There are %d active customers', counter)
        return counter

    except Exception as ex:
        LOGGER.info(ex)

    finally:
        LOGGER.info('Closing database')
        DATABASE.close()

def update_status(customer_id, new_status):
    """This functions will update the status of a single customer"""
    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

        new_status_customer = Customers.get(Customers.customer_id == customer_id)

        if new_status in ('active', 'inactive'):
            new_status_customer.status = new_status
            LOGGER.info('Status successfully updated')
            new_status_customer.save()
        else:
            LOGGER.info('Status must be set to either "active" or "inactive"')
            LOGGER.info('Status was not updated')

    except Exception as ex:
        LOGGER.info('Error finding %s', customer_id)
        LOGGER.info('Status not updated')
        LOGGER.info(ex)

    finally:
        LOGGER.info('Closing database')
        DATABASE.close()
