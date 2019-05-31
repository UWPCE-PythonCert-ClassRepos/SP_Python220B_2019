"""basic operations class"""
# pylint: disable=unused-wildcard-import,wildcard-import,too-many-arguments,wrong-import-position
import logging
import sys
import datetime
sys.path.append(r"/Users/guntur/PycharmProjects/uw/p220/"
                r"SP_Python220B_2019/students/g_rama/lesson04/src")
from customer_model import *
from create_customerdb import *
# log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '_DB.log'
# formatter = logging.Formatter(log_format)
# logging.basicConfig(level=logging.INFO)
# LOGGER = logging.getLogger(__name__)
# file_handler = logging.FileHandler(log_file)
# file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.INFO)
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
log_file = datetime.datetime.now().strftime('%Y-%m-%d') + '_charges_calc.log'
formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(file_handler)


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
        logger.info("Added the customers")
    except IntegrityError:
        print("Duplicate primary keys no allowed")


def search_customer(customer_id):
    """Searching the customer"""
    # DB.connect()
    # DB.execute_sql('PRAGMA foreign_keys = ON;')
    logger.info(f"Searching for customer {customer_id}")
    s_customers = (Customer.select().where(Customer.customer_id == customer_id)).execute()
    #return s_customers.name
    for cus in s_customers:
        return cus.name
    #return s_customers


def delete_customer(customer_id):
    """Delete the customer"""
    # db.connect()
    # db.execute_sql('PRAGMA foreign_keys = ON;')
    logger.info(f"Deleting the customer {customer_id}")
    query = Customer.delete().where(Customer.customer_id == customer_id)
    query.execute()
    # db.close()


def update_customer_credit(customer_id, limit):
    """Update the customer credit limit"""
    # db.connect()
    # db.execute_sql('PRAGMA foreign_keys = ON;')
    logger.info(f"Updating the customer {customer_id} credit limt to {limit}")
    query = Customer.update(credit_limit=limit).where(Customer.customer_id == customer_id)
    query.execute()
    # db.close()


def list_active_customers():
    """Display the active customers"""
    # db.connect()
    # db.execute_sql('PRAGMA foreign_keys = ON;')
    active_customers = [customer.customer_id for customer in Customer.select().where(Customer.status == "1")]
    print(active_customers)
    logger.info(f"Total number of active customers are {len(active_customers)}")
    return len(active_customers)
    # db.close()


def display_all_customer_names():
    """Function to display the customers using comprehensions"""
    all_customers = Customer.select()
    customer_names = [customer.name + " " + customer.last_name for customer in all_customers]
    print(customer_names)
