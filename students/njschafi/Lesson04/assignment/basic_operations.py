"""
Program to manipulate customer database.
"""
import logging
import peewee
from customer_model import Customer
# pylint: disable=W1203, C0103, R0913, W0703, C0121
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler('db.log')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    """This function will add a new customer to the sqlite3 database."""
    logger.info('Adding a new customer')
    try:
        new_customer = Customer.create(
            customer_id=customer_id,
            customer_name=name,
            customer_last_name=lastname,
            customer_address=home_address,
            customer_phone=phone_number,
            customer_email=email_address,
            customer_status=status,
            customer_limit=credit_limit)
        new_customer.save()
        logger.info('Database add successful')
        logger.info(f'Customer: {name} '
                    f'{lastname} saved as'
                    f' {customer_id}')
    except peewee.IntegrityError:
        logger.error(f'{customer_id} already exists in database')
        raise ValueError('Customer already exists in the database') from None
    except Exception as e:
        logger.error(f'Error creating = {customer_id} - check all inputs.')
        logger.debug(e)

def search_customer(customer_id):
    """
    This function will return a dictionary object with name, lastname,
    email address and phone number of a customer or an empty dictionary
    object if no customer was found.
    """
    logger.info(f'Searching for a customer with customer id: {customer_id}')
    try:
        acustomer = Customer.get(Customer.customer_id == customer_id)
        logger.info(f'{acustomer.customer_id} found!')
        return {'name': acustomer.customer_name,
                'lastname': acustomer.customer_last_name,
                'email': acustomer.customer_email,
                'phone_number': acustomer.customer_phone}
    except Exception as e:
        logger.debug(e)
        logger.warning(f'{customer_id} not found in database. '
                       'Empty dict to be returned')
        return {}

def delete_customer(customer_id):
    """This function will delete a customer from the sqlite3 database."""
    logger.info('Deleting a customer')
    try:
        acustomer = Customer.get(Customer.customer_id == customer_id)
        logger.info(f'Trying to delete {acustomer.customer_name}'
                    f' {acustomer.customer_last_name}')
        acustomer.delete_instance()
        logger.info(f'{customer_id} successfully deleted from database')
    except Exception as e:
        logger.error(f'{customer_id} not deleted!'
                     ' Customer ID not found in database')
        logger.debug(e)

def update_customer_credit(customer_id, credit_limit):
    """
    This function will search an existing customer by customer_id
    and update their credit limit or raise a ValueError exception if the
    customer does not exist.
    """
    logger.info('Updating customer credit limit')
    try:
        logger.info('Checking if inputted credit limit is float type')
        float(credit_limit)
        logger.debug(f'{credit_limit} is type float')
    except Exception as e:
        logger.debug(e)
        logger.error(f'{credit_limit} not float type')
        raise TypeError(f'{credit_limit} NOT valid!') from None

    try:
        acustomer = Customer.get(Customer.customer_id == customer_id)
        logger.info(f'{customer_id} found in database!')
        acustomer.customer_limit = credit_limit
        acustomer.save()
    except (IndexError, Exception) as e:
        logger.error(f'Customer id {customer_id} not found in database')
        raise ValueError(f'{customer_id} NOT found in database!') from None


def list_active_customers():
    """
    This function will return an integer with the number of
    customers whose status is currently active.
    """
    logger.info('Listing active customers')
    query = Customer.select().where(Customer.customer_status == True).count()
    logger.info(f'{query} customers are active')
    return query


def display_customers():
    """
    Displays all customers (by first and last name) in the database as a list
    """
    query = Customer.select()
    logger.info('Now listing all customers in database')
    m = [(p.customer_name + ' ' + p.customer_last_name) for p in query]
    return m
