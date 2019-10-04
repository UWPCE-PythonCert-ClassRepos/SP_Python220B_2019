'''
basic operations for database
'''

import logging
from peewee import *
from customer_db_model import Customer

def add_customer(customer_id, name, last_name, home_address, phone_number,
                 email_address, status, credit_limit):
    pass

def search_customer(customer_id):
    pass

def delete_customer(customer_id):
    pass

def update_customer_credit(customer_id, credit_limit):
    pass

def list_active_customers():
    pass
