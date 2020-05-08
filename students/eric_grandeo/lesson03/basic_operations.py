'''
Basic opertions: add, search, and delete a customer. Update credit
limit and provide total number of active customers
'''

# pylint: disable=R0913
# pylint: disable=W

import logging
from peewee import *
from customers_model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

#database = SqliteDatabase('customers.db')


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
            LOGGER.info('Database add successful')
    except Exception as error:
        LOGGER.info('Error creating = {}'.format(name))
        LOGGER.info(error)
    finally:
        database.close()
        LOGGER.info('Database closed')

def search_customer(customer_id):
    '''Insert docstring'''
    try:
        customer = Customers.get(Customers.customer_id == customer_id)
        LOGGER.info('Customer found')
        return {'name':customer.name, 'lastname':customer.lastname,
                'email_address':customer.email_address, 'phone_number':customer.phone_number}
    except DoesNotExist as error:
        LOGGER.info(error)
        return {}

def delete_customer(customer_id):
    '''Insert docstring'''
    try:
        customer = Customers.get(Customers.customer_id == customer_id)
        customer.delete_instance()
        LOGGER.info('Customer deleted')
    except:
        LOGGER.info("Customer not found for delete")
        raise ValueError('Customer not found')

def update_customer_credit(customer_id, credit_limit):
    '''Updates the customer credit limit with a new number'''
    try:
        customer = Customers.get(Customers.customer_id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
        LOGGER.info('Customer credit limit updated')
    except:
        LOGGER.info("Customer not found to update credit limit")
        raise ValueError('Customer not found')

def list_active_customers():
    '''Count of all customers where active == True'''
    query = Customers.select().where(Customers.status).count()
    LOGGER.info("Number of active users: {}".format(query))
    return query

if __name__ == "__main__":
    database.create_tables([Customers])
    database.close()
