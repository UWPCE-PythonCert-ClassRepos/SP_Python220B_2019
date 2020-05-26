'''
Basic opertions: add, search, and delete a customer. Update credit
limit and provide total number of active customers
'''

# pylint: disable=R0913
# pylint: disable=W

import logging
import datetime
from peewee import *
from customers_model import *

#logging.basicConfig(level=logging.INFO)
#LOGGER = logging.getLogger(__name__)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

LOG_FILE = 'db.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(FILE_HANDLER)


def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    '''Add customer to DB'''

    try:
        with database.transaction():
            new_customer = Customers.create(
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
            LOGGER.info('Added userid: {} to database'.format(customer_id))
    except Exception as error:
        LOGGER.error('Error creating = {}: {}'.format(name, error))
        #LOGGER.error(error)
        
    finally:
        database.close()
        LOGGER.info('Database closed')

    return new_customer

def search_customer(customer_id):
    '''Search for a customer by id'''
    try:
        customer = Customers.get(Customers.customer_id == customer_id)
        LOGGER.info('Customer {} found'.format(customer_id))
        return {'name':customer.name, 'lastname':customer.lastname,
                'email_address':customer.email_address, 'phone_number':customer.phone_number}
    except DoesNotExist as error:
        LOGGER.error("User does not exist: {}".format(error))
        return {}

def delete_customer(customer_id):
    '''Delete a customer by the id'''
    try:
        customer = Customers.get(Customers.customer_id == customer_id)
        customer.delete_instance()
        LOGGER.info('Customer id {} deleted'.format(customer_id))
    except:
        LOGGER.error("Customer {} not found for delete".format(customer_id))
        raise ValueError('Customer not found')

def update_customer_credit(customer_id, credit_limit):
    '''Updates the customer credit limit with a new number'''
    try:
        customer = Customers.get(Customers.customer_id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
        LOGGER.info('Customer credit limit updated')
    except:
        LOGGER.error("Customer {} not found to update credit limit".format(customer_id))
        raise ValueError('Customer not found')

def list_active_customers():
    '''Count of all customers where active == True'''
    query = Customers.select().where(Customers.status).count()
    LOGGER.info("Number of active users: {}".format(query))
    return query
    
    
def return_active_customers():
    '''Iterable that return the list of all customers where active == True'''
    query = Customers.select().where(Customers.status)
    for customer in query:
        LOGGER.info("Active customer: {}".format(customer))
        print(customer)

def add_multiple_customers(customers):
    "Add multiple customers to the db using comprehension"
    return [add_customer(**customer) for customer in customers ]
 
def return_all_customers():
    '''This is a generator that yields all customers by ID and name'''
    for customer_id in Customers.select(Customers.customer_id):
        yield search_customer(customer_id)

def print_all_customers():
    '''Display all customers on screen'''
    for customer in return_all_customers():
        print(customer)

if __name__ == "__main__":
    database.create_tables([Customers])
    database.close()

