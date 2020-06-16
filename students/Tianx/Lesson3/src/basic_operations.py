import logging
from peewee import *
from customer_model import Customer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SqliteDatabase('customers.db')
db.create_tables([Customer])

# pylint: disable = W0614, W0401, C0301, C0114, W1203


def add_customer(customer_id, first_name, last_name, home_address, phone_number,
                 email_address, active_status, credit_limit):
    """
    This function will add a new customer to the sqlite3 database.
    """
    try:
        db.connect()
        db.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info('Try to create a new customer record')
        with db.transaction():
            new_customer = Customer.create(customer_id=customer_id,
                                           first_name=first_name,
                                           last_name=last_name,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           active_status=active_status,
                                           credit_limit=credit_limit)
            new_customer.save()
            logger.info(f'Adding new customer:{customer_id} to the database.')
    except Exception as e:
        logger.info(f'Error creating = {customer_id}')
        logger.info(e)
    finally:
        logger.info('database closes')
        db.close()


def search_customer(customer_id):
    """
    This function will return a dictionary object with name, lastname, email address and phone number of a customer
    or an empty dictionary object if no customer was found.
    """
    try:
        db.connect()
        db.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info('Try to search a customer record')
        with db.transaction():
            customer = Customer.get(Customer.customer_id == customer_id)
            logger.info(f'{customer_id} found.')
        return {'first_name': customer.first_name, 'last_name': customer.last_name,
                'email': customer.email_address, 'phone_number': customer.phone_number}
    except DoesNotExist:
        logger.warning(f'Customer {customer_id} does not exit')
        customer = dict()
        return customer  # Empty dictionary if no customer was found
    finally:
        logger.info('database closes')
        db.close()


def delete_customer(customer_id):
    """
    This function will delete a customer from the sqlite3 database.
    """
    try:
        db.connect()
        db.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info('Try to search a customer record')
        with db.transaction():
            customer = Customer.get(Customer.customer_id == customer_id)
            customer.delete_instance()
            logger.info(f'{customer_id} found and deleted.')
    except DoesNotExist:
        logger.info(f'{customer_id} does not exist.')
    finally:
        logger.info('database closes')
        db.close()


def update_customer_credit(customer_id, credit_limit):
    """
    This function will search an existing customer by customer_id and update their credit limit or
    raise a ValueError exception if the customer does not exist.
    """
    try:
        db.connect()
        db.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info('Try to search a customer record')
        with db.transaction():
            customer = Customer.get(Customer.customer_id == customer_id)
            customer.credit_limit = credit_limit
            customer.save()
            logger.info(f'{customer_id} now has a ${credit_limit} credit limit.')
    except DoesNotExist:
        logger.info(f'{customer_id} does not exist.')
        raise DoesNotExist
    finally:
        logger.info('database closes')
        db.close()


def list_active_customers():
    """
    This function will return an integer with the number of customers whose status is currently active
    """
    active_customers = Customer.select().where(Customer.active_status).count()
    logger.info(f'We have {active_customers} active customers.')
    return active_customers
