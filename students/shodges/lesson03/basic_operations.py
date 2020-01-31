from customer_model import *
import logging

customer_db.create_tables([Customer])

def add_customer(**kwargs):
    with customer_db.transaction():
        new_customer = Customer.create(**kwargs)
        new_customer.save()

customer_db.close()
