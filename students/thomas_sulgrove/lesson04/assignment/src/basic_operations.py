"""
Defins how you access the DB
"""
import logging
import peewee as pw
from cust_schema import Customer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# pylint: disable=too-many-arguments
def add_customer(customer_id, first_name, last_name, home_address,
                 phone_number, email, status, credit_limit):
    """
    Add a customer to the DB
    :return: NOTHING!
    """
    try:
        new_customer = Customer.create(
            customer_id=customer_id,
            customer_first_name=first_name,
            customer_last_name=last_name,
            customer_home_address=home_address,
            customer_phone_number=phone_number,
            customer_email=email,
            customer_status=status,
            customer_credit_limit=credit_limit)
        new_customer.save()
        LOGGER.info('successfully added: %s', str(first_name + ' ' + last_name))
    except pw.IntegrityError:
        LOGGER.info('id: % already exists', customer_id)

def search_customer(customer_id):
    """
    Return a dict object with first_name, last_name, email address, phone number, or empty if DNE
    :return: a dict with deets seen above here.
    """
    try:
        searched_customer = Customer.get(Customer.customer_id == customer_id)
        return {'Name': searched_customer.customer_first_name,
                'Last Name': searched_customer.customer_last_name,
                'Email': searched_customer.customer_email,
                'Phone Number': searched_customer.customer_phone_number}
    except pw.DoesNotExist:
        LOGGER.warning('%d not found', customer_id)
        return {}

def delete_customer(customer_id):
    """
    Delete a customer from the DB
    :return: Nodda!
    """
    try:
        Customer.get(Customer.customer_id == customer_id).delete_instance()
        LOGGER.info('% successfully deleted', customer_id)
    except:
        LOGGER.info('%d not found', customer_id)
        raise

def update_customer(customer_id, credit_limit):
    """
    search and existing customer by cust_id
    update their credit limit or raise a Value Error if DNE
    :return: ZIP! ZILCH!
    """
    try:
        searched_customer = Customer.get(Customer.customer_id == customer_id)
        searched_customer.customer_credit_limit = credit_limit
        searched_customer.save()
        LOGGER.info('credit limit successfully for id %d', customer_id)

    except pw.DoesNotExist:
        LOGGER.info('credit limit unsuccessful for id %d', customer_id)
        raise

def list_active_customers():
    """
    return and integer with the number of customers whos status is active
    :return: count (int) of active users
    """
    active_count = Customer.select().where(Customer.customer_status).count()
    LOGGER.info('There are % active customers', active_count)
    return active_count
