"""This contains functions for basic operation for working with database"""

import logging
from peewee import OperationalError, IntegrityError, DoesNotExist
from codes.customer_model import Customer, DATABASE



logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

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
        LOGGER.info(f'Error occured while adding customer: {customer_id} to database')
        LOGGER.info(myerror)

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
        LOGGER.info("Cannot delete because that customer_id does not exist")

def update_customer_credit(customer_id, credit_limit):
    """This is for updating customer credit limit"""
    try:
        mycustomer = Customer.get(Customer.customer_id == customer_id)
        mycustomer.credit_limit = credit_limit
        mycustomer.save()
        return mycustomer.credit_limit
    except DoesNotExist:
        LOGGER.info("Cannot update because that customer_id does not exist")
        return ValueError

def list_active_customers():
    """This is for listing active customers only"""
    query = Customer.select().where(Customer.customer_status)
    for my_c in query:
        print(my_c.customer_id, my_c.customer_name, my_c.lastname, my_c.customer_status)
    return query.count()


DATABASE.close()
