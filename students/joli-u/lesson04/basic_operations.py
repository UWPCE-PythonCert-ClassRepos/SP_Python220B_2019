"""
basic_operations.py
Assignment 4
Joli Umetsu
PY220
"""
import logging
from peewee import IntegrityError, DoesNotExist
from customer_model import DB, Customer

# log formatting setup
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

# log file handler setup
LOG_FILE = 'db.log'
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.INFO)

# log console handler setup
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(logging.INFO)

# logger setup
LOGGER = logging.getLogger()

# add handlers
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


def add_customer(customer_id, name, lastname, home_address, phone_number, email_address,
                 status, credit_limit):
    """
        Adds a new customer to the database
        returns: new customer (object)
    """
    logging.info("(attempting to add customer: %s %s...)", name, lastname)
    try:
        with DB.transaction():
            new_customer = Customer.create(customer_id=customer_id,
                                           name=name,
                                           lastname=lastname,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           status=status,
                                           credit_limit=credit_limit)

            new_customer.save()
            logging.debug("Added %s %s to the database!", name, lastname)
            return new_customer

    except IntegrityError:
        logging.error("Error: customer %s %s not added due to missing information", name, lastname)


def add_customers(customers):
    """
        Adds multiple new customers to the database
        returns: list of new customers
    """
    return [add_customer(*customer) for customer in customers]


def search_customer(customer_id):
    """
        Searches customer by ID
        returns: dict; with name, lastname, email, phone
                 (or)
                 empty if no customer found
    """
    logging.info("(searching customer ID %s...)", customer_id)
    try:
        with DB.transaction():
            searched_customer = Customer.get(Customer.customer_id == customer_id)
            logging.debug("Searched and found customer ID %s!", customer_id)

            return {"name": searched_customer.name, "lastname": searched_customer.lastname,
                    "email_address": searched_customer.email_address,
                    "phone_number": searched_customer.phone_number}

    except DoesNotExist:
        logging.error("Error: customer ID#%s does not exist", customer_id)
        return {}


def search_customers(customer_ids):
    """
        Searches multiple customers by ID
        returns: dict; with names, lastnames, emails, phones
                 (or)
                 empty if no customer found
    """
    return [search_customer(customer_id) for customer_id in customer_ids]


def delete_customer(customer_id):
    """
        Deletes a customer from the database
        returns:
    """
    logging.info("(attempting to delete customer ID %s...)", customer_id)
    try:
        with DB.transaction():
            to_delete = Customer.get(Customer.customer_id == customer_id)
            to_delete.delete_instance()
            logging.debug("Deleted customer ID %s!", customer_id)
            return to_delete

    except DoesNotExist:
        logging.error("Error: customer ID#%s does not exist", customer_id)


def delete_customers(customer_ids):
    """
        Deletes multiple customers from the database
        returns:
    """
    return [delete_customer(customer_id) for customer_id in customer_ids]


def update_customer_credit(customer_id, credit_limit):
    """
        Searches customer by ID and updates credit limit
        returns:
    """
    logging.info("(attempting to update customer ID %s with limit: %s...)", customer_id,
                 credit_limit)
    try:
        with DB.transaction():
            update_customer = Customer.get(Customer.customer_id == customer_id)
            update_customer.credit_limit = credit_limit
            update_customer.save()
            logging.debug("Updated credit limit for customer ID %s!", customer_id)
            return update_customer

    except DoesNotExist:
        logging.error("Error: customer ID#%s does not exist", customer_id)
        raise ValueError


def list_active_customers():
    """
        Gets customers whose status is currently active
        returns: int; number of active customers
    """
    logging.info("(getting active customers...)")
    return Customer.select().where(Customer.status).count()
