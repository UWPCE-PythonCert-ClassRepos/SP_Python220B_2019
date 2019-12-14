""" Implement basic operations for the database """
import logging

from peewee import IntegrityError, DoesNotExist
from customer_model import database, Customer

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)

def add_customer(customer_id, name, lastname, home_address, phone_number, email_address, status, credit_limit):
    """ Add a new customer to the database """
    logging.info("add_customer()")
    # Convert inputs into a dictionary
    customer_dict = [
        {'customer_id': customer_id, 'name': name, 'lastname': lastname, 'home_address': home_address, 'phone_number': phone_number, 'email_address': email_address, 'status': status, 'credit_limit': credit_limit},
    ]
    # Insert the given customer data into the database
    try:
        with database.atomic():
            Customer.insert_many(customer_dict).execute()
    except IntegrityError as err_msg:
        logging.error(f"Failed to add customer {customer_id}: {name} {lastname} to the database: {err_msg}")
        raise IntegrityError

def search_customer(customer_id):
    """ Search for a customer in the database using customer_id """
    logging.info("search_customer()")
    result = {}
    try:
        with database.transaction():
            person = Customer.get_by_id(customer_id)
            result = {'name': person.name, 'lastname': person.lastname, 'email_address': person.email_address, 'phone_number': person.phone_number}
    except DoesNotExist:
        logging.error(f"Can't find customer data with id = {customer_id} in the database.")
    finally:
        return result

def delete_customer(customer_id):
    """ Delete a customer from the database using customer_id """
    logging.info("delete_customer()")
    # Try to find given customer in the database, just want to see logging error
    search_customer(customer_id)
    # Try to delete whether it is found or not
    with database.transaction():
        Customer.delete_by_id(customer_id)

def update_customer_credit(customer_id, credit_limit):
    """ Update an existing customer's credit limit in the database """
    logging.info("update_customer_credit()")
    try:
        with database.atomic():
            person = Customer.get_by_id(customer_id)
            person.credit_limit = credit_limit
            Customer.bulk_update([person], fields=[Customer.credit_limit])
    except DoesNotExist:
        logging.error(f"Can't find customer data with id = {customer_id} in the database.")
        raise ValueError

def list_active_customers():
    """ Return the total number of customers in the database whose status is currently active """
    logging.info("list_active_customers()")
    with database.atomic():
        active_customers = Customer.filter(status=True)
        return len(active_customers)

if __name__ == "__main__":

    MODELS = [Customer]

    CLIENTS = [
        {'customer_id': 1, 'name': 'Andrew', 'lastname': 'York', 'home_address': "This is Andrew's home address", 'phone_number': '425-111-1111', 'email_address': 'andrew.york@gmail.com', 'status': True, 'credit_limit': 10000},
        {'customer_id': 2, 'name': 'Peter', 'lastname': 'Young', 'home_address': "This is Peter's home address", 'phone_number': '425-222-2222', 'email_address': 'peter.young@gmail.com', 'status': True, 'credit_limit': 5000},
    ]

    # Create Customer table in the database
    database.drop_tables(MODELS)
    database.create_tables(MODELS)
    logging.info(f"database = {database.get_tables()}")

    # All all customers in the CLIENTS dictionary into the database
    for person in CLIENTS:
        add_customer(**person)

    # Search for an existing customer in the database
    a_client = search_customer(1)
    logging.info(f"a_client = {a_client}")

    # Update an existing customer's credit limit in the database
    update_customer_credit(2, 15000)
    logging.info(f"new limit = {Customer.get_by_id(2).credit_limit}")

    # Return the total number of customers in the database whose status is currently active
    active_customers = list_active_customers()
    logging.info(f"There are {active_customers} active customers.")

    # Delete an existing customer in the database
    delete_customer(1)

    # Delete Customer table and close the database
    database.drop_tables(MODELS)
    database.close()
