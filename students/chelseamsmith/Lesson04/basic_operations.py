# pylint: disable=W0401, W0614, R0913
"""functions for interacting with customer database"""
from peewee import *
from customer_model import *
import logging

#create log format
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

#set log format
formatter = logging.Formatter(log_format)

#create file handler to send logging to file db.log
file_handler = logging.FileHandler('db.log')
file_handler.setFormatter(formatter)

#get root logger, add file handler to root handler
logger = logging.getLogger()
logger.addHandler(file_handler)

#set level to INFO since it is what will be used for
logger.setLevel(logging.INFO)

def add_customer(cust_id, firstname, lastname, address, phone, email, is_active, credit):
    """adds a new customer to the database"""
    new_customer = Customer.create(customer_id=cust_id,
                                   name=firstname,
                                   last_name=lastname,
                                   home_address=address,
                                   phone_number=phone,
                                   email_address=email,
                                   status=is_active,
                                   credit_limit=credit)
    new_customer.save()
    logging.info("New customer with ID {} created".format(cust_id))

def search_customer(cust_id):
    """searchs for a customer and returns either customer details
       or, if the customer doesn't exist, a blank dictionary"""
    try:
        query = Customer.get(Customer.customer_id == cust_id)
        result = {'name' : query.name, 'last name' : query.last_name,
                  'email address' : query.email_address,
                  'phone number' : query.phone_number}
    except DoesNotExist:
        result = {}
    return result

def delete_customer(cust_id):
    """deletes a customer"""
    try:
        query = Customer.get(Customer.customer_id == cust_id)
        query.delete_instance()
        logging.info("Customer with ID {} deleted.".format(cust_id))
    except DoesNotExist:
        raise ValueError

def update_customer_credit(cust_id, new_credit_limit):
    """updates credit limit of customer"""
    try:
        query = Customer.get(Customer.customer_id == cust_id)
        query.credit_limit = new_credit_limit
        query.save()
        logging.info("Customer {} credit limit changed to {}".format(cust_id, new_credit_limit))
    except DoesNotExist:
        raise ValueError

def list_active_customers():
    """returns the number of customers whose status equals True"""
    number_active_customers = Customer.select().where(Customer.status).count()
    return number_active_customers

if __name__ == "__main__":
    DB.init('customers.db')
    DB.create_tables([Customer])
