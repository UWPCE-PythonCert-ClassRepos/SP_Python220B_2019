# Stella Kim
# Assignment 3: Storing Customer Data

"""Create customer database with Peewee ORM, SQLite and Python"""


import logging
from peewee import IntegrityError, DoesNotExist
from customer_model import CUSTOMER_DB, Customer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Logger has initiated.')

CUSTOMER_DB.create_tables([Customer])
LOGGER.info('Customer table created.')


def add_customer(customer_id, first_name, last_name, home_address,
                 phone, email, status, credit_limit):
    """Create a new customer.  Raises error if ID in use."""
    try:
        with CUSTOMER_DB.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                first_name=first_name,
                last_name=last_name,
                home_address=home_address,
                phone=phone,
                email=email,
                status=status,
                credit_limit=credit_limit
            )
        new_customer.save()
        LOGGER.debug('New customer %s %s (ID: %s) has been added to DB',
                     first_name, last_name, customer_id)

    except IntegrityError as error:
        LOGGER.error('Failure: ID %s already in use.', customer_id)
        LOGGER.info(error)
        raise ValueError


def search_customer(customer_id):
    """Search for a customer in the database by ID."""
    try:
        search = Customer.get(Customer.customer_id == customer_id)
        LOGGER.debug('Searching for customer %s...', customer_id)
        return {'First Name': search.first_name,
                'Last Name': search.last_name,
                'Email Address': search.email,
                'Phone Number': search.phone}

    except DoesNotExist:
        LOGGER.error('Customer %s does not exist.', customer_id)
        return {}


def delete_customer(customer_id):
    """Delete a customer from the database by ID."""
    try:
        search = Customer.get(Customer.customer_id == customer_id)
        LOGGER.debug('Searching for customer %s...', customer_id)
        search.delete_instance()
        LOGGER.debug('Customer %s has been deleted from database.',
                     customer_id)
        return search

    except DoesNotExist:
        LOGGER.error('Customer %s does not exist.', customer_id)
        return None


def update_customer_credit(customer_id, credit_limit):
    """Update a customer's credit limit by ID."""
    try:
        search = Customer.get(Customer.customer_id == customer_id)
        LOGGER.debug('Searching for customer %s...', customer_id)
        with CUSTOMER_DB.transaction():
            search.credit_limit = credit_limit
            search.save()
        LOGGER.debug('Credit limit for %s has been updated.', customer_id)
        return search.credit_limit

    except DoesNotExist:
        LOGGER.error('Customer %s does not exist.', customer_id)
        return None


def list_active_customers():
    """Display a count of active customers in the database."""
    active_customers = Customer.select().where(Customer.status ==
                                               'Active').count()
    LOGGER.info('Number of customers whose status is currently active: %s.',
                active_customers)
    return active_customers


CUSTOMER_DB.close()
