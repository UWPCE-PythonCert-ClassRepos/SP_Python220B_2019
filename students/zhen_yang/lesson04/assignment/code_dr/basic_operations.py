""" This modules defines severl functions to deliver some
    database requirements.
"""
import logging
from peewee import SqliteDatabase
from code_dr.customer_model import Customer, database


#set logging configuration
log_format = "%(levelname)s %(filename)s %(message)s"
log_file = 'db.log'

# Create a "formatter" using our format string
formatter = logging.Formatter(fmt=log_format)
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)# only warning info and above to file

# Create a 'console' log message handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)# all info to console

# Get the "root" logger.
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

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

    customer = {}
    # using Generator Comprehesions to get the customer iterator.
    for the_customer in (C for C in Customer if C.customer_id == customer_id):
        key_list = ['name', 'lastname', 'phone_number', 'email_address']
        val_list = [the_customer.name, the_customer.lastname,
                    the_customer.phone_number, the_customer.email_address]
        customer = dict(zip(key_list, val_list))
        break
    if customer:
        logger.info(f'Found customer {customer_id} successfully.')
    else:
        logger.info(f'search customer {customer_id} fail.')
        logger.info(f'Customer {customer_id} is not found.')
    return customer

def delete_customer(customer_id):
    """ This function will delete a customer from the customers.db database """
    logger.info('In delete_customer().')

    # using filter() to get the customer iterator
    for customer in filter(lambda c: c.customer_id == customer_id, Customer):
        customer.delete_instance()
        logger.info(f'Delete customer {customer.customer_id} successfully.')
        return
    logger.info(f'Delete customer {customer_id} fail.')
    logger.info(f'Customer {customer_id} is not in the datbase.')

def update_customer_credit(customer_id, credit_limit):
    """ This function will search an existing customer by customer_id and
        update their credit limit or raise a ValueError exception if the
        customer does not exist.
    """
    # using filter() to get the customer iterator
    for customer in filter(lambda c: c.customer_id == customer_id, Customer):
        customer.credit_limit = credit_limit
        customer.save()
        logger.info(f'Customer {customer.customer_id} credit limit is '
                    'updated successfully .')
        return
    logger.info(f'Update customer {customer_id} credit limit fail.')
    logger.info(f'Customer {customer_id} does not exist.')
    #raise ValueError

def list_active_customers():
    """ This function will return an integer with the number of customers
         whose status is currently active.
    """
    # using filter to get the iterator
    return len(list(filter(lambda c: c.status, Customer)))
