'''
This file contains basic operations for interacting with a customer database
'''

import logging
from peewee import OperationalError, IntegrityError, DoesNotExist
from customer_model import database, Customer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the class from the model in the database')
database.create_tables([Customer])
database.close()

def add_customer(id, firstname, lastname, address, phone,email, status, credit_limit):
    try:
        with database.transaction():
            new_customer = Customer.create(
            id = id,
            firstname = firstname,
            lastname = lastname,
            address = address,
            phone = phone,
            email = email,
            status = status,
            credit_limit = credit_limit)
        new_customer.save()
        logger.info('Database add successful')
    except (OperationalError, IntegrityError, DoesNotExist) as e:
        logger.info(f'Error creating entry for customer {id}, see error below')
        logger.info(e)

def search_customer(id):
    try:
        customer = Customer.get(Customer.id == id)
        # Return dictionary of customer name, email, phone
        return {'firstname': customer.firstname, 'lastname': customer.lastname,
                'email': customer.email, 'phone':customer.phone}
    except DoesNotExist as e:
        # Customer not found, return empty dictionary
        return {}

def delete_customer(id):
    # Retrieve and delete customer from database
    customer = Customer.get(Customer.id == id)
    customer.delete_instance()
