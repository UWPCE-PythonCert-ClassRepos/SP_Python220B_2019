"""
basic_operations.py
Joli Umetsu
PY220
"""
import logging
from peewee import IntegrityError, DoesNotExist
from customer_model import DB, Customer

# logger setup
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    """
        Adds a new customer to the database
        returns:
    """
    logging.info("attempting to add customer: %s %s...", name, lastname)
    try:
        with DB.transaction():
            # add new customer entry
            new_customer = Customer.create(customer_id=customer_id,
                                           name=name,
                                           lastname=lastname,
                                           home_address=home_address,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           status=status,
                                           credit_limit=credit_limit)

            # save new customer entry in database
            new_customer.save()
            LOGGER.info("successfully saved new customer %s %s!", name, lastname)

    except IntegrityError:
        LOGGER.error("IntegrityError occurred while creating customer %s %s!", name, lastname)


def search_customer(customer_id):
    """
        Searches customer by ID
        returns: dict; with name, lastname, email, phone
                 (or)
                 empty if no customer found
    """
    logging.info("searching customer ID %s...", customer_id)
    try:
        with DB.transaction():
            # query database for customer by ID
            searched_customer = Customer.get(Customer.customer_id == customer_id)
            logging.info("successfully found customer!")
            # return dict with name, lastname, email, phone number
            return {"name": searched_customer.name, "lastname": searched_customer.lastname,
                    "email_address": searched_customer.email_address,
                    "phone_number": searched_customer.phone_number}

    except DoesNotExist:
        LOGGER.error("DoesNotExisterror: customer ID %s not found!", customer_id)
        # return empty dict
        return {}


def delete_customer(customer_id):
    """
        Deletes a customer from the database
        returns:
    """
    logging.info("attempting to delete customer ID %s...", customer_id)
    try:
        with DB.transaction():
            # query database for customer by ID
            to_delete = Customer.get(Customer.customer_id == customer_id)
            # delete the customer found
            to_delete.delete_instance()
            logging.info("successfully deleted customer!")

    except DoesNotExist:
        LOGGER.error("DoesNotExisterror: customer ID %s delete failed!", customer_id)


def update_customer_credit(customer_id, credit_limit):
    """
        Searches customer by ID and updates credit limit
        returns:
    """
    logging.info("attempting to update customer ID %s with limit: %s...", customer_id, credit_limit)
    try:
        with DB.transaction():
            # query database for customer by ID
            update_customer = Customer.get(Customer.customer_id == customer_id)
            # update credit limit
            update_customer.credit_limit = credit_limit
            update_customer.save()
            logging.info("successfully updated credit limit!")
    except DoesNotExist:
        LOGGER.error("error: customer ID %s update failed!", customer_id)
        # if customer does not exist, raise ValueError
        raise ValueError

def list_active_customers():
    """
        Gets customers whose status is currently active
        returns: int; number of active customers
    """
    logging.info("getting active customers...")
    return Customer.select().where(Customer.status).count()
