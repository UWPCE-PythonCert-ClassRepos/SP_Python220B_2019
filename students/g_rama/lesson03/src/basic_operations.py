import logging
import sqlite3
import peewee
import sys
sys.path.append(r"/Users/guntur/PycharmProjects/uw/p220/SP_Python220B_2019/students/g_rama/lesson03/src")
import create_customerdb
from customer_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    """Adding the new customer"""
    customer = Customer.create(
        customer_id=customer_id,
        name=name,
        last_name=lastname,
        home_address=home_address,
        phone_number=phone_number,
        email_address=email_address,
        status=status,
        credit_limit=credit_limit
    )
    customer.save()


def search_customer(customer_id):
    """Searching the customer"""
    query = Customer.select().where(Customer.customer_id == customer_id)
    if query:
        print(query)


def delete_customer(customer_id):
    """Delete the customer"""
    query = Customer.delete().where(Customer.customer_id == customer_id)
    query.execute()


def update_customer_credit(customer_id, credit_limit):
    """Update the customer credit limit"""
    query = Customer.update(credit_limit = credit_limit).where(Customer.customer_id == customer_id)
    query.execute()


def list_active_customers():
    """Display the active customers"""
    query = Customer.select().where(status=1).count()
    query.execute()


