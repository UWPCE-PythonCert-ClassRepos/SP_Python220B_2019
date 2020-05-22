'''
basic operations for employees to perform
for customer data
'''

import logging
from peewee import *
from customer_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Working with Customer class')

def add_customer(customer_id, name, last_name,
                 home_address, email_address,
                 phone_number, status, credit_limit):
    ''' add new customers to the database '''

    try:
        with database.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                name=name,
                last_name=last_name,
                home_address=home_address,
                email_address=email_address,
                phone_number=phone_number,
                status=status,
                credit_limit=credit_limit)
            new_customer.save()
            logger.info(f'{name} {last_name} added to database')

    except IntegrityError as e:
        logger.info(f'Integrity error thrown {e}')

def search_customer(customer_id):
    ''' searches for a customer by id '''
    try:
        customer = Customer.get(customer_id=customer_id)

    except DoesNotExist:
        raise ValueError(f'{customer_id} not found in database')

    return {'name': customer.name,
            'last_name': customer.last_name,
            'email_address': customer.email_address,
            'phone_number': customer.phone_number}

def delete_customer(customer_id):
    ''' remove a customer from the database '''
    try:
        customer = Customer.get(customer_id=customer_id)
        customer.delete_instance()
        logger.info(f'{customer.name} has been deleted')

    except DoesNotExist:
        raise ValueError(f'{customer_id} not found in database')

def update_customer_credit(customer_id, credit_limit):
    ''' update customers credit limit '''
    logger.info(f'updating customers credit limit {credit_limit}')

    try:
        customer = Customer.get(customer_id=customer_id)
        logger.info(f'found customers id: {customer.customer_id}')
        customer.credit_limit = credit_limit
        customer.save()
        logger.info(f'customers credit limit is now set to: ${customer.credit_limit}')

    except DoesNotExist:
        raise ValueError(f'{customer_id} not found in database')

    return credit_limit

def update_customer_status(customer_id, status):
    ''' update customers status '''
    logger.info(f'updating customers status {status}')

    try:
        customer = Customer.get(customer_id=customer_id)
        logger.info(f'found customers id: {customer.customer_id}')
        customer.status = status
        customer.save()
        logger.info(f'customers status is now set to: {customer.status}')

    except DoesNotExist:
        raise ValueError(f'{customer_id} not found in database')

    return customer.status

def list_active_customers():
    ''' return number of active customers in database '''
    active_customers = Customer.select().where(Customer.status).count()
    logger.info(f'active customer count is {active_customers}')

    return active_customers

def list_active_customers_name():
    ''' displays active customers by name returned in a list '''
    total_active = list_active_customers()
    customer = Customer.select().order_by(Customer.name).get()

    active_customers = [customer.name for x in range(total_active)]

    return active_customers
