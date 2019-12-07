'''
This file shows the basic operations for the customer model file
'''
import datetime
import logging
import peewee as p
from customer_model import Customer, DB

#format for the log
LOG_FORMAT = "%(asctime)s %(filename)s: %(lineno)-3d %(levelname)s %(message)s"

#setup for formatter and log file
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'

#setup for file hanlder at error level
FILE_HANDLER = logging.FileHandler(LOG_FILE, mode='w')
FILE_HANDLER.setLevel(30)
FILE_HANDLER.setFormatter(FORMATTER)

#setup for console handler at debug level
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(10)
CONSOLE_HANDLER.setFormatter(FORMATTER)

#setup for logging set at debug level
LOGGER = logging.getLogger()
LOGGER.setLevel(10)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

#dict to convert debug input to log level
LOG_LEVEL = {'0': 51, '1': 40, '2': 30, '3': 10}

def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
                 #pylint: disable=too-many-arguments
    '''
    This function adds a customer and its data to the customer database
    '''
    logging.debug('Attempting to add customer %s to database', customer_id)
    with DB.atomic():
        try:
            added_customer = Customer.create(customer_id=customer_id, name=name,
                                             lastname=lastname, home_address=home_address,
                                             phone_number=phone_number, email_address=email_address,
                                             status=status, credit_limit=credit_limit)
            added_customer.save()
            logging.debug('Successfully added customer %s to database', customer_id)
        except p.DatabaseError:
            logging.error('Could not add customer %s to database', customer_id)

def search_customer(customer_id):
    '''
    This function searches for a customer in the database based on their ID
    '''
    logging.debug('Attempting to search customer %s', customer_id)
    try:
        searched_customer = Customer.select().where(Customer.customer_id == customer_id).get()
        logging.debug('Succesfully obtained searched customer %s', customer_id)
        returned_dict = {'name': searched_customer.name,
                         'lastname': searched_customer.lastname,
                         'email_address': searched_customer.email_address,
                         'phone_number': searched_customer.phone_number}
        return returned_dict
    except p.DoesNotExist:
        logging.error('Can not find customer %s, returning blank dict', customer_id)
        return {}


def delete_customer(customer_id):
    '''
    This function deletes a customer from the database
    '''
    logging.debug('Attempting to delete customer %s', customer_id)
    try:
        deleted_customer = Customer.select().where(Customer.customer_id == customer_id).get()
        number_of_deletions = deleted_customer.delete_instance()
        logging.debug('Successfully deleted %s customers', number_of_deletions)
        return number_of_deletions
    except p.DoesNotExist:
        logging.error('Can not find customer %s, deleting no customers', customer_id)
        return 0

def update_customer_credit(customer_id, credit_limit):
    '''
    This function updates the credit of a customer
    '''
    logging.debug('Attempting to update credit of customer %s', customer_id)
    try:
        updated_customer = Customer.select().where(Customer.customer_id == customer_id).get()
        updated_customer.credit_limit = credit_limit
        updated_customer.save()
        logging.debug('Successfully updated credit of customer %s', customer_id)
    except p.DoesNotExist:
        logging.error('Can not find customer %s, raising value error', customer_id)
        raise ValueError

def list_active_customers():
    '''
    This function lists all the customers that are active
    '''
    logging.debug('Attempting to list active customers')
    active_customers = Customer.select().where(Customer.status == 'active').count()
    logging.debug('Number of active customers: %s', active_customers)
    return active_customers
