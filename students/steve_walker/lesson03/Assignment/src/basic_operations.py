"""
Establishes CRUD tools for the customers database.
"""

# pylint: disable=W0614, W0401, C0103, W1202, R0913

import logging
from peewee import *
from src.customer_model import Customer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SqliteDatabase("customers.db")

# Creates the Customer table in customers.db if it doesn't already exist.
db.create_tables([Customer], safe=True)


def connect_customer_db():
    """Helper function to create db."""

    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;')


def add_customer(customer_id, first_name, last_name, home_address,
                 phone_number, email_address, active_customer, credit_limit):
    """Add customer to customer_database"""

    try:
        connect_customer_db()
        with db.atomic():
            new_customer = Customer.create(customer_id=customer_id,
                                           first_name=first_name,
                                           last_name=last_name,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           active_customer=active_customer,
                                           credit_limit=credit_limit)
            new_customer.save()
            logger.info(f"Added {customer_id} to the database.")

    except TypeError as err:
        logger.info(f"Could not add {customer_id} to the database.")
        logger.info(err)
        raise TypeError

    finally:
        db.close()


def search_customer(customer_id):
    """
    Return dictionary object with a customer's name and contact info
    if found, otherwise return an empty dictionary object.
    """

    try:
        connect_customer_db()
        customer = Customer.get_by_id(customer_id)
        logger.info(f"{customer_id} found. Returning name and contact info.")

        return {'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email_address': customer.email_address,
                'phone_number': customer.phone_number}

    except DoesNotExist:
        logger.info(f"{customer_id} does not exist in the database.")
        return {}

    finally:
        db.close()


def delete_customer(customer_id):
    """Delete a customer from the customers database."""

    try:
        connect_customer_db()
        Customer.get_by_id(customer_id).delete_instance()
        logger.info(f"{customer_id} deleted from the database.")

    except DoesNotExist:
        logger.info(f"{customer_id} does not exist in the database.")
        raise DoesNotExist

    finally:
        db.close()


def update_customer_credit(customer_id, credit_limit):
    """Update a customer's credit limit."""

    try:
        connect_customer_db()
        customer = Customer.get_by_id(customer_id)
        customer.credit_limit = credit_limit
        customer.save()
        logger.info(f"Credit limit for {customer_id} updated to {credit_limit}.")

    except DoesNotExist as err:
        logger.info(f"{customer_id} does not exist in the database.")
        raise DoesNotExist

    finally:
        db.close()


def list_active_customers():
    """Return the number of customers with an active_status of True."""

    try:
        connect_customer_db()
        active_count = Customer.select().where(Customer.active_customer).count()
        logger.info(f"There are currently {active_count} active customers.")
        return active_count

    finally:
        db.close()
