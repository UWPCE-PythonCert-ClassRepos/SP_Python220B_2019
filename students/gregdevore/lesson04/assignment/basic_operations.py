'''
This file contains basic operations for interacting with a customer database
'''

import logging
from peewee import OperationalError, IntegrityError, DoesNotExist, fn
from customer_model import database, Customer

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
FORMATTER = logging.Formatter(LOG_FORMAT)

# Create log file for warning and error messages
LOG_FILE = 'db.log'
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)
# Add handlers to logger
LOGGER.addHandler(FILE_HANDLER)

LOGGER.info('One off program to build the class from the model in the database')
database.create_tables([Customer])
database.close()

def add_customers(customer_dict):
    '''
    Add multiple customer to database

    Args:
        customer_dict (dict):
            Nested dictionary of customers to add, key is customer_id, value is
            dictionary of remaining customer attributes
    '''
    for customer in customer_dict:
        add_customer(customer,
                     customer_dict[customer]['firstname'],
                     customer_dict[customer]['lastname'],
                     customer_dict[customer]['address'],
                     customer_dict[customer]['phone'],
                     customer_dict[customer]['email'],
                     customer_dict[customer]['status'],
                     customer_dict[customer]['credit_limit'])

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
        LOGGER.info(f'Added customer {customer_id} to database')
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

def return_customer_ids():
    '''
    Return all customer IDs from database.
    Note that this function returns a generator so all customers aren't
    collected at once (provision for large customer database).
    '''
    for customer_id in Customer.select(Customer.id):
        yield search_customer(customer_id)

def print_all_customers():
    '''
    Print all customers names, email addresses, and phone numbers
    Since return_customer_ids() produces a generator, need to handle
    StopIteration error that will be thrown when generator is exhausted.
    '''
    customers = return_customer_ids()
    try:
        while customers:
            print('{firstname} {lastname}, {email}, {phone}'.format(**next(customers)))
    except StopIteration:
        pass

def delete_customer(customer_id):
    '''
    Delete customer from database.

    Args:
        customer_id (str):
            Unique customer ID (5 characters)
    '''
    # Retrieve and delete customer from database
    LOGGER.info(f'Deleted customer {customer_id} from database')
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
        LOGGER.info(f'Updated credit limit of customer {customer_id} to {credit_limit} dollars')
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
