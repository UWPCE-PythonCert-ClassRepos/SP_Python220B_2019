"""Module for database functionality - required functions"""
import logging
from customer_model import DB, Customer


# set up logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("logger initialized")

def add_customer(customer_id, firstname, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    """ This function will add a new customer to the sql database. """
    with DB.transaction():
        LOGGER.info("adding customer: %s %s to the database...", firstname, lastname)
        new_customer = Customer.create(customer_id=customer_id,
                                       firstname=firstname,
                                       lastname=lastname,
                                       home_address=home_address,
                                       phone_number=phone_number,
                                       email_address=email_address,
                                       status=status,
                                       credit_limit=credit_limit)
        new_customer.save()
        LOGGER.info("added customer: %s %s was successfull", firstname, lastname)

    #unreachable code
    #except IntegrityError as error:
    #    raise error
    #    LOGGER.info("unable to add customer %s, %s to database", firstname, lastname)

def search_customer(customer_id):
    """This function will return a dictionary object with firstname,
     lastname, email address and phone number of a customer or an
     empty dictionary object if no customer was found."""

    LOGGER.info('searching for customer_id: %s', customer_id)

    the_customer = Customer.get_or_none(Customer.customer_id == customer_id)

    if the_customer:
        LOGGER.info('building dictionary for: %s', customer_id)
        customer = {}
        customer['firstname'] = the_customer.firstname
        customer['lastname'] = the_customer.lastname
        customer['phone_number'] = the_customer.phone_number
        customer['email_address'] = the_customer.email_address
        LOGGER.info('Customer %s is found', customer_id)
    else:
        customer = {} # return empty dict object for non-existing customer.
        LOGGER.info('Customer %s is not found', customer_id)

    return customer


def delete_customer(customer_id):
    """This function will delete a customer from the sqlite3 database."""
    try:
        with DB.transaction():
            LOGGER.info("deleting customer_id: %s", customer_id)
            info = Customer.get(Customer.customer_id == customer_id)
            info.delete_instance()
            LOGGER.info("customer_id: %s has been deleted", customer_id)
    except IndexError:
        LOGGER.info('customer_id: %s does not exist - nothing has been deleted', customer_id)


def update_customer_credit(customer_id, credit_limit):
    """This function will search an existing customer by customer_id
    and update their credit limit or raise a ValueError exception if
    the customer does not exist."""
    try:
        with DB.transaction():
            customer = Customer.get(Customer.customer_id == customer_id)
            customer.credit_limit = credit_limit
            customer.save()
            LOGGER.info("Datatbase updated successfully")
    except IndexError:
        LOGGER.info("customer_id does not exist")

def list_active_customers():
    """This function will return an integer with the number of customers
    whose status is currently active."""
    active_count = Customer.select().where(Customer.status).count()
    LOGGER.info("Number of active customers retrieved")
    return active_count
