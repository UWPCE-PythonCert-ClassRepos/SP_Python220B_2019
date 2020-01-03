"""Module for basic operations"""

# pylint: disable=too-many-arguments
# pylint: disable=logging-format-interpolation

import logging
import peewee as pw
import customer_model as cm

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


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
    # database.transaction; all work given to database gets done or none of it
    with cm.DATABASE.transaction():
        try:
            # .create inserts the data into the database
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
            LOGGER.info(f"Added customer #{customer_id}")
        except pw.IntegrityError:
            LOGGER.info(f"Unique constraint failed for customer {customer_id}")
            raise pw.IntegrityError


def search_customer(customer_id):
    """Return a dictionary with customer information"""
    with cm.DATABASE.transaction():
        try:
            # .get() finds the attribute equal to the set attribute
            a_customer = cm.Customer.get(
                cm.Customer.customer_id == customer_id)
            # Creating dictionary to return with customer information
            a_customer = {'first_name': a_customer.first_name,
                          'last_name': a_customer.last_name,
                          'email_address': a_customer.email_address,
                          'phone_number': a_customer.phone_number}
            LOGGER.info(f"Found customer #{customer_id}")
            return a_customer
        except pw.DoesNotExist:
            LOGGER.info(f"Customer #{customer_id} not found")
            a_customer = {}
            return a_customer  # Empty dictionary if no customer was found


def delete_customer(customer_id):
    """Delete a customer from the database"""
    with cm.DATABASE.transaction():
        try:
            LOGGER.info(f"Searching for customer #{customer_id}")
            a_customer = cm.Customer.get(
                cm.Customer.customer_id == customer_id)
            # .delete_instance() will delete the record
            a_customer.delete_instance()
            a_customer.save()
            LOGGER.info("Deleted customer")
        except pw.DoesNotExist:
            LOGGER.info(f"Customer #{customer_id} not found")
            raise ValueError


def update_customer_credit(customer_id, credit_limit):
    """Search an existing customer and update their credit limit"""
    with cm.DATABASE.transaction():
        try:
            a_customer = cm.Customer.get(
                cm.Customer.customer_id == customer_id)
            a_customer.credit_limit = credit_limit
            a_customer.save()
            LOGGER.info(f"Updating credit limit to ${credit_limit}")
        except pw.DoesNotExist:
            LOGGER.info(f"Customer {customer_id} not found")
            raise ValueError


def list_active_customers():
    """Return an integer with the number of active customers"""
    with cm.DATABASE.transaction():
        # .select() has a .where() method to specify criteria for searching
        active_customers = cm.Customer.select().where(
            cm.Customer.status == "Active").count()
        LOGGER.info(f"Count of active customers: {active_customers}")
        return active_customers


if __name__ == "__main__":
    setup_database()
    teardown_database()
