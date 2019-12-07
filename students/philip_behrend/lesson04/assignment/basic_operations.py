""" Operations file to interact with Customer database """
import logging
from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict
from customer_model import *

# Set up logger
logger = logging.getLogger(__name__)

# Create log file for database information
log_level = logging.INFO
log_format = "%(asctime)s %(filename)s: %(lineno)-3d %(levelname)s %(message)s"
log_file = "db.log"
logging.basicConfig(level=log_level, format=log_format, filename=log_file)


def add_customer(**kwargs):
    """ Add customer function """
    try:
        with db.transaction():
            new_cust = (Customer.create)(**kwargs)
            new_cust.save()
            logger.info('Customer addition success: %s %s', new_cust.firstname, new_cust.lastname)
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


def count_active_customers():
    """ Counts all customers with status == 1 """
    result = Customer.select().where(Customer.status == 1).count()
    if result == 1:
        logger.info('There is %s active customer', result)
    else:
        logger.info('There are %s active customers', result)
    return result

def list_active_customers():
    """ Lists customers with active status """
    result = Customer.select().where(Customer.status == 1)
    result_dict = {}
    for person in result:
        logger.info('%s %s is active', person.firstname, person.lastname)
        result_dict[person.customer_id] = model_to_dict(person)
    logger.info('Active customer information: \n %s', result_dict)
    return result_dict
