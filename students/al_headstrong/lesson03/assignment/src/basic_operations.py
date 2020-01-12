"""
    This module contains functions to use and manipulate the customer database.
"""

from customer_model import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_customer(customer_id,
                 name,
                 lastname,
                 home_address,
                 phone_number,
                 email_address,
                 status,
                 credit_limit):
    """This function adds customer data to 'customer.db' database."""

    try:
        with database.transaction():
            new_customer = Customer.create(customer_id=customer_id,
                                           name=name,
                                           lastname=lastname,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           status=status,
                                           credit_limit=credit_limit)
            new_customer.save()
            logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = Customer {customer_id}')
        logger.info(e)
        raise err