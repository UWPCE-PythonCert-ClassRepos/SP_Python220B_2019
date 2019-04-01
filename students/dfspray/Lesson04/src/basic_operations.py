"""
    This file will contain the basic operations
    required to manipulate data in the database
"""

import logging
import create_customer
from customer_model_schema import *

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'db.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

def add_customer(id_number, first, last, address, phone, email, activity, credit):
    """This function will add a new customer to the sqlite3 database"""

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
        LOGGER.debug('Successfully connected to the database')
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
            LOGGER.debug('Successfully added new customer - %s %s', first, last)

    except IntegrityError as ex1:
        LOGGER.warning('Error creating %s, Non-unique customer id', id_number)
        LOGGER.debug(ex1)

    except Exception as ex2:
        LOGGER.debug(ex2)

    finally:
        LOGGER.debug('Closing database')
        DATABASE.close()

def search_customer(customer_id):
    """This function will return a dictionary object with name, lastname,
    email address and phone number of a customer or an empty dictionary
    object if no customer was found."""

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
        searched_customer = Customers.get(Customers.customer_id == customer_id)
        LOGGER.debug('Customer %s Found!', customer_id)
        return {'customer_id': searched_customer.customer_id,
                'name': searched_customer.name,
                'lastname': searched_customer.lastname,
                'home_address': searched_customer.home_address,
                'phone_number': searched_customer.phone_number,
                'email_address': searched_customer.email_address,
                'status': searched_customer.status,
                'credit_limit': searched_customer.credit_limit}

    except Exception as ex:
        LOGGER.warning('Error finding %s', customer_id)
        LOGGER.debug(ex)
        return {}

    finally:
        LOGGER.debug('Closing database')
        DATABASE.close()

def delete_customer(customer_id):
    """This function will delete a customer from the sqlite3 database"""

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
        delete_customer = Customers.get(Customers.customer_id == customer_id)
        delete_customer.delete_instance()
        LOGGER.debug('Successfully deleted customer %s', customer_id)

    except Exception as ex:
        LOGGER.warning('Error finding %s', customer_id)
        LOGGER.debug('Customer was not deleted')
        LOGGER.debug(ex)

    finally:
        LOGGER.debug('Closing database')
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
        LOGGER.debug('Credit limit successfully updated for %s', new_credit_customer.name,
                     new_credit_customer.lastname)
        new_credit_customer.save()

    except Exception as ex:
        LOGGER.warning('Error finding %s', customer_id)
        LOGGER.debug('Credit limit not updated')
        LOGGER.debug(ex)

    finally:
        LOGGER.debug('Closing database')
        DATABASE.close()


def list_active_customers():
    """This function will return an integer with the number of customers
    whose status is currently active"""

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
        customer_list = [customer.customer_id for customer in
                         Customers.select().where(Customers.status == 'active')]
        LOGGER.debug('There are %d active customers', len(customer_list))
        LOGGER.debug('%s', str(customer_list))
        return len(customer_list)

    except Exception as ex:
        LOGGER.debug(ex)

    finally:
        LOGGER.debug('Closing database')
        DATABASE.close()

def update_status(customer_id, new_status):
    """This functions will update the status of a single customer"""
    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

        new_status_customer = Customers.get(Customers.customer_id == customer_id)

        if new_status in ('active', 'inactive'):
            new_status_customer.status = new_status
            LOGGER.debug('Status successfully updated for %s %s', new_status_customer.name,
                         new_status_customer.lastname)
            new_status_customer.save()
        else:
            LOGGER.debug('Status must be set to either "active" or "inactive"')
            LOGGER.debug('Status was not updated')

    except Exception as ex:
        LOGGER.warning('Error finding %s', customer_id)
        LOGGER.debug('Status not updated')
        LOGGER.debug(ex)

    finally:
        LOGGER.debug('Closing database')
        DATABASE.close()
