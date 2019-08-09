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

def add_customer(customer_id, name, lastname, home_address, phone_number,
                email_address, status, credit_limit):
    try:
        with database.transaction():
            new_customer = Customer.create(
            id = customer_id,
            firstname = name,
            lastname = lastname,
            address = home_address,
            phone = phone_number,
            email = email_address,
            status = status,
            credit_limit = credit_limit)
        new_customer.save()
        logger.info('Database add successful')
    except (OperationalError, IntegrityError, DoesNotExist) as e:
        logger.info(f'Error creating entry for customer {customer_id}, see error below')
        logger.info(e)
