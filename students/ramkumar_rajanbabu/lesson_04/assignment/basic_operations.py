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



def setup_database():
    """Setup database"""
    cm.DATABASE.drop_tables([cm.Customer])
    LOGGER.info("Cleared the database")
    cm.DATABASE.create_tables([cm.Customer])
    LOGGER.info("Created a table in database")


def teardown_database():
    """Close database"""
    cm.DATABASE.close()
    LOGGER.info("Closed database")


def add_customer(customer_id, first_name, last_name, home_address,
                 phone_number, email_address, status, credit_limit):
    """Add a new customer to the database"""
    with cm.DATABASE.transaction():
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
            LOGGER.info(f"Added customer #{customer_id}")
        except pw.IntegrityError:
            LOGGER.info(f"Unique constraint failed for customer {customer_id}")
            raise pw.IntegrityError


def search_customer(customer_id):
    """Return a dictionary with customer information"""
    with cm.DATABASE.transaction():
        try:
            cus = cm.Customer.get(cm.Customer.customer_id == customer_id)
            cus = {'first_name': cus.first_name,
                   'last_name': cus.last_name,
                   'email_address': cus.email_address,
                   'phone_number': cus.phone_number}
            LOGGER.info(f"Found customer #{customer_id}")
            return cus
        except pw.DoesNotExist:
            LOGGER.info(f"Customer #{customer_id} not found")
            cus = {}
            return cus


def delete_customer(customer_id):
    """Delete a customer from the database"""
    with cm.DATABASE.transaction():
        try:
            LOGGER.info(f"Searching for customer #{customer_id}")
            cus = cm.Customer.get(cm.Customer.customer_id == customer_id)
            cus.delete_instance()
            cus.save()
            LOGGER.info("Deleted customer")
        except pw.DoesNotExist:
            LOGGER.info(f"Customer #{customer_id} not found")
            raise ValueError


def update_customer_credit(customer_id, credit_limit):
    """Search an existing customer and update their credit limit"""
    with cm.DATABASE.transaction():
        try:
            cus = cm.Customer.get(cm.Customer.customer_id == customer_id)
            cus.credit_limit = credit_limit
            cus.save()
            LOGGER.info(f"Updating credit limit to ${credit_limit}")
        except pw.DoesNotExist:
            LOGGER.info(f"Customer {customer_id} not found")
            raise ValueError


def list_active_customers():
    """Return an integer with the number of active customers"""
    with cm.DATABASE.transaction():
        active = cm.Customer.select().where(cm.Customer.status).count()
        LOGGER.info(f"Active customers: {active}")
        return active

if __name__ == "__main__":
    setup_database()
    add_customer(100, 'Peter', 'Parker',
                 '135 W. 50th Street, New York City, NY 10011',
                 '212-576-4000', 'peter.parker@marvel.com', True, 1000)
    add_customer(200, 'Iron', 'Man',
                 '17801 International Blvd, Seattle, WA 98101',
                 '206-787-5388', 'iron.man@gmail.com', True, 5000)
    add_customer(300, 'Ramkumar', 'Rajanbabu',
                 '7525 166th Ave NE, Redmond, WA 98052',
                 '425-556-2900', 'ram.kumar@gmail.com', False, 7078)
    search_customer(200)
    update_customer_credit(200, 9000)
    list_active_customers()
    delete_customer(200)
    list_active_customers()
    #delete_customer(200)
    teardown_database()
