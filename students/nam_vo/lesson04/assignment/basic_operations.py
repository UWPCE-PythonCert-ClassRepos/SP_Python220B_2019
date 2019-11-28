""" Implement basic database functionlities """

# pylint: disable=line-too-long, too-many-arguments, logging-format-interpolation, invalid-name, no-value-for-parameter, lost-exception, redefined-outer-name

import logging

from peewee import OperationalError, IntegrityError, DoesNotExist
from customer_model import database, Customer

def setup_logger():
    """ Set up console and database file logging """
    # Create root logging and set logging level to error
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # Create format for logging message and file
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)
    # Create logging console handler, set logging level to error, format and attach it to root
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # console_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.ERROR)
    logger.addHandler(console_handler)
    # Create logging file handler, set logging level to critical, format and attach it to root
    log_file = 'db.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.CRITICAL)
    logger.addHandler(file_handler)

def display_customers():
    """ Display all customer data from database """
    # Display customer data to db.log file
    client_generator = (client for client in Customer.select())
    logging.critical("-" * 100)
    for client in client_generator:
        logging.critical(", ".join(["{}"] * 8).format(client.customer_id, client.name, client.lastname, client.home_address, client.phone_number, client.email_address, client.status, client.credit_limit))
    logging.critical("-" * 100)

def get_customer_generator(customer_id, name, lastname, home_address, phone_number, email_address, status, credit_limit):
    """ Get customer data as a generator """
    yield {'customer_id': customer_id, 'name': name, 'lastname': lastname, 'home_address': home_address, 'phone_number': phone_number, 'email_address': email_address, 'status': status, 'credit_limit': credit_limit}

def add_customer(customer_id, name, lastname, home_address, phone_number, email_address, status, credit_limit):
    """ Add a new customer to the database """
    logging.info("add_customer()")
    # Insert the given customer data into the database
    try:
        with database.atomic():
            Customer.insert_many(get_customer_generator(customer_id, name, lastname, home_address, phone_number, email_address, status, credit_limit)).execute()
    except (OperationalError, IntegrityError) as err_msg:
        logging.error(f"Failed to add customer {customer_id}: {name} {lastname} to the database: {err_msg}")
        raise IntegrityError

def search_customer(customer_id):
    """ Search for a customer in the database using customer_id """
    logging.info("search_customer()")
    result = {}
    try:
        with database.atomic():
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
    with database.atomic():
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
