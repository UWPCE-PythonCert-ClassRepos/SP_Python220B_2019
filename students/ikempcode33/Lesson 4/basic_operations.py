"""Basic op. module for database functionality"""
# pylint: disable=pointless-string-statement,too-many-arguments
#Use comprehensions, iterators/iterables and generators 
import logging
from peewee import *
from customer_model import *

# Add code to log all database data changes , prints to db.log
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler('db.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.info("logger is set up")

def add_customer(customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit):
    """Create a new customer object in database"""
    try:
        with database.transaction():
            logger.info("adding customer: %s, %s to the database...", last_name, first_name)
            new_customer = Customer.create(customer_id=customer_id,
                                           first_name=first_name,
                                           last_name=last_name,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           status=status,
                                           credit_limit=credit_limit)
            new_customer.save()
            logger.info("adding customer: %s was successfull", first_name)

    except TypeError:
        logger.info("unable to add customer %s, %s to database", last_name, first_name)


def add_customers(customers):
    """Adds list of customers to database"""
    logger.info("adding new customers to database")
    new = [add_customer(*customer) for customer in customers]
    logger.info("new customers have been added")
    return new



def search_customer(customer_id):
    """search for customer in the database by their id number"""
    try:
        logger.info('searching for customer id: %s', customer_id)
        customer = Customer.get(Customer.customer_id == customer_id)
        customer_info = {'first_name': customer.first_name,
                         'last_name': customer.last_name,
                         'phone_number': customer.phone_number,
                         'email_address': customer.email_address}
        logger.info(customer_info)
        return customer_info
    except DoesNotExist as ex:
        logger.info(ex)
        logger.info('Customer ID %s does not exist', customer_id)
        return {}


def search_customers(customer_ids):
    """Searches multiple customers in the database"""
    logger.info("searching for customers IDs %s, within database", customer_ids)
    return [search_customer(customer_id) for customer_id in customer_ids]


def delete_customer(customer_id):
    """Deletes a customer from a given ID"""
    try:
        with database.transaction():
            logger.info("deleting customer id: %s....", customer_id)
            info = Customer.get(Customer.customer_id == customer_id)
            info.delete_instance()
            logger.info("customer ID %s has been deleted", customer_id)
    except IndexError:
        logger.info('Customer ID %s does not exist', customer_id)
        raise ValueError


def delete_customers(customer_ids):
    """Delete a list of customers from the database"""
    logger.info("deleting customer IDs %s from database", customer_ids)
    return [delete_customer(customer_id) for customer_id in customer_ids]
    logger.info("customers successfully deleted from database")


def update_customer_credit(customer_id, credit_limit):
    """Update the credit limit of an existing customer"""
    try:
        with database.transaction():
            customer = Customer.get(Customer.customer_id == customer_id)
            customer.credit_limit = credit_limit
            customer.save()
            logger.info("Datatbase updated successfully")
    except IndexError:
        logger.info("customer ID provided does not exist")


def list_active_customers():
    """list all active customers"""
    active_count = Customer.select().where(Customer.status==True).count()
    logger.info("There are %s customers active in the database", active_count)
    return active_count
