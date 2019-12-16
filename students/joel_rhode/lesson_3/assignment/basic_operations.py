"""
Contains basic functions for adding, deleting, and querying data from the customer database.
"""
# pylint: disable=too-many-arguments

import logging
import datetime
import peewee

from customer_model import Customer, DATABASE as database

DATABASE_NAME = 'customer.db'

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
LOG_FILE = 'basic_operations_'+datetime.datetime.now().strftime('%Y-%m-%d')+'.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE, delay=True)
FILE_HANDLER.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.addHandler(FILE_HANDLER)

LOGGER.setLevel(logging.ERROR)


def add_customer(customer_id, name, lastname, home_address, phone_number, email_address, status,
                 credit_limit):
    """Adds a new customer to the database."""
    init_database()
    try:
        with database.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                active_status=status,
                credit_limit=credit_limit
            )
            new_customer.save()
            logging.info('New customer, ID %s, added successfully.', customer_id)
            return True
    except peewee.IntegrityError as exc:
        logging.error('Error creating new customer with ID %s: %s.', customer_id, exc)
        return False
    finally:
        database.close()


def search_customer(customer_id):
    """Searches for a customer in the database, returning a dictionary of contact info if found."""
    init_database()
    try:
        customer = Customer.get_by_id(customer_id)
        customer_dict = {
            'name': customer.name,
            'lastname': customer.lastname,
            'email_address': customer.email_address,
            'phone_number': customer.phone_number
        }
        return customer_dict
    except peewee.DoesNotExist:
        logging.warning("Customer ID %s doesn't exist in database.", customer_id)
        return {}
    finally:
        database.close()


def delete_customer(customer_id):
    """Deletes a customer from the database."""
    init_database()
    try:
        with database.transaction():
            customer = Customer.get_by_id(customer_id)
            customer.delete_instance()
            logging.info('Customer with ID %s successfully deleted.', customer_id)
            return True
    except peewee.DoesNotExist:
        logging.error('Customer delete with ID %s failed, not in database..', customer_id)
        return False
    finally:
        database.close()


def update_customer_credit(customer_id, credit_limit):
    """Updates a customer's credit limit in the database."""
    init_database()
    try:
        customer = Customer.get_by_id(customer_id)
        customer.credit_limit = credit_limit
        customer.save()
        return True
    except peewee.DoesNotExist:
        logging.error("Customer ID %s doesn't exist in database.", customer_id)
        raise ValueError('Customer ID does not exist in database.')
    finally:
        database.close()


def list_active_customers():
    """Returns a count of active customers in the database."""
    init_database()
    return Customer.select().where(Customer.active_status).count()


def init_database():
    """This function checks to see if the database exists, and if not, generates the tables."""
    database.init(DATABASE_NAME)
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON')
    if not database.table_exists([Customer]):
        database.create_tables([Customer])
    database.close()
