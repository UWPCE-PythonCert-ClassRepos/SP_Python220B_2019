"""
This file contains functions required to perform different
operations on customer database
"""

import logging
from Customer_model import  Customer, peewee, db



CUSTOMER_LIST = [('Andrew', 'peterson', '344 james ave' \
                  , 6308153728, 'a_peteerson@mail.com', True, 4500), \
                  ('Wang', 'Wou', '103 spring ave', \
                   2223334456, 'wang_wou@gmail.com', True, 22000)]
NAME = 0
LASTNAME = 1
ADDRESS = 2
PHONE = 3
EMAIL = 4
STATUS = 5
LIMIT = 6


LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
FORMATTER = logging.Formatter(LOG_FORMAT)

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setLevel(logging.DEBUG)

LOGGER.addHandler(STREAM_HANDLER)

def db_init():
    """
    Function to initialize DB, create
    and add tables
    """
    db.init('customer.db')
    db.create_tables([Customer])
    add_customer(CUSTOMER_LIST)

def add_customer(customer_data):
    """
    This function will add new custome to Customer table
    in customer.db
    """
    for customer in customer_data:
        try:
            with db.transaction():
                LOGGER.info('Adding \"%s\" as new customer', (customer[NAME], customer[LASTNAME]))
                new_customer = Customer.create(
                    name=customer[NAME],
                    lastname=customer[LASTNAME],
                    home_address=customer[ADDRESS],
                    phone_number=customer[PHONE],
                    email_address=customer[EMAIL],
                    status=customer[STATUS],
                    credit_limit=customer[LIMIT])
                LOGGER.info('New Customer : \"%s \" added to the database',\
                            (customer[NAME], customer[LASTNAME]))
                new_customer.save()

        except peewee.IntegrityError as exp:
            LOGGER.debug('IntegrityError, Error adding customer %s', exp)



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
        LOGGER.debug('No customer with id=%s was found', c_id)
        LOGGER.debug(exp)
    return a_customer_dict




def del_customer(c_id):
    """
    This function will delete a customer from the sqlite3 database.
    """
    try:
        LOGGER.info('Searching for customer with id = %s', c_id)
        a_customer = Customer.get(Customer.id == c_id)
        a_customer.delete_instance()
        LOGGER.info('customer %s with id = %s deleted', a_customer.name, c_id)

    except Customer.DoesNotExist as exp:
        LOGGER.debug('No customer with id=%s was found', c_id)
        LOGGER.debug(exp)

def update_customer_credit(c_id, credit_limit):
    """
    This function will search an existing customer by customer_id
    and update their credit limit or raise a ValueError exception if the customer does not exist.
    """

    try:
        LOGGER.info('Searching for customer with id = %s', c_id)
        customer = search_customer(c_id)
        a_customer = Customer.get(Customer.id == c_id)
        LOGGER.info('old credit limit = %s', a_customer.credit_limit)
        a_customer.credit_limit = credit_limit
        LOGGER.info('New credit limit = %s', a_customer.credit_limit)
        a_customer.save()
        return customer
    except Customer.DoesNotExist:
        LOGGER.info('No record found for customer_id %s', c_id)


def list_active_customers():
    """
    This function will return an integer with the number of
    customers whose status is currently active.
    """
    active_customer_count = Customer.select().where(Customer.status==True).count()
    return active_customer_count


if __name__ == '__main__':
    db_init()
    # search_customer(4)
    # print(search_customer(3))
    update_customer_credit(1, 25000)
    # update_customer_credit(4, 35000)
    # del_customer(4)
    print(list_active_customers())
    # db.close()
