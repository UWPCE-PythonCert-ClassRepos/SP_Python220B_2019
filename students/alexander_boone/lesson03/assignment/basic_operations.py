'''
This module performs basic operations on
the customer database.
'''
import logging
from customer_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    '''Add a new customer to the customer database.'''
    try:
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
            logger.info('Saved new customer to DB')

    except Exception as exc:
        logger.info('Error while trying to save new customer to DB')
        logger.info(exc)


def search_customer(customer_id):
    '''
    Return a dictionary object with name, lastname, email address
    and phone number of a customer or an empty dictionary object
    if no customer was found.
    '''
    try:
        with database.transaction():
            customer_found = Customer.get(Customer.customer_id == customer_id)
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
    except Exception as exc:
        logger.info('Customer not found')
        logger.info(exc)
        return {}


def delete_customer(customer_id):
    '''Delete a customer from the customer database.'''
    try:
        with database.transaction():
            cust_to_delete = Customer.get_or_none(Customer.customer_id == customer_id)
            if cust_to_delete is not None:
                cust_to_delete.delete_instance()
                return True
    except Exception as exc:
        logger.info('Error while trying to delete customer from DB')
        logger.info(exc)
    return False


def update_customer_credit(customer_id, credit_limit):
    '''
    Search an existing customer by customer_id and update their
    credit limit or raise a ValueError exception if the customer
    does not exist.
    '''
    try:
        with database.transaction():
            cust_to_update = Customer.get_or_none(Customer.customer_id == customer_id)
            if cust_to_update is None:
                return False
            cust_to_update.credit_limit = credit_limit
            cust_to_update.save()
            return True
    except Exception as exc:
        logger.info('Error while trying to delete customer from DB')
        logger.info(exc)
        return False

def list_active_customers():
    '''
    Return an integer with the number of customers whose status
    is currently active.
    '''
    try:
        with database.transaction():
            active_customers = Customer.select().where(Customer.status == 'active')
            return active_customers.count()
    except Exception as exc:
        logger.info('Error while trying to retrieve count of active customers.')
        logger.info(exc)
        return None
