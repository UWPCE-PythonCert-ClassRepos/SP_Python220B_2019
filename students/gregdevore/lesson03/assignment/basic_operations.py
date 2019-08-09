'''
This file contains basic operations for interacting with a customer database
'''

from customer_model import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the class from the model in the database')
database.create_tables([Customer])
database.close()

def add_customer(customer_id, name, lastname, home_address, phone_number,
                email_address, status, credit_limit):
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
