"""
This file contains functions required to perform different
operations on customer database
"""

import logging
from customer_model import  Customer, peewee, DB



CUSTOMER_LIST = [('Andrew', 'peterson', '344 james ave' \
                  , 6308153728, 'a_peteerson@mail.com', True, 4500), \
                  ('Wang', 'Wou', '103 spring ave', \
                   2223334456, 'wang_wou@gmail.com', False, 22000)]
NAME = 0
LASTNAME = 1
ADDRESS = 2
PHONE = 3
EMAIL = 4
STATUS = 5
LIMIT = 6

def my_logger():
    """logger function to setup logging"""

    log_format = "<<%(asctime)s %(filename)s:" \
                 "Line:%(lineno)-3d %(levelname)s>> %(message)s"

    #define log file name format
    log_file_name = 'db.log'

    #assign log_format to formatter of logging
    formatter = logging.Formatter(log_format)

    f_handler = logging.FileHandler(log_file_name)
    f_handler.setFormatter(formatter)
    f_handler.setLevel('DEBUG')

    c_handler = logging.StreamHandler()
    c_handler.setFormatter(formatter)
    c_handler.setLevel('INFO')

    #create logger
    logger = logging.getLogger()
    logger.addHandler(f_handler)
    logger.addHandler(c_handler)
    logger.setLevel('DEBUG')

    return logger




def db_init():
    """
    Function to initialize DB, create/add
    tables and add customer data to the DB
    """
    DB.init('customer.db')
    DB.create_tables([Customer])
    [add_customer(customer) for customer in CUSTOMER_LIST if customer is not None]

def add_customer(customer):

    """
    This function will add new custome to Customer table
    in customer.db
    """
    try:
        with DB.transaction():
            logging.info('Adding \"%s\" as new customer', (customer[NAME], customer[LASTNAME]))
            new_customer = Customer.create(
                name=customer[NAME],
                lastname=customer[LASTNAME],
                home_address=customer[ADDRESS],
                phone_number=customer[PHONE],
                email_address=customer[EMAIL],
                status=customer[STATUS],
                credit_limit=customer[LIMIT])
            logging.debug('New Customer : \"%s \" added to the database',\
                        (customer[NAME], customer[LASTNAME]))
            new_customer.save()
    except peewee.IntegrityError as exp:
        logging.debug('IntegrityError, Error adding customer %s', exp)



def search_customer(c_id):
    """
    This function will return a dictionary object with name,
    lastname, email address and phone number of a customer or
    an empty dictionary object if no customer was found.
    """
    a_customer_dict = dict()
    try:
        a_customer = Customer.get(Customer.id == c_id)
        a_customer_dict = {'id': a_customer.id,
                           'name': a_customer.name,
                           'last_name': a_customer.lastname,
                           'phone_number': a_customer.phone_number,
                           'email_address': a_customer.email_address,}


        return a_customer_dict

    except Customer.DoesNotExist as exp:
        logging.debug('No customer with id=%s was found', c_id)
        logging.debug(exp)
    return a_customer_dict




def del_customer(c_id):
    """
    This function will delete a customer from the sqlite3 database.
    """
    try:
        logging.info('Searching for customer with id = %s', c_id)
        a_customer = Customer.get(Customer.id == c_id)
        a_customer.delete_instance()
        logging.info('customer %s with id = %s deleted', a_customer.name, c_id)

    except Customer.DoesNotExist as exp:
        logging.debug('No customer with id=%s was found', c_id)
        logging.debug(exp)

def update_customer_credit(c_id, credit_limit):
    """
    This function will search an existing customer by customer_id
    and update their credit limit or raise a ValueError exception if the customer does not exist.
    """

    try:
        logging.info('Searching for customer with id = %s', c_id)
        customer = search_customer(c_id)
        a_customer = Customer.get(Customer.id == c_id)
        logging.info('old credit limit = %s', a_customer.credit_limit)
        a_customer.credit_limit = credit_limit
        logging.info('New credit limit = %s', a_customer.credit_limit)
        a_customer.save()
        return customer
    except Customer.DoesNotExist:
        logging.info('No record found for customer_id %s', c_id)


def list_active_customers():
    """
    This function will return an integer with the number of
    customers whose status is currently active.
    """
    active_customer_count = Customer.select().where(Customer.status).count()
    return active_customer_count


# def query_all_customers():
#     """ Generator to return customer_id for all the
#     customers int the DB"""
#     query = Customer.select()
#     c_id = (customer.id for customer in query)
#     return c_id

def query_all_customers():
    """Return entries for all the customers
    in the DB """
    query = Customer.select()
    c_id = (customer.id for customer in query)
    all_customers = [search_customer(customer_id) for customer_id in c_id]
    return all_customers


if __name__ == '__main__':
    my_logger()
    db_init()
