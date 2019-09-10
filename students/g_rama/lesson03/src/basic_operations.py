"""basic operations class"""
import logging
import sys
from peewee import IntegrityError
from customer_model import Customer
from create_customerdb import *
sys.path.append(r"/Users/guntur/PycharmProjects/uw/p220/"
                r"SP_Python220B_2019/students/g_rama/lesson03/src")
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


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
    try:
        customer.save()
    except IntegrityError:
        print("Duplicate primary keys no allowed")


def search_customer(customer_id):
    """Searching the customer"""
    # DB.connect()
    # DB.execute_sql('PRAGMA foreign_keys = ON;')
    logging.info(f"Searching for customer {customer_id}")
    s_customers = (Customer.select().where(Customer.customer_id == customer_id)).execute()
    #return s_customers.name
    for cus in s_customers:
        return cus.name
    #return s_customers


def delete_customer(customer_id):
    """Delete the customer"""
    # db.connect()
    # db.execute_sql('PRAGMA foreign_keys = ON;')
    logging.info(f"Deleting the customer {customer_id}")
    query = Customer.delete().where(Customer.customer_id == customer_id)
    query.execute()
    # db.close()


def update_customer_credit(customer_id, limit):
    """Update the customer credit limit"""
    # db.connect()
    # db.execute_sql('PRAGMA foreign_keys = ON;')
    logging.info(f"Updating the customer {customer_id} credit limt to {limit}")
    query = Customer.update(credit_limit=limit).where(Customer.customer_id == customer_id)
    query.execute()
    # db.close()


def list_active_customers():
    """Display the active customers"""
    # db.connect()
    # db.execute_sql('PRAGMA foreign_keys = ON;')
    count = Customer.select().where(Customer.status == "1").count()
    logging.info(f"Total number of active customers are {count}")
    print(count)
    return count
    # db.close()
