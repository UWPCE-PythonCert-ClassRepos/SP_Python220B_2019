from customer_model import *
import logging

customer_db.create_tables([Customer])

def add_customer(**kwargs):
    with customer_db.transaction():
        new_customer = Customer.create(**kwargs)
        new_customer.save()

def search_customer(customer_id):
    customer = Customer.get(Customer.customer_id == customer_id)
    return customer

def delete_customer(customer_id):
    customer = Customer.get(Customer.customer_id == customer_id)
    customer.delete_instance()


customer_db.close()
