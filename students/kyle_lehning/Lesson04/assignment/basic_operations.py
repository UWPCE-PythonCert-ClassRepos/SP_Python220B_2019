#!/usr/bin/env python3
"""
Basic operations
"""
import logging
import datetime
import peewee
from customer_schema import Customer


def __setup_logger(name, log_file, level=logging.WARNING, stream=True):
    """
    This function sets up loggers.
    """
    log_format = logging.Formatter("%(asctime)s%(filename)s:%(lineno)-3d %(levelname)s %(message)s")
    handler = logging.FileHandler(log_file)
    handler.setFormatter(log_format)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    if stream is True:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_format)
        logger.addHandler(stream_handler)
    return logger


LOG_FILE = 'basic_operations' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
LOGGER = __setup_logger('first_logger', LOG_FILE)
ACTIVITY_LOGGER = __setup_logger('second_logger', 'db.log', logging.INFO, False)


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
        ACTIVITY_LOGGER.info('Added new customer, ID: %s', customer_id)
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
        ACTIVITY_LOGGER.info('Deleted customer ID: %s', customer_id)
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
    old_limit = db_query.credit_limit
    db_query.credit_limit = float(credit_limit)
    db_query.save()
    ACTIVITY_LOGGER.info("Updated customer ID %s's credit from %s to %s",
                         customer_id, old_limit, credit_limit)


def list_active_customers():
    """
    This function will return an integer with the number of customers whose status is
    currently active.
    """
    db_query = Customer.select().where(Customer.status == True).count()  # pylint: disable=C0121
    return db_query


def display_customers(active_only=True):
