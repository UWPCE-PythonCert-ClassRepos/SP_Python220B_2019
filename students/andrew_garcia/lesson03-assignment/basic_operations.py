""" Basic functions to interact with different customers """

# pylint: disable=too-many-arguments

import logging
import peewee as pw
import customer_model as cm

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(customer_id, customer_firstname, customer_lastname, customer_address,
                 customer_phone, customer_email, customer_status, customer_credit):
    """ Adds a new customer to the database """
    LOGGER.info('Adding New Customer')
    with cm.DATABASE.transaction():
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
        LOGGER.info('New Customer Added')


def search_customer(customer_id):
    """ Searches and returns dictionary of customer """
    LOGGER.info('Looking for customer')
    try:
        a_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)
        a_customer = {'first_name': a_customer.customer_firstname,
                      'last_name': a_customer.customer_lastname,
                      'email_address': a_customer.customer_address,
                      'phone_number': a_customer.customer_phone}
        LOGGER.info('Customer found')
        return a_customer

    except pw.DoesNotExist:
        LOGGER.info('Not found')
        return {}


def update_customer(customer_id, customer_credit):
    """ Updates credit limit of a customer """
    try:
        with cm.DATABASE.transaction():
            LOGGER.info('Updating Credit')
            a_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)
            a_customer.customer_credit = float(customer_credit)
            a_customer.save()
    except pw.DoesNotExist:
        raise ValueError


def delete_customer(customer_id):
    """" Removes a customer from the database """
    if cm.Customer.get(cm.Customer.customer_id == customer_id):
        LOGGER.info('Customer found')
        with cm.DATABASE.transaction():
            a_customer = cm.Customer.get(cm.Customer.customer_id == customer_id)
            a_customer.delete_instance()
        LOGGER.info('Customer deleted')
    else:
        LOGGER.info('Not found')
        raise pw.DoesNotExist


def list_active_customers():
    """ Lists amount of active customers """
    LOGGER.info('Getting active customers')
    return cm.Customer.select().where(cm.Customer.customer_status).count()
