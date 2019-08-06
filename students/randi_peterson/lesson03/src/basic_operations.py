"""This file defines the basic funtionality of ways to access and manipulate the HP Norton
 database"""

import logging
import peewee
from customer_schema import Customer


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(customer_id, name, lastname, home_address, phone_number, email_address, status,
                 credit_limit):
    """Add new customer to database"""
    try:
        new_customer = Customer.create(customer_id=customer_id, first_name=name,
                                       last_name=lastname, address=home_address,
                                       phone=phone_number, email=email_address,
                                       status=status, credit_limit=credit_limit)
        new_customer.save()
        LOGGER.info('New customer saved!')
    except peewee.IntegrityError:
        LOGGER.info(f'Customer ID {customer_id} had issues, may already exist in the database')
        raise


def search_customer(customer_id):
    """Searches for customer by ID, returns a dictionary object with name, last name, email address,
     and phone number OR an empty dict if no customer found"""
    try:
        the_customer = Customer.get(Customer.customer_id == customer_id)
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
