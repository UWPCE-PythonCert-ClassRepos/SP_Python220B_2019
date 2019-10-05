'''
basic operations for database
'''

import logging
from peewee import *
from customer_db_model import Customer

def add_customer(customer_id, name, last_name, home_address, phone_number,
                 email_address, status, credit_limit):
    new_customer = Customer.create(
        customer_id=customer_id,
        name=name,
        last_name=last_name,
        home_address=home_address,
        phone_number=phone_number,
        email_address=email_address,
        status=status,
        credit_limit=credit_limit
    )
    new_customer.save()

def search_customer(customer_id):
    search_dict = {}
    search = Customer.get(Customer.customer_id == customer_id)
    search_dict['name'] = search.name
    search_dict['last_name'] = search.last_name
    search_dict['email_address'] = search.email_address
    search_dict['phone_number'] = search.phone_number
    return search_dict

def delete_customer(customer_id):
    pass

def update_customer_credit(customer_id, credit_limit):
    update_limit = Customer.get(Customer.customer_id == customer_id)
    update_limit.credit_limit = credit_limit
    update_limit.save()

def list_active_customers():
    pass
