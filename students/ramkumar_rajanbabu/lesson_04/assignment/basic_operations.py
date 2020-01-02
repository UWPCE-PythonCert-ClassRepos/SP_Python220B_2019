"""Module for basic operations"""

# pylint: disable=too-many-arguments
# pylint: disable=logging-format-interpolation

import logging
import peewee as pw
import customer_model as cm

# Logging Setup
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = "db.log"

FORMATTER = logging.Formatter(LOG_FORMAT) # Formats output by string format

FILE_HANDLER = logging.FileHandler(LOG_FILE) # Create file log message handler
FILE_HANDLER.setFormatter(FORMATTER)  # Create formatter and add to handler

CONSOLE_HANDLER = logging.StreamHandler()  # Create console log message handler
CONSOLE_HANDLER.setFormatter(FORMATTER)  # Create formatter and add to handler

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER) # Add file handler to logger
LOGGER.addHandler(CONSOLE_HANDLER) # Add console handler to logger


def add_customer(customer_id, first_name, last_name, home_address,
                 phone_number, email_address, status, credit_limit):
    """Add a new customer to the database"""
    with cm.DATABASE.transaction():
        LOGGER.info(f"In process of adding customer {customer_id}")
        new_customer = cm.Customer.create(customer_id=customer_id,
                                          first_name=first_name,
                                          last_name=last_name,
                                          home_address=home_address,
                                          phone_number=phone_number,
                                          email_address=email_address,
                                          status=status,
                                          credit_limit=credit_limit)
        new_customer.save()
        LOGGER.info(f"Added a new customer {first_name} {last_name}")


def search_customer(customer_id):
    """Return a dictionary with customer information"""
    with cm.DATABASE.transaction():
        try:
            LOGGER.info(f"Searching for customer {customer_id}")
            a_customer = cm.Customer.get(
                cm.Customer.customer_id == customer_id)
            a_customer = {'first_name': a_customer.first_name,
                          'last_name': a_customer.last_name,
                          'email_address': a_customer.email_address,
                          'phone_number': a_customer.phone_number}
            LOGGER.info(f"Found customer {customer_id}")
            return a_customer
        except pw.DoesNotExist:
            LOGGER.warning("Customer not found")
            return {}


def delete_customer(customer_id):
    """Delete a customer from the database"""
    with cm.DATABASE.transaction():
        if cm.Customer.get(cm.Customer.customer_id == customer_id):
            LOGGER.info(f"Found customer {customer_id}")
            a_customer = cm.Customer.get(
                cm.Customer.customer_id == customer_id)
            a_customer.delete_instance()
            LOGGER.info(f"Deleted customer {customer_id}")
        else:
            LOGGER.warning("Customer not found")
            raise pw.DoesNotExist


def update_customer_credit(customer_id, credit_limit):
    """Search an existing customer and update their credit limit"""
    with cm.DATABASE.transaction():
        try:
            LOGGER.info("Updating credit limit")
            a_customer = cm.Customer.get(
                cm.Customer.customer_id == customer_id)
            a_customer.credit_limit = credit_limit
            a_customer.save()
            LOGGER.info(f"Updated credit limit to {credit_limit}")
        except pw.DoesNotExist:
            LOGGER.warning("Error updating credit limit")
            raise ValueError


def list_active_customers():
    """Return an integer with the number of active customers"""
    with cm.DATABASE.transaction():
        LOGGER.info("Obtaining number of active customers")
        active_customers = cm.Customer.select().where(
            cm.Customer.status == "Active").count()
        LOGGER.info(f"Count of active customers: {active_customers}")
        return active_customers
