"""Module for basic operations"""

# pylint: disable=too-many-arguments
# pylint: disable=logging-format-interpolation

import logging
import peewee as pw
import customer_model as cm


LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT) # Formats output by string format

FILE_HANDLER = logging.FileHandler("db.log") # Create a file log message handler
FILE_HANDLER.setLevel(logging.INFO)  # Set level of messages in file
FILE_HANDLER.setFormatter(FORMATTER)  # Create formatter and add to handler

CONSOLE_HANDLER = logging.StreamHandler()  # Create console file log message handler
CONSOLE_HANDLER.setLevel(logging.DEBUG)  # Set level of messages in console
CONSOLE_HANDLER.setFormatter(FORMATTER)  # Create formatter and add to handler

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER) # Add file handler to logger
LOGGER.addHandler(CONSOLE_HANDLER) # Add console handler to logger
LOGGER.setLevel(logging.INFO)


def add_customer(customer_id, first_name, last_name, home_address,
                 phone_number, email_address, status, credit_limit):
    """Add a new customer to the database"""
    # database.transaction; all work given to database gets done or none of it
    with cm.DATABASE.transaction():
        # .create inserts the data into the database
        LOGGER.info(f"In process of adding customer {customer_id}")
        new_customer = cm.Customer.create(customer_id=customer_id,
                                          first_name=first_name,
                                          last_name=last_name,
                                          home_address=home_address,
                                          phone_number=phone_number,
                                          email_address=email_address,
                                          status=status,
                                          credit_limit=credit_limit)
        # .save() will write the data to the database
        new_customer.save()
        LOGGER.info(f"Added a new customer {first_name} {last_name}")


def search_customer(customer_id):
    """Return a dictionary with customer information"""
    with cm.DATABASE.transaction():
        try:
            LOGGER.info(f"Searching for customer {customer_id}")
            # .get() finds the attribute equal to the set attribute
            a_customer = cm.Customer.get(
                cm.Customer.customer_id == customer_id)
            # Creating dictionary to return with customer information
            a_customer = {'first_name': a_customer.first_name,
                          'last_name': a_customer.last_name,
                          'email_address': a_customer.email_address,
                          'phone_number': a_customer.phone_number}
            LOGGER.info(f"Found customer {customer_id}")
            return a_customer
        except pw.DoesNotExist:
            LOGGER.info("Customer not found")
            # Empty dictionary if no customer was found
            return {}


def delete_customer(customer_id):
    """Delete a customer from the database"""
    with cm.DATABASE.transaction():
        if cm.Customer.get(cm.Customer.customer_id == customer_id):
            LOGGER.info(f"Found customer {customer_id}")
            a_customer = cm.Customer.get(
                cm.Customer.customer_id == customer_id)
            # .delete_instance() will delete the record
            a_customer.delete_instance()
            LOGGER.info("Deleted customer information")
        else:
            LOGGER.info("Customer not found")
            raise pw.DoesNotExist


def update_customer_credit(customer_id, credit_limit):
    """Search an existing customer and update their credit limit"""
    with cm.DATABASE.transaction():
        try:
            LOGGER.info("Updating credit limit")
            a_customer = cm.Customer.get(
                cm.Customer.customer_id == customer_id)
            a_customer.credit_limit = float(credit_limit)
            a_customer.save()
        except pw.DoesNotExist:
            raise ValueError


def list_active_customers():
    """Return an integer with the number of active customers"""
    with cm.DATABASE.transaction():
        LOGGER.info("Obtaining number of active customers")
        # .select() has a .where() method to specify criteria for searching
        active_customers = cm.Customer.select().where(
            cm.Customer.status == "Active").count()
        return active_customers
