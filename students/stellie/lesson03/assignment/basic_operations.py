# Stella Kim
# Assignment 3: Storing Customer Data

"""Create customer database with Peewee ORM, SQLite and Python"""


import logging
from peewee import IntegrityError
from customer_model import CUSTOMER_DB, Customer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Logger has initiated.')

CUSTOMER_DB.create_tables([Customer])
LOGGER.info('Customer table created.')


def add_customer(customer_id, first_name, last_name, home_address,
                 phone, email, status, credit_limit):
    try:
        with CUSTOMER_DB.atomic():
            new_customer = Customer.create(
                customer_id=customer_id,
                first_name=first_name,
                last_name=last_name,
                home_address=home_address,
                phone=phone,
                email=email,
                status=status,
                credit_limit=credit_limit
            )
        new_customer.save()
        LOGGER.DEBUG(f'New customer: {last_name}, {first_name} added to DB')
    except IntegrityError as error:
        LOGGER.info('Failure: ID %s already in use.', customer_id)
        LOGGER.info(error)
        raise


def search_customer(customer_id):
    # This function will return a dictionary object with name, lastname,
    # email address and phone number of a customer or an empty dictionary
    # object if no customer was found.


def delete_customer(customer_id):
    # This function will delete a customer from the sqlite3 database.


def update_customer_credit(customer_id, credit_limit):
    # This function will search an existing customer by customer_id and
    # update their credit limit or raise a ValueError exception if the
    # customer does not exist.


def list_active_customers():
    # This function will return an integer with the number of customers
    # whose status is currently active.


CUSTOMER_DB.close()
