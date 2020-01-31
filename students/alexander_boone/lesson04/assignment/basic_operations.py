'''
This module performs basic operations on
the customer database.
'''
import logging
from customer_model import *

# ----- LOGGING SETUP ----- #

# Set up Formatting
LOG_FORMAT = ('%(asctime)s %(filename)s:%(lineno)-3d \
                   %(levelname)s %(message)s')
FORMATTER = logging.Formatter(LOG_FORMAT)

# Set up File Handler
LOG_FILE = 'db.log'
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

# Set up Console Handler
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

# Set up Logger and add handler(s)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

# ----- CUSTOMER FUNCTIONS ----- #


def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    '''Add a new customer to the customer database.'''
    with database.transaction():
        new_customer = Customer.create(
            customer_id=customer_id,
            name=name,
            lastname=lastname,
            home_address=home_address,
            phone_number=phone_number,
            email_address=email_address,
            status=status,
            credit_limit=credit_limit
        )
        new_customer.save()
        LOGGER.info('%s %s (id: %d) added to DB.', name, lastname, customer_id)
    return new_customer


def add_customers(customers):
    '''
    Add customers from sequence and return
    list of customers.
    '''
    return [add_customer(*customer) for customer in customers]


def search_customer(customer_id):
    '''
    Return a dictionary object with name, lastname, email address
    and phone number of a customer or an empty dictionary object
    if no customer was found.
    '''
    with database.transaction():
        customer_found = Customer.get_or_none(
            Customer.customer_id == customer_id)
        if not customer_found:
            return {}
        customer_dict = {
            'name': customer_found.name,
            'lastname': customer_found.lastname,
            'home_address': customer_found.home_address,
            'phone_number': customer_found.phone_number,
            'email_address': customer_found.email_address,
            'status': customer_found.status,
            'credit_limit': customer_found.credit_limit
        }
        return customer_dict


def search_customers(customer_ids):
    '''
    Return a list of customers found from list of customer ids.
    '''
    return [search_customer(customer_id) for customer_id in customer_ids]


def delete_customer(customer_id):
    '''Delete a customer from the customer database.'''
    with database.transaction():
        cust_to_delete = Customer.get_or_none(
            Customer.customer_id == customer_id)
        if cust_to_delete is not None:
            cust_to_delete.delete_instance()
            LOGGER.info('%s %s deleted',
                        cust_to_delete.name, cust_to_delete.lastname)
            return cust_to_delete
        return False


def delete_customers(customer_ids):
    '''
    Return a list of customers deleted from db.
    '''
    return [delete_customer(customer_id) for customer_id in customer_ids]


def update_customer_credit(customer_id, credit_limit):
    '''
    Search an existing customer by customer_id and update their
    credit limit or raise a ValueError exception if the customer
    does not exist.
    '''
    with database.transaction():
        cust_to_update = Customer.get_or_none(
            Customer.customer_id == customer_id)
        if cust_to_update is None:
            return False
        cust_to_update.credit_limit = credit_limit
        cust_to_update.save()
        LOGGER.info('%s %s (id: %d) credit updated.', cust_to_update.name,
                    cust_to_update.lastname, customer_id)
        return True


def list_active_customers():
    '''
    Return an integer with the number of customers whose status
    is currently active.
    '''
    with database.transaction():
        active_customers = Customer.select().where(Customer.status == 'active')
        return active_customers.count()
