"""
Store customer data from HP Norton in a relational database (sqlite3).
"""
from peewee import *
import logging

database = SqliteDatabase('customer.db')
database.connect()
database.execute_sql('Pragma foreign_keys = ON;')

class BaseModel(Model):
    """ Set up database """
    class Meta:
        database = database

class Customer(BaseModel):
    """
        This class defines a customer, which maintains the details of
        a customer's information.
    """

    customer_id = IntegerField(primary_key = True)
    first_name = CharField()
    last_name = CharField()
    home_address = CharField()
    phone_number = IntegerField()
    email_address = CharField()
    status = BooleanField()
    credit_limit = DecimalField()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_customer(customer_id, first_name, last_name, home_address, phone_number,
                 email_address, status, credit_limit):
    """ Create a new customer profile """
    try:
        with database.transaction():
            new_customer = Customer.create(customer_id = customer_id, first_name = first_name,
                                           last_name = last_name, home_address = home_address,
                                           phone_number = phone_number, email_address = email_address,
                                           status = status, credit_limit = credit_limit)
            new_customer.save()
            logger.info(f'Database add successful {first_name} {last_name}')

    except Exception as e:
        logger.info(f'Error creating - customer id {customer_id}')
        logger.info(e)

    database.close()

def search_customer(search_id):
    """ Search for an existing customer """
    try:
        with database.transaction():
            a_customer = Customer.get(Customer.customer_id == search_id)
            a_customer_dict = {search_id: [a_customer.first_name, a_customer.last_name,
                                           a_customer.phone_number, a_customer.email_address]}
        return a_customer_dict
    except Exception as e:
        logger.info(f'Error searching - {search_id}, customer not found')
        logger.info(e)
        raise ValueError

    database.close()


def delete_customer(search_id):
    """ Delete an existing customer """
    try:
        with database.transaction():
            a_customer = Customer.get(Customer.customer_id == search_id)
            a_customer.delete_instance()

    except Exception as e:
        logger.info(f'Delete failed: {search_id}, customer not found')
        logger.info(e)
        raise ValueError

def update_customer_credit(search_id, updated_limit):
    """" Update an existing customer's credit limit"""
    try:
        with database.transaction():
            a_customer = Customer.get(Customer.customer_id == search_id)
            a_customer.credit_limit = updated_limit
            a_customer.save()
            logger.info('Credit limit update succesful')

    except Exception as e:
        logger.info(f'Update failed: {search_id}, {updated_limit}')
        logger.info(e)
        raise ValueError

    database.close()

def list_active_customers():
    """ List number of current active customers """
    active_customer_count = 0
    query = (Customer.select(Customer))
    for customer in query:
        logger.info(f'{customer.first_name} {customer.last_name} has status {customer.status}')
        if customer.status == True:
            active_customer_count = active_customer_count + 1
    return active_customer_count