'''
This file contains basic operations for interacting with a customer database
'''

import logging
from peewee import OperationalError, IntegrityError, DoesNotExist, fn
from customer_model import database, Customer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('One off program to build the class from the model in the database')
database.create_tables([Customer])
database.close()

def add_customer(customer_id, firstname, lastname, address, phone, email, status, credit_limit):
    '''
    Add customer to database, handle several peewee exceptions in the event
    of an error.

    Args:
        customer_id (str):
            Unique customer id (5 characters)
        firstname (str):
            Customer's first name
        lastname (str):
            Customer's last name
        address (str):
            Customer's address
        phone (str):
            Customer's phone number (format XXX-XXX-XXXX)
        email (str):
            Customer's email address
        status (boolean):
            Customer's status (active or not)
        credit_limit (float):
            Customer's credit limit in dollars

    '''
    try:
        with database.transaction():
            new_customer = Customer.create(
                id=customer_id,
                firstname=firstname,
                lastname=lastname,
                address=address,
                phone=phone,
                email=email,
                status=status,
                credit_limit=credit_limit)
        new_customer.save()
        LOGGER.info('Database add successful')
    except (OperationalError, IntegrityError, DoesNotExist) as exc:
        LOGGER.info(f'Error creating entry for customer {customer_id}, see error below')
        LOGGER.info(exc)

def search_customer(customer_id):
    '''
    Search for customer in database.

    Args:
        customer_id (str):
            Unique customer ID (5 characters)

    Returns:
        Dictionary with customer information or empty dictionary if customer
        not found.
    '''
    try:
        customer = Customer.get(Customer.id == customer_id)
        # Return dictionary of customer name, email, phone
        return {'firstname': customer.firstname, 'lastname': customer.lastname,
                'email': customer.email, 'phone':customer.phone}
    except DoesNotExist:
        # Customer not found, return empty dictionary
        return {}

def delete_customer(customer_id):
    '''
    Delete customer from database.

    Args:
        customer_id (str):
            Unique customer ID (5 characters)
    '''
    # Retrieve and delete customer from database
    customer = Customer.get(Customer.id == customer_id)
    customer.delete_instance()

def update_customer_credit(customer_id, credit_limit):
    '''
    Update customer credit limit. Raises value error if customer not found.

    Args:
        customer_id (str):
            Unique customer ID (5 characters)
        credit_limit (float):
            New customer credit limit
    '''
    try:
        # Retrieve customer and update credit limit
        customer = Customer.get(Customer.id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
    except DoesNotExist:
        raise ValueError(f'Customer with id {customer_id} does not exist.')

def list_active_customers():
    '''
    Return count of active customers in database.

    Returns:
        Count of active customers (int)
    '''
    query = Customer.select(Customer, fn.SUM(Customer.status)).where(Customer.status)
    return query.count()
