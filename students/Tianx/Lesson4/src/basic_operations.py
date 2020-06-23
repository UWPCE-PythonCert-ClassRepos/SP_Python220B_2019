# pylint: disable = W0614, W0401, C0301, C0114,R0913,W0703,W1203

import logging
from peewee import *
from customer_model import Customer


# Logging setup
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'db.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE, mode="w")
FILE_HANDLER.setFormatter(FORMATTER)
LOGGING = logging.getLogger(__name__)
LOGGING.setLevel(logging.INFO)
LOGGING.addHandler(FILE_HANDLER)

# Database setup
db = SqliteDatabase('customers.db')
db.create_tables([Customer])


def add_customer(customer_id, first_name, last_name, home_address, phone_number,
                 email_address, active_status, credit_limit):
    """
    This function will add a new customer to the sqlite3 database.
    """
    try:
        db.connect()
        db.execute_sql('PRAGMA foreign_keys = ON;')
        LOGGING.info('Try to create a new customer record')
        with db.transaction():
            new_customer = Customer.create(customer_id=customer_id,
                                           first_name=first_name,
                                           last_name=last_name,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           active_status=active_status,
                                           credit_limit=credit_limit)
            new_customer.save()
            LOGGING.info(f'Adding new customer:{customer_id} to the database.')
    except Exception as err:
        LOGGING.info(f'Error creating = {customer_id}')
        LOGGING.info(err)
    finally:
        LOGGING.info('database closes')
        db.close()


def search_customer(customer_id):
    """
    This function will return a dictionary object with name, lastname, email address and phone
    number of a customer
    or an empty dictionary object if nodebug customer was found.
    """
    try:
        db.connect()
        db.execute_sql('PRAGMA foreign_keys = ON;')
        LOGGING.info('Try to search a customer record')
        with db.transaction():
            customer = Customer.get(Customer.customer_id == customer_id)
            LOGGING.info(f'{customer_id} found.')
        return {'first_name': customer.first_name, 'last_name': customer.last_name,
                'email': customer.email_address, 'phone_number': customer.phone_number}
    except DoesNotExist:
        LOGGING.info(f'Customer {customer_id} does not exit')
        customer = dict()
        return customer  # Empty dictionary if no customer was found
    finally:
        LOGGING.info('database closes')
        db.close()


def delete_customer(customer_id):
    """
    This function will delete a customer from the sqlite3 database.
    """
    try:
        db.connect()
        db.execute_sql('PRAGMA foreign_keys = ON;')
        LOGGING.info('Try to search a customer record')
        with db.transaction():
            customer = Customer.get(Customer.customer_id == customer_id)
            customer.delete_instance()
            LOGGING.info(f'{customer_id} found and deleted.')
    except DoesNotExist:
        LOGGING.info(f'{customer_id} does not exist.')
        raise DoesNotExist
    finally:
        LOGGING.info('database closes')
        db.close()


def update_customer_credit(customer_id, credit_limit):
    """
    This function will search an existing customer by customer_id and update their credit limit or
    raise a ValueError exception if the customer does not exist.
    """
    try:
        db.connect()
        db.execute_sql('PRAGMA foreign_keys = ON;')
        LOGGING.info('Try to search a customer record')
        with db.transaction():
            customer = Customer.get(Customer.customer_id == customer_id)
            customer.credit_limit = credit_limit
            customer.save()
            LOGGING.info(f'{customer_id} now has a ${credit_limit} credit limit.')
    except DoesNotExist:
        LOGGING.info(f'{customer_id} does not exist.')
        raise DoesNotExist
    finally:
        LOGGING.info('database closes')
        db.close()


def list_active_customers():
    """
    This function will return an integer with the number of customers whose status is currently active
    """
    active_customers = Customer.select().where(Customer.active_status).count()
    LOGGING.info(f'We have {active_customers} active customers.')
    return active_customers


def display_customer_credit(min_credit):
    """
    returns a list of customers with credit limit above a given parameter.
    """
    query = Customer.select().where(Customer.active_status)
    lst_of_customer = [f'Name:{i.first_name} {i.last_name}, Phone number:{i.phone_number}, ' \
                       f'Credit limit:{i.credit_limit}'
                       for i in query if i.credit_limit >= min_credit]
    LOGGING.info("Getting customer credit limit above %s", min_credit)
    return lst_of_customer
