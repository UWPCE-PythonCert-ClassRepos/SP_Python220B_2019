"""Module for basic operations"""

# pylint: disable=too-many-arguments

import logging
import peewee as pw
import customer_model as cm

# Logging Setup
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = "db.log"

FORMATTER = logging.Formatter(LOG_FORMAT)  # Formats output by string format

FILE_HANDLER = logging.FileHandler(LOG_FILE)  # Create file log message handler
FILE_HANDLER.setFormatter(FORMATTER)  # Create formatter and add to handler

CONSOLE_HANDLER = logging.StreamHandler()  # Create console log message handler
CONSOLE_HANDLER.setFormatter(FORMATTER)  # Create formatter and add to handler

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)  # Add file handler to logger
LOGGER.addHandler(CONSOLE_HANDLER)  # Add console handler to logger


def add_customer(customer_id, first_name, last_name, home_address,
                 phone_number, email_address, status, credit_limit):
    """Add a new customer to the database"""
    try:
        cus = cm.Customer.create(customer_id=customer_id,
                                 first_name=first_name,
                                 last_name=last_name,
                                 home_address=home_address,
                                 phone_number=phone_number,
                                 email_address=email_address,
                                 status=status,
                                 credit_limit=credit_limit)
        cus.save()
        LOGGER.info("Added customer [%s]", customer_id)
    except pw.IntegrityError:
        LOGGER.error("Customer [%s] not added to database!", customer_id)
        raise pw.IntegrityError


def search_customer(customer_id):
    """Return a dictionary with customer information"""
    try:
        cus = cm.Customer.get(cm.Customer.customer_id == customer_id)
        cus = {'first_name': cus.first_name,
               'last_name': cus.last_name,
               'email_address': cus.email_address,
               'phone_number': cus.phone_number}
        LOGGER.info("Found customer [%s]", customer_id)
        return cus
    except pw.DoesNotExist:
        LOGGER.warning("Customer [%s] not in database!", customer_id)
        cus = dict()
        return cus


def delete_customer(customer_id):
    """Delete a customer from the database"""
    try:
        LOGGER.info("Searching for customer [%s]", customer_id)
        cus = cm.Customer.get(cm.Customer.customer_id == customer_id)
        cus.delete_instance()
        cus.save()
        LOGGER.info("Deleted customer")
    except pw.DoesNotExist:
        LOGGER.warning("Customer [%s] not in database!", customer_id)
        raise ValueError


def update_customer_credit(customer_id, credit_limit):
    """Search an existing customer and update their credit limit"""
    try:
        cus = cm.Customer.get(cm.Customer.customer_id == customer_id)
        cus.credit_limit = credit_limit
        cus.save()
        LOGGER.info("Updating customer [%s] credit limit to $%s",
                    customer_id, credit_limit)
    except pw.DoesNotExist:
        LOGGER.warning("Error updating credit limit for customer [%s]!",
                       customer_id)
        raise ValueError


def list_active_customers():
    """Return an integer with the number of active customers"""
    active = cm.Customer.select().where(cm.Customer.status).count()
    LOGGER.info("Active customers: %s", active)
    return active


def display_customers():
    """Returns all customers with first name and last name"""
    LOGGER.info("Display all customers")
    gen_comp = ((f"{cus.first_name}" + " " + f"{cus.last_name}")
                for cus in cm.Customer.select())
    cus_list = []
    for cus_name in gen_comp:
        cus_list.append(cus_name)
        LOGGER.info(cus_name)
    return cus_list


if __name__ == "__main__":
    cm.DATABASE.drop_tables([cm.Customer])
    cm.DATABASE.create_tables([cm.Customer])
