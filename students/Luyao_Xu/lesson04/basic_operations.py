"""
Basic operation model
"""
import logging
from peewee import IntegrityError
from customer_model import Customer, DATABASE


LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.setLevel(logging.INFO)


def add_customer(customer_id, first_name, last_name, home_address, phone_number,
                 email_address, is_active, credit_limit):
    """
    add new customer to customer database
    :param customer_id:customer id
    :param first_name: customer first name
    :param last_name: customer last name
    :param home_address: customer address
    :param phone_number: customer cell phone number
    :param email_address: customer email address
    :param is_active: whether the customer is active
    :param credit_limit: customer credit limit
    :return: add a new customer to table
    """
    try:
        LOGGER.info('Successfully connected to the database')

        with DATABASE.transaction():
            new_customer = Customer.create(customer_id=customer_id,
                                           first_name=first_name,
                                           last_name=last_name,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           is_active=is_active,
                                           credit_limit=credit_limit)
            new_customer.save()
            LOGGER.info("Customer added successfully")

    except IntegrityError as error:
        LOGGER.info(error)
        LOGGER.info('Error occurred')


def search_customer(customer_id):
    """
    Search for customer information with customer id
    :param customer_id: ID of the customer
    :return: customer information in a dictionary
    """
    try:
        LOGGER.info('Searching for customer with %s', customer_id)
        a_customer = Customer.get(Customer.customer_id == customer_id)
        return {'first_name': a_customer.first_name,
                'last_name': a_customer.last_name,
                'email_address': a_customer.email_address,
                'phone_number': a_customer.phone_number}

    except Customer.DoesNotExist as error:
        LOGGER.info('Customer with id %s not found.', customer_id)
        LOGGER.info(error)
        raise ValueError
        return dict()


def delete_customer(customer_id):
    """
    Search for the customer with customer id and delete from the database.
    :param customer_id: ID of the customer
    :return: None
    """
    LOGGER.info('Delete customer with id %s', customer_id)
    try:
        a_customer = Customer.get(Customer.customer_id == customer_id)
        a_customer.delete_instance()
        LOGGER.info('Customer with id %s deleted successfully', customer_id)
    except Customer.DoesNotExist as error:
        LOGGER.info('Delete failed.')
        LOGGER.info('Customer with id %s not found.', customer_id)
        LOGGER.info(error)
        raise ValueError


def update_customer_credit(customer_id, credit_limit):
    """
    Update customer credit limit by searching customer id.
    :param customer_id: ID of the customer
    :param credit_limit: Credit limit to be set for the customer
    :return: None
    """
    try:
        LOGGER.info('Update credit limit for customer.')
        with DATABASE.transaction():
            a_customer = Customer.get(Customer.customer_id == customer_id)
            a_customer.credit_limit = int(credit_limit)
            a_customer.save()
            LOGGER.info('customer credit limit has updated')

    except Customer.DoesNotExist as error:
        LOGGER.info('Updated failed.')
        LOGGER.info('Customer with id %s not found.', customer_id)
        LOGGER.info(error)
        raise ValueError


def list_active_customer():
    """
    Show the status of customer
    :return: Count of all active customers
    """
    active_customer = Customer.select().where(Customer.is_active)
    LOGGER.info('Number of active customers retrieved.')
    return len([customer.customer_id for customer in active_customer])
