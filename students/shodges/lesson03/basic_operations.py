from customer_model import *
import logging

customer_db.create_tables([Customer])

def add_customer(**kwargs):
    with customer_db.transaction():
        new_customer = Customer.create(**kwargs)
        new_customer.save()

def search_customer(customer_id):
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        return customer
    except IndexError:
        raise ValueError

def delete_customer(customer_id):
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.delete_instance()
    except IndexError:
        raise ValueError

def update_customer_credit(customer_id, credit_limit):
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
    except IndexError:
        raise ValueError


def list_active_customers():
    return 0


customer_db.close()
