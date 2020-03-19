"""basic functions for managing db"""
# pylint: disable=unused-import, unused-wildcard-import,
# pylint: disable=too-few-public-methods, too-many-arguments, wildcard-import
# pylint: disable=logging-format-interpolation, pointless-string-statement
import logging
import datetime
from customers import *
from peewee import *
"""logging setup"""
LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
FORMATTER = logging.Formatter(LOG_FORMAT)

LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.DEBUG)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOG = logging.getLogger()
if not LOG.hasHandlers():
    LOG.addHandler(FILE_HANDLER)
    LOG.addHandler(CONSOLE_HANDLER)


with DATABASE:
    DATABASE.create_tables([Customer])

def add_customer(customer_id,
                 name,
                 last_name,
                 home_address,
                 phone_number,
                 email_address,
                 status,
                 credit_limit):
    """Adds a customer to the database"""

    try:
        new_customer = Customer.create(customer_id=customer_id,
                                       name=name,
                                       last_name=last_name,
                                       home_address=home_address,
                                       phone_number=phone_number,
                                       email_address=email_address,
                                       status=status,
                                       credit_limit=credit_limit)
        new_customer.save()
        LOG.debug(f"Added Customer {customer_id} to database")
    except TypeError:
        LOG.debug(f"Couldn't add customer{customer_id}")


def search_customer(customer_id):
    """Searches for a customer"""
    try:
        searched_customer = Customer.get(Customer.customer_id == customer_id)
        customer_dictionary = {"Name": searched_customer.name,
                               "Last Name": searched_customer.last_name,
                               "Email Address": searched_customer.email_address,
                               "Phone number": searched_customer.phone_number}
    except DoesNotExist:
        LOG.debug(f"customer search failed, no data for {customer_id} exists")
        customer_dictionary = {}

    return customer_dictionary


def delete_customer(customer_id):
    """Deletes a customer"""
    try:
        deleted_customer = Customer.get(Customer.customer_id == customer_id)
        deleted_customer.delete_instance()
        LOG.debug(f"deleted {customer_id} from database")
    except DoesNotExist:
        LOG.debug(f"customer deletion failed, no data for {customer_id} exists")


def update_customer_credit(customer_id, credit_limit):
    """Updates a customers credit limit"""
    try:
        updated_customer = Customer.get(Customer.customer_id == customer_id)
        updated_customer.credit_limit = credit_limit
        updated_customer.save()
        LOG.debug(f"updated customer: {customer_id} credit limit to {credit_limit}")
    except DoesNotExist:
        LOG.debug(f"customer credit update failed, no data for {customer_id} exists")
        raise ValueError


def list_active_customers():
    """Counts number of active customers"""
    active_customers = Customer.select().where(Customer.status)
    return len(active_customers)
