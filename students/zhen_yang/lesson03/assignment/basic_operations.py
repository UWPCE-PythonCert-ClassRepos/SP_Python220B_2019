""" This modules defines severl functions to deliver some
    database requirements.
"""
import logging
from peewee import SqliteDatabase, fn
from customer_model import Customer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    """ This function will add a new customer to the customers.db database """
    logger.info('In add_customer().')

    database = SqliteDatabase('customers.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            new_customer = Customer.create(customer_id=customer_id, name=name,
                                           lastname=lastname,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           status=status,
                                           credit_limit=credit_limit)

            new_customer.save()
            logger.info('Add new customer to Customer database successfully.')
    except Exception as e:
        logger.info(f'Error creating {name} customer record.')
        logger.info(e)

    finally:
        logger.info('database closes.')
        database.close()

def search_customer(customer_id):
    """ This function will search a customer from the customers.db database
        will return a dictionary object with name, lastname, email address
        and phone number of a customer or an empty dictionary object if
        no customer was found.
    """
    logger.info('In search_customer().')
    logger.info(f'Searching customer {customer_id}.')

    the_customer = Customer.get_or_none(Customer.customer_id == customer_id)

    # build the dict for the found customer
    if the_customer:
        customer = {}
        customer['name'] = the_customer.name
        customer['lastname'] = the_customer.lastname
        customer['phone_number'] = the_customer.phone_number
        customer['email_address'] = the_customer.email_address
        logger.info(f'Found customer {customer_id} successfully.')
    else:
        customer = {} # return empty dict object for non-existing customer.
        logger.info(f'customer {customer_id} is not found.')

    return customer

def delete_customer(customer_id):
    """ This function will delete a customer from the customers.db database """
    logger.info('In delete_customer().')

    the_customer = Customer.get_or_none(Customer.customer_id == customer_id)

    # make sure only the existing customer will be deleteed.
    if the_customer:
        the_customer.delete_instance()
        logger.info(f'Delete customer {customer_id} successfully.')

def update_customer_credit(customer_id, credit_limit):
    """ This function will search an existing customer by customer_id and
        update their credit limit or raise a ValueError exception if the
        customer does not exist.
    """
    the_customer = Customer.get_or_none(Customer.customer_id == customer_id)

    # make sure only the existing customer will be deleteed.
    #if the_customer:
    try:
        the_customer.credit_limit = credit_limit
        the_customer.save()
        logger.info(f'Customer {customer_id} credit limit is '
                    'updated successfully .')
    except AttributeError:
        print(f'Customer {customer_id} does not exist.')


def list_active_customers():
    """ This function will return an integer with the number of customers
         whose status is currently active.
    """
    num = (Customer.select(fn.COUNT(Customer.status))
           .where(Customer.status))
    return num.scalar()
