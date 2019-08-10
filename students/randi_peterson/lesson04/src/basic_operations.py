"""This file defines the basic funtionality of ways to access and manipulate the HP Norton
 database"""

import logging
import peewee
from customer_schema import Customer

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
LOG_FILE = 'db.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

#   File handler set up
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

#   Console handler set up
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

#   Get logger
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


def add_customer(customer_id, name, lastname, home_address, phone_number, email_address, status,
                 credit_limit):
    """Add new customer to database"""
    try:
        new_customer = Customer.create(customer_id=customer_id, first_name=name,
                                       last_name=lastname, address=home_address,
                                       phone=phone_number, email=email_address,
                                       status=status, credit_limit=credit_limit)
        new_customer.save()
        LOGGER.info(f'New customer {customer_id} saved!')
    except peewee.IntegrityError:
        LOGGER.info(f'Customer ID {customer_id} had issues, may already exist in the database')
        raise


def search_customer(customer_id):
    """Searches for customer by ID, returns a dictionary object with name, last name, email address,
     and phone number OR an empty dict if no customer found"""
    try:
        the_customer = Customer.get(Customer.customer_id == customer_id)
        LOGGER.info(f'Customer {customer_id} was found!')
        return {'Name': the_customer.first_name, 'Last Name': the_customer.last_name,
                'Email': the_customer.email, 'Phone Number': the_customer.phone}
    except peewee.DoesNotExist:
        LOGGER.warning(f'Customer {customer_id} is not in the database!')
        # Return an empty dictionary
        return {}


def delete_customer(customer_id):
    """Deletes customer from database"""
    try:
        the_customer = Customer.get(Customer.customer_id == customer_id)
        the_customer.delete_instance()
        LOGGER.info(f'Customer {customer_id} was deleted!')
    except peewee.DoesNotExist:
        LOGGER.warning(f'Customer {customer_id} is not in the database!')
        raise


def update_customer_credit(customer_id, credit_limit):
    """Searches for existing customer, updates the credit limit, or raises ValueError if
    customer not found"""
    try:
        update_credit = Customer.get(Customer.customer_id == customer_id)
        update_credit.credit_limit = credit_limit
        update_credit.save()
        LOGGER.info('Credit limit successfully updated and saved')

    except peewee.DoesNotExist:
        LOGGER.info('Error with updating credit limit')
        raise


def list_active_customers():
    """Returns number of active customers"""
    active_count = Customer.select().where(Customer.status).count()
    LOGGER.info(f'I counted {active_count} active customers')
    return active_count


def list_customer_names():
    """Returns a list of customers in the database"""
    customer_list = Customer.select()
    return [person.customer_id + ": " + person.last_name + ", " + person.first_name
            for person in customer_list]
