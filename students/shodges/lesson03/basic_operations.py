from customer_model import *
import logging

customer_db.create_tables([Customer])

def add_customer(**kwargs):
    with customer_db.transaction():
        try:
            new_customer = Customer.create(**kwargs)
        except:
            return False
        else:
            new_customer.save()
            return True

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
        return True
    except:
        return False

def update_customer_credit(customer_id, credit_limit):
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
        return True
    except Exception as e:
        return False


def list_active_customers():
    return Customer.select().count()


customer_db.close()
