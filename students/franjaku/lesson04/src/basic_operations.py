"""
    Defines the basic operations needed to operate and maintain a customer database in sqlite3.
        -add new customers to the database
        -search customers in the database
        -delete existing customers from the database
        -update customers credit
        -list the number of active customers in the database

    Uses logging to capture messages.
    Assignment #4 Python 220
    Add code to log all database data changes (adds, amends, deletes) to a file called db.log.
"""

import warnings
import logging
import peewee

from customer_model import Customer, database

logging.basicConfig(level=logging.ERROR)

# Setup logging params
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = 'db.log'

FILE_HANDLER = logging.FileHandler(LOG_FILE, mode="w")
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

LOG_DICT = {'0': 60,
            '1': 40,
            '2': 30,
            '3': 10}


def add_customer(customer_id, name, last_name, home_address, phone_number, email_address, status,
                 credit_limit):
    """
        Adds a new customer to the database. Throw an exception if the customer already exists.
        Checks the input data to ensure its valid.
        Customer ID is used as the primary  key.
    """
    with database.atomic():
        try:
            new_customer = Customer.create(customer_id=customer_id,
                                           name=name,
                                           last_name=last_name,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           status=status,
                                           credit_limit=credit_limit)
            new_customer.save()
            logging.info('New Customer: %s, created and saved to the database.', customer_id)
        except peewee.IntegrityError as err:
            print(err)
            logging.warning('Error adding to db, could not add customer: %s', customer_id)


def search_customer(customer_id):
    """
        Searches the database of existing customers. Returns a dictionary with customer information.
        An empty dictionary is returned if the customer does not exist in the database.

        :param customer_id: primary key used to search the database
        :return: dict{customer_id, name, last_name, email_address, phone_number, email_address,
                    status, credit_limit}
    """
    customer = Customer.get_or_none(Customer.customer_id == customer_id)

    logging.debug('Searching for customer: %s in database.', customer_id)
    # make a full dictionary if the person exists
    if customer:
        logging.debug('Customer: %s found in the database.', customer_id)
        customer_dict = {'customer_id': customer.customer_id,
                         'name': customer.name,
                         'last_name': customer.last_name,
                         'home_address': customer.home_address,
                         'phone_number': customer.phone_number,
                         'email_address': customer.email_address,
                         'status': customer.status,
                         'credit_limit': customer.credit_limit}
        logging.debug('Customer dictionary created.')
    else:
        # create an empty dict
        logging.debug('Customer: %s not found in the database, returning empty dictionary.',
                      customer_id)
        customer_dict = {}

    return customer_dict


def delete_customer(customer_id):
    """
        Deletes an existing customer from the database. A warning message is printed if the
        customer does not exist in the database.
    """
    logging.debug('Attempting to delete customer: %s', customer_id)

    query = Customer.delete().where(Customer.customer_id == customer_id).execute()

    if query == 0:
        warnings.warn(f'User with customer_id={customer_id} does not exist in the database.'
                      , UserWarning)
    else:
        logging.info('Customer: %s, successfully deleted from the database.', customer_id)


def update_customer_credit(customer_id, credit_limit):
    """
        Updates a customers credit limit in the database. A ValueError exception is thrown if the
        customer does not exist in the database.
    """
    logging.debug('Attempting to update credit for customer: %s, to %s ', customer_id, credit_limit)
    customer = Customer.get_or_none(Customer.customer_id == customer_id)

    if customer:
        customer.credit_limit = credit_limit
        customer.save()
        logging.info('Updated credit limit for customer: %s to %s', customer_id, credit_limit)
    else:
        logging.error('Error: customer: %s does not exist.', customer_id)
        raise ValueError


def list_active_customers():
    """
        Returns an integer with the number of customers whose status is active in the database.
    """
    logging.debug('Querying for number of active customers.')
    query = Customer.select().where(Customer.status == 'Active')
    active_customers = len(query)
    logging.debug('Number of active customers: %s', active_customers)
    return active_customers
