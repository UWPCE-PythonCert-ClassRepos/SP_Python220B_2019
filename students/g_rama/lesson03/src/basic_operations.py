"""basic operations class"""
# pylint: disable=unused-wildcard-import,wildcard-import,too-many-arguments
import logging
import sys
from customer_model import Customer
from peewee import *
import create_customerdb
sys.path.append(r"/Users/guntur/PycharmProjects/uw/p220/"
                r"SP_Python220B_2019/students/g_rama/lesson03/src")

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
    # DB.close()


def search_customer(customer_id):
    """Searching the customer"""
    # DB.connect()
    # DB.execute_sql('PRAGMA foreign_keys = ON;')
    s_customers = (Customer.select().where(Customer.customer_id == customer_id)).execute()
    print(s_customers)

    # for cus in s_customers:
    #     print(f"{cus.name}, {cus.last_name}")


def delete_customer(customer_id):
    """Delete the customer"""
    # db.connect()
    # db.execute_sql('PRAGMA foreign_keys = ON;')
    query = (Customer.delete().where(Customer.customer_id == customer_id)).execute()
    # db.close()


def update_customer_credit(customer_id, limit):
    """Update the customer credit limit"""
    # db.connect()
    # db.execute_sql('PRAGMA foreign_keys = ON;')
    query = (Customer.update(credit_limit=limit).where(Customer.customer_id == customer_id)).execute()
    # db.close()


def list_active_customers():
    """Display the active customers"""
    # db.connect()
    # db.execute_sql('PRAGMA foreign_keys = ON;')
    query = Customer.select().where(Customer.status == 1).count()
    query.execute()
    # db.close()
