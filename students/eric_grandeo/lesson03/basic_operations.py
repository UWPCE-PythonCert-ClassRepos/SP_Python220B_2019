'''
Basic opertions

'''

from customers_model import *
from peewee import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('customers.db')

def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    pass

def search_customer(customer_id):
    pass

def delete_customer(customer_id):
    pass

def update_customer_credit(customer_id, credit_limit):
    pass

def list_active_customers():
    pass

if __name__ == "__main__":
    database.create_tables([Customers])
    



