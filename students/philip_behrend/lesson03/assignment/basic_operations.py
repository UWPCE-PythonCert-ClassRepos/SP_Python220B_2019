""" Operations file to interact with Customer database """
import logging
import traceback
from peewee import IntegrityError
from customer_model import *


logging.basicConfig(level=(logging.INFO))
logger = logging.getLogger(__name__)

def add_customer(**kwargs):
    """ Add customer function """
    try:
        with db.transaction():
            new_cust = (Customer.create)(**kwargs)
            new_cust.save()
            logger.info('Customer addition successful')
    except IntegrityError as e:
        logger.info('Error adding customer')
        logger.info(e)
        raise IntegrityError      


def search_customer(customer_id):
    """ Search for customer by customer_id """
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
    except DoesNotExist as e:
        print('Customer not found')
        print(e)
        raise ValueError

    return {'firstname':customer.firstname, 'lastname':customer.lastname, 'email':customer.email,
            'phone_no':customer.phone_no}


def update_customer_credit(customer_id, credit_limit):
    """ Update credit limit for customer, given input customer_id """
    try:
        with db.transaction():
            customer = Customer.get_by_id(customer_id)
            customer.credit_limit = credit_limit
            customer.save()
            logger.info('Customer credit limit modified to: {}'.format(credit_limit))
    except ValueError:
        print('Customer does not exist')


def list_active_customers():
    """ Lists all customers with status == 1 """
    result = Customer.select().where(Customer.status == 1).count()
    return result
