"""
This script contains the methods to manipulate the database.
"""
import os
import logging
import peewee
from customer_model import DATABASE, Customer, PATH

#pylint: disable = too-many-arguments

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = os.path.join(PATH, 'logs', 'db.log')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE, 'a+')
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.INFO)

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setLevel(logging.DEBUG)

LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(STREAM_HANDLER)

def add_customer(customer_id, name, last_name, home_address, phone_number,
                 email_address, status, credit_limit):
    """
    Add the data to the table
    :parm customer_id: a unique integer value
    :parm name: customer first name.
    :parm last_name: customer last name.
    :parm home_address: customer home address.
    :parm phone_number: customer phone number.
    :parm email_address: customer email address.
    :parm status: customer active/nonactive status. default= False.
    :parm credit_limit: numeric value representing money
    """
    LOGGER.debug("Adding a new customer to the table")
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
        LOGGER.info("New customer added.")
    except peewee.IntegrityError:
        msg = f'Unique constrain failed for customer id = {customer_id}'
        LOGGER.error(msg)
        raise peewee.IntegrityError


def search_customer(customer_id):
    """
    Search the customer data based on the customer_id.
    :parm customer_id: customer id.
    :return: customer data in the dictionary format.
    """
    msg = f"Searching the table for customer {customer_id}"
    LOGGER.debug(msg)
    data_dict = {}
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        data_dict.update({'Name':customer.name, 'Last Name':customer.last_name,
                          'Email': customer.email_address,
                          'Phone':customer.phone_number})
        msg = f'Customer {customer_id} was found'
        LOGGER.info(msg)
    except peewee.DoesNotExist:
        msg = f'Customer {customer_id} is not found in the database'
        LOGGER.warning(msg)
    return data_dict


def delete_customer(customer_id):
    """
    Delete the customer from the database based on the customer_id
    :parm customer_id: customer id
    :return: None
    """
    msg = f"Deleting the customer {customer_id}"
    LOGGER.debug(msg)
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.delete_instance()
        customer.save()
        msg = f"Customer {customer_id} was deleted successfully"
        LOGGER.info(msg)
    except peewee.DoesNotExist:
        msg = f'Customer {customer_id} is not found in the database'
        LOGGER.error(msg)
        raise peewee.DoesNotExist


def update_customer(customer_id, credit_limit):
    """
    Update the customer credit limit
    :parm customer_id: customer_id
    :parm credit_limit: Decimal value for the money
    :return: None
    """
    msg = f'Updating the credit limit for customer {customer_id}'
    LOGGER.debug(msg)
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
        msg = 'Customer {customer_id} was updated successfully'
        LOGGER.info(msg)
    except peewee.DoesNotExist:
        msg = f'Customer {customer_id} is not found in the database'
        LOGGER.error(msg)
        raise ValueError


def list_active_customer():
    """ Return the number of customers with the active status."""
    LOGGER.debug("Searching the total active users")
    active_members = Customer.select().where(Customer.status).count()
    msg = f'Active Customers = {active_members}'
    LOGGER.info(msg)
    return active_members


if __name__ == "__main__":

    DATABASE.create_tables([Customer])
    # add_customer(1, 'Muhammad', 'Khan',
    #              '9x9 xyzxy Dr. Apt # 529D xxxxxx SC. 29403',
    #              '202-755-3xx1', 'mxmxmx@gmail.com', True, 244.20)
    # add_customer(2, 'Kristina', 'Lawry',
    #              '8x8 xyzxy Dr. Apt # 200D xxxxxx WA. 60089',
    #              '747-900-4950', 'yyyymmm@gmail.com', True, 399)
    # # update_customer(3, 500.00)
    # print(search_customer(2))
    # delete_customer(2)
    # print(search_customer(2))
    # update_customer(3, 500.00)
#     # for data in Customer.select():
#     #     print(data.credit_limit)
