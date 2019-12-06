""" Operations file to interact with Customer database """
import logging
import traceback
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
    except Exception as e:
        logger.info('Error adding customer: {} {}'.format(kwargs['firstname'], kwargs['lastname']))
        logger.info(e)
        logger.info(traceback.format_exc())


def search_customer(customer_id):
    """ Search for customer by customer_id """
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
    except Exception as e:
        print('Customer not found')
        print(e)

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
