"""This contains functions for basic operation for working with database"""

import logging
from peewee import OperationalError, IntegrityError, DoesNotExist
from codes.customer_model import Customer, DATABASE



LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'DB.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)

LOGGER.info('Working with Customer class')

def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    """this is for adding customer"""
    try:
        with DATABASE.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                customer_name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                customer_status=status,
                credit_limit=credit_limit)
            new_customer.save()
            LOGGER.info('New customer added to the database')
    except (OperationalError, IntegrityError, DoesNotExist) as myerror:
        LOGGER.error(f'Error occured while adding customer: {customer_id} to database')
        LOGGER.error(myerror)

def search_customer(customer_id):
    """this is for searching customer"""
    try:
        mycustomer = Customer.get(Customer.customer_id == customer_id)
        return {'firstname': mycustomer.customer_name, 'lastname':mycustomer.lastname,
                'email':mycustomer.email_address, 'phone': mycustomer.phone_number}
    except DoesNotExist:
        return {}

def delete_customer(customer_id):
    """this is for deleting a customer from the database"""
    try:
        mycustomer = Customer.get(Customer.customer_id == customer_id)
        LOGGER.info(f'deleting customer {customer_id}')
        mycustomer.delete_instance()
    except DoesNotExist:
        LOGGER.error("Cannot delete because that customer_id does not exist")

def update_customer_credit(customer_id, credit_limit):
    """This is for updating customer credit limit"""
    try:
        mycustomer = Customer.get(Customer.customer_id == customer_id)
        mycustomer.credit_limit = credit_limit
        mycustomer.save()
        return mycustomer.credit_limit
    except DoesNotExist:
        LOGGER.error("Cannot update because that customer_id does not exist")
        return ValueError

def list_active_customers():
    """This is for listing active customers only"""
    query = Customer.select().where(Customer.customer_status)
    for my_c in query:
        print(my_c.customer_id, my_c.customer_name, my_c.lastname, my_c.customer_status)
    return query.count()


DATABASE.close()
