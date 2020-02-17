'''basic operations module.  For access from front_end.'''
import logging
from peewee import *
from customer_model import Customer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def add_customer(customer_id, name, lastname, home_address, phone_number, email_address, status, credit_limit):
    pass

def search_customer(customer_id):
    pass

def delete_customer(customer_id):
    pass

def update_customer_credit(customer_id, credit_limit):
    pass

def list_active_customers():
    pass