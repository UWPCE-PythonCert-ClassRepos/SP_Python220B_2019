# pylint: disable=unused-import, singleton-comparison

"""This module defines the standard set of CRUD operations for the Customer database."""

import logging
from customer_model import CUSTOMER_DB, Customer, DoesNotExist, IntegrityError

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'db.log'

FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(FILE_HANDLER)

CUSTOMER_DB.create_tables([Customer])

def add_customer(**kwargs):
    """
    This takes the specified dictionary and attempts to create a new customer record.

    Returns True on successful creation; otherwise, returns False.
    """
    with CUSTOMER_DB.transaction():
        try:
            new_customer = Customer.create(**kwargs)
        except IntegrityError as exception_info:
            logging.error('Error creating record: %s', exception_info)
            return False
        else:
            new_customer.save()
            logging.debug('Successfully creating record: %s', kwargs)
            return True

def search_customer(customer_id):
    """
    This function returns the Customer record for the specified customer_id, if found.

    If no Customer record is found, it will raise a ValueError.
    """
    customer = Customer.select().where(Customer.customer_id == customer_id).dicts()
    customer_record = customer.first()
    if customer_record is None:
        logging.warning('Unable to find record for customer_id == %s', customer_id)
        return {}

    logging.debug('Successfully found record for customer_id == %s (%s)',
                  customer_id, customer_record)
    return customer_record

def delete_customer(customer_id):
    """
    This function will attempt to delete the Customer record for the specified customer_id.

    Returns True if successful; otherwise, returns False.
    """
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.delete_instance()
        logging.debug('Successfully deleted record for customer_id == %s', customer_id)
        return True
    except (IndexError, DoesNotExist):
        logging.error('Unable to delete record for customer_id == %s', customer_id)
        return False

def update_customer_credit(customer_id, credit_limit):
    """
    This function will attempt to update the credit_limit value for the specified customer_id.

    Returns True if successful; otherwise, returns False.
    """
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
        logging.debug('Successfully updated credit limit to %s for customer_id == %s',
                      credit_limit, customer_id)
        return True
    except (IndexError, DoesNotExist):
        logging.error('Unable to update record for customer_id == %s', customer_id)
        return False


def list_active_customers():
    """
    This function will return the count of active customers.
    """
    return Customer.select().where(Customer.is_active == True).count()


class CustomerList:
    """
    A class to provide a iterator to be step through the customer list.
    """
    def __init__(self, max=1000):
        """
        Initialize the iterator.
        """
        self.cur_customer = 0
        self.full_list = Customer.select().dicts()
        # The calling function can set a lower max than the length of the customer DB
        self.max = (max if max < len(self.full_list) else len(self.full_list)) - 1

    def __iter__(self):
        """
        Define the iteration
        """
        return self

    def __next__(self):
        """
        Define the next functionality of the iterator
        """
        if self.cur_customer > self.max:
            raise StopIteration
        return_val = self.full_list[self.cur_customer]
        self.cur_customer += 1
        return return_val

def customer_list_ids(max=1000):
    customers = Customer.select().dicts()
    if max >= len(customers):
        max = len(customers)
    max -= 1
    i = 0
    while i <= max:
        yield customers[i]['customer_id']
        i += 1

CUSTOMER_DB.close()
