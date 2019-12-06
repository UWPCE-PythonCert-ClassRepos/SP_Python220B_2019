""" Basic functions to interact with different customers """

# pylint: disable=too-many-arguments

import logging
import peewee as pw
import customer_model as cm

# create log format to use for logging
LOG_FORMAT = '%(asctime)s) %(levelname)s %(message)s'
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.INFO)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.addHandler(FILE_HANDLER)


def add_customer(customer_id, customer_firstname, customer_lastname, customer_address,
                 customer_phone, customer_email, customer_status, customer_credit):
    """ Adds a new customer to the database """
    with cm.DATABASE.transaction():
        LOGGER.info('Adding New Customer')
        new_customer = cm.Customer.create(
            customer_id=customer_id,
            customer_firstname=customer_firstname,
            customer_lastname=customer_lastname,
            customer_address=customer_address,
            customer_phone=customer_phone,
            customer_email=customer_email,
            customer_status=customer_status,
            customer_credit=customer_credit)
        new_customer.save()
        LOGGER.info('Customer %s Added to Database', customer_id)


def search_customer(customer_id):
    """ Searches and returns dictionary of customer """
    try:
        LOGGER.info('Searching For Customer %s', customer_id)
        a_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)
        a_customer = {'first_name': a_customer.customer_firstname,
                      'last_name': a_customer.customer_lastname,
                      'email_address': a_customer.customer_address,
                      'phone_number': a_customer.customer_phone}
        LOGGER.info('Customer %s Found', customer_id)
        return a_customer

    except pw.DoesNotExist:
        LOGGER.info('Customer %s Not Found', customer_id)
        return {}


def update_customer(customer_id, customer_credit):
    """ Updates credit limit of a customer """
    try:
        with cm.DATABASE.transaction():
            LOGGER.info('Updating Customer Credit')
            a_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)
            a_customer.customer_credit = float(customer_credit)
            LOGGER.info('Customer %s Credit Updated', customer_id)
            a_customer.save()
    except pw.DoesNotExist:
        LOGGER.info('Customer %s Not Found', customer_id)
        raise ValueError


def delete_customer(customer_id):
    """" Removes a customer from the database """
    if cm.Customer.get(cm.Customer.customer_id == customer_id):
        LOGGER.info('Searching For Customer %s', customer_id)
        with cm.DATABASE.transaction():
            a_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)
            a_customer.delete_instance()
        LOGGER.info('Customer %s Deleted', customer_id)
    else:
        LOGGER.info('Customer %s Not Found', customer_id)
        raise pw.DoesNotExist


def list_active_customers():
    """ Lists amount of active customers """
    LOGGER.info('Getting Active Customers')
    return cm.Customer.select().where(cm.Customer.customer_status).count()


def return_all_customers():
    """" Returns all customer ids, first and last names """
    LOGGER.info('Retrieving All Customers')
    return [{customer.customer_id:(customer.customer_firstname, customer.customer_lastname)} for
            customer in cm.Customer.select().where(cm.Customer.customer_id)]
