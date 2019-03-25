"""
    This file will contain the basic operations
    required to manipulate data in the database
"""

from customer_model_schema import *

import logging

def add_customer(customer_id, name, lastname, home_address, phone_number,
email_address, status, credit_limit):
    """This function will add a new customer to the sqlite3 database"""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('customer_data.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            new_customer = Customers.create(
                customer_id,
                name,
                lastname,
                home_address,
                phone_number,
                email_address,
                status,
                credit_limit
            )
            new_customer.save()
    except Exception as e:
        logger.info(f'Error creating {customer_id}')
        logger.info(e)
    finally:
        logger.info('closing database')
        database.close()

def search_customer(customer_id):
    """This function will return a dictionary object with name, lastname,
    email address and phone number of a customer or an empty dictionary
    object if no customer was found."""
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        searched_customer = Customers.get(Customers.customer_id == customer_id)
        logger.info('Customer Found!')
        return {'customer_id': searched_customer.customer_id,
                'name': searched_customer.name,
                'lastname': searched_customer.lastname,
                'home_address': searched_customer.home_address,
                'phone_number': searched_customer.phone_number,
                'email_address': searched_customer.email_address,
                'status': searched_customer.status,
                'credit_limit': searched_customer.credit_limit}
    except Exception as e:
        logger.info(f'Error finding {customer_id}')
        logger.info(e)
        return {}

    finally:
        logger.info('closing database')
        database.close()

def delete_customer(customer_id):
    """This function will delete a customer from the sqlite3 database"""



def update_customer_credit(customer_id, credit_limit):
    """This function will search an existing customer by customer_id and
    update their credit limit or raise a ValueError exception if the
    customer does not exist."""
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        new_credit_customer = Customers.get(Customers.customer_id == customer_id)
        new_credit_customer.credit_limit = credit_limit
        logger.info('Credit limit successfully updated')

    except Exception as e:
        logger.info(f'Error finding {customer_id}')
        logger.info('Credit limit not updated')
        logger.info(e)
        return {}

    finally:
        logger.info('closing database')
        database.close()

def list_active_customers():
    """This function will return an integer with the number of customers
    whose status is currently active"""
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        counter = 0
        for customer in Customers.select().where(Person.status == active)
            counter += 1
        logger.info(f'There are {counter} active customers')
    except Exception as e:
        logger.info(e)
    finally:
        logger.info('closing database')
        database.close()

