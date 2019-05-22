#!/usr/bin/env python3
"""
Basic operations
"""
import logging
import datetime
import peewee
from customer_schema import Customer

LOG_FILE = 'basic_operations' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
LOG_FORMAT = "%(asctime)s%(filename)s:%(lineno)-3d%(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.setLevel(logging.WARNING)
FILE_HANDLER.setLevel(logging.WARNING)
CONSOLE_HANDLER.setLevel(logging.WARNING)


def add_customer(customer_id, name, lastname, home_address, phone_number,  # pylint: disable=R0913
                 email_address, status, credit_limit):
    """
    This function will add a new customer to the sqlite3 database.
    """
    try:
        new_customer = Customer.create(
            customer_id=customer_id,
            name=name,
            lastname=lastname,
            home_address=home_address,
            phone_number=phone_number,
            email_address=email_address,
            status=status,
            credit_limit=credit_limit
        )
        new_customer.save()
    except peewee.IntegrityError as exception:
        if 'unique' in str(exception).lower():
            LOGGER.warning('Tried to add a customer_id that already exists: %s', customer_id)
            raise peewee.IntegrityError('Tried to add a customer_id that already exists: {}'
                                        .format(customer_id))
        LOGGER.debug("Integrity Error in add_customer: %s", str(exception))
    except Exception as exception:
        LOGGER.debug('add_customer exception: %s', str(exception))
        raise Exception('add_customer raised this error: {}'.format(str(exception)))


def search_customer(customer_id):
    """
    This function will return a dictionary object with name, lastname, email address
    and phone number of a customer or an empty dictionary object if no customer was found.
    """
    customer_dict = {}
    try:
        db_query = Customer.get_by_id(customer_id)
    except peewee.DoesNotExist:
        LOGGER.warning("'%s' doesn't exist in database using search_customer()", customer_id)
        return customer_dict
        # raise peewee.DoesNotExist("{} doesn't exist in database".format(customer_id))
    keys = ['name', 'lastname', 'email_address', 'phone_number']
    values = [db_query.name, db_query.lastname, db_query.email_address, db_query.phone_number]
    customer_dict = dict(zip(keys, values))

    return customer_dict


def delete_customer(customer_id):
    """
    This function will delete a customer from the sqlite3 database.
    """
    try:
        db_query = Customer.get_by_id(customer_id)
        db_query.delete_instance()
    except peewee.DoesNotExist:
        LOGGER.warning("'%s' doesn't exist in database using delete_customer()", customer_id)


def update_customer_credit(customer_id, credit_limit):
    """
    This function will search an existing customer by customer_id and update
    their credit limit or raise a ValueError exception if the customer does not exist.
    """
    try:
        db_query = Customer.get_by_id(customer_id)
    except peewee.DoesNotExist:
        LOGGER.warning("'%s' doesn't exist in database using update_customer_credit()", customer_id)
        raise ValueError
    db_query.credit_limit = float(credit_limit)
    db_query.save()


def list_active_customers():
    """
    This function will return an integer with the number of customers whose status is
    currently active.
    """
    db_query = Customer.select().where(Customer.status == True).count()  # pylint: disable=C0121
    return db_query
