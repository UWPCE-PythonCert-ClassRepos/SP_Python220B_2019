""" Basic operations for handling data in the Customers database """

import logging
from peewee import IntegrityError, DoesNotExist
from customer_model import DATABASE, Customer

# pylint: disable=too-many-arguments, logging-fstring-interpolation

logging.basicConfig(level=logging.ERROR)

def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    """ Add a new customer to the database """

    try:
        logging.debug(f"Adding new customer: {name} {lastname}")
        with DATABASE.transaction():
            Customer.create(customer_id=customer_id,
                            name=name,
                            lastname=lastname,
                            home_address=home_address,
                            phone_number=phone_number,
                            email_address=email_address,
                            status=status,
                            credit_limit=credit_limit)
        logging.debug("Customer added successfully")
    except IntegrityError:
        logging.error(f"Error adding customer: {name} {lastname}")
        raise IntegrityError

def search_customer(customer_id):
    """ Find a customer in the database via customer_id """

    try:
        logging.debug(f"Searching database for customer_id:  {customer_id}")
        return Customer.get(Customer.customer_id == customer_id)
    except DoesNotExist:
        logging.error(f"Unable to find customer with id:  {customer_id}")
        raise DoesNotExist

def delete_customer(customer_id):
    """ Delete a customer from the databsse via customer_id """

    try:
        customer_to_delete = Customer.get(Customer.customer_id == customer_id)
        with DATABASE.transaction():
            logging.debug(f"Deleting customer with customer_id:  {customer_id}")
            customer_to_delete.delete_instance()
            customer_to_delete.save()
            logging.debug("Successfully deleted customer")
    except DoesNotExist:
        logging.error(f"Unable to find customer with id:  {customer_id}")
        raise DoesNotExist

def update_customer_credit(customer_id, credit_limit):
    """ Update the credit limit for a customer via customer_id """

    try:
        customer_to_update = Customer.get(Customer.customer_id == customer_id)
        with DATABASE.transaction():
            logging.debug(f"Updating customer with customer_id:  {customer_id}")
            customer_to_update.credit_limit = credit_limit
            customer_to_update.save()
    except DoesNotExist:
        logging.error(f"Unable to find customer with id:  {customer_id}")
        raise DoesNotExist

def list_active_customers():
    """ List all active customers in the database """

    active_members = Customer.select().where(Customer.status == 'active').count()
    return active_members

if __name__ == "__main__":
    # Create database/tables
    DATABASE.create_tables([Customer])
