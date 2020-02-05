# pylint: disable=wildcard-import, unused-wildcard-import
# pylint: disable=too-few-public-methods
"""This model is used to perform basic database operations for sqlite3 database."""

import logging
from customer_model import *

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.INFO)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(CONSOLE_HANDLER)


def setup_database():
    """This function will create a new sqlite3 database."""
    try:
        with database:
            LOGGER.info('Attempting to create database')
            database.create_tables([
                Customer,
                CustomerContact
            ])
        LOGGER.info('Database created successfully.')
    except Exception as create_error:
        LOGGER.error(str(create_error))


def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    """This function will add a new customer to the sqlite3 database."""
    try:
        LOGGER.info('Attempt add Customer %s %s %s %s %s %s %s %s ', customer_id, name,
                    lastname, home_address, phone_number, email_address, status, credit_limit)
        with database.transaction():
            new_customer = Customer.create(
                customerid=customer_id,
                name=name,
                lastname=lastname,
                status=status,
                creditlimit=credit_limit
            )
            new_customer.save()
            LOGGER.info('New customer added to Customer table')
            new_contact = CustomerContact.create(
                homeaddress=home_address,
                phonenumber=phone_number,
                emailaddress=email_address,
                contactid=customer_id
            )
            new_contact.save()
            LOGGER.info('New customer data added to CustomerContact table')
    except Exception as addcusterror:
        LOGGER.error(str(addcusterror))
        LOGGER.info('Error Creating Customer record %s', name)


def search_customer(customer_id):
    """
    Search_customer(customer_id): This function will return
    :param customer_id:
    :return: a dictionary object with name, lastname, email address and phone number
     of a customer or an empty dictionary object
    if no customer was found.
    """
    query_customer = {}
    try:
        with database.transaction():
            query_customer = (Customer.select(Customer.name, Customer.lastname, CustomerContact.emailaddress,
                                              CustomerContact.phonenumber).join(CustomerContact).where(
                                                  Customer.customerid == customer_id).dicts()[0])
            return query_customer
    except Exception as custerror:
        LOGGER.error(str(custerror))
        raise custerror
    finally:
        return query_customer


def delete_customer(customer_id):
    """This function will delete a customer from the sqlite3 database."""
    try:
        with database.transaction():
            logging.info('ATTEMPTING TO DELETE CUSTOMER: %s and dependent objects from '
                         'customer and customercontact tables', customer_id)
            del_customer = Customer.get(Customer.customerid == customer_id)
            del_customer.delete_instance(recursive=True)
            logging.info('Customer: %s deleted', customer_id)
            return del_customer
    except (NameError, IndexError, KeyError):
        LOGGER.info('Delete failed for customer %s', customer_id)
        raise Exception
    #finally:
     #   return 0


def update_customer_credit(customer_id, credit_limit):
    """
    This function will search an existing customer by customer_id and update their
    credit limit or raise a ValueError exception if the customer does not exist.
    """
    try:
        with database.transaction():
            logging.info('Attempting to update customer %s credit limit to %s',
                         customer_id, credit_limit)
            update_customer = (Customer
                               .update(creditlimit=credit_limit)
                               .where(Customer.customerid == customer_id))
            rowsupdated = update_customer.execute()
            if rowsupdated == 0:
                raise ValueError('Customer %s was not found in database', customer_id)
            logging.info('%s -Records updated ', rowsupdated)
    except ValueError as customervalueerror:
        LOGGER.error(str(customervalueerror))
        raise customervalueerror


def list_active_customers():
    """
    This function will return an integer with the number of
    customers whose status is currently active.
    """
    try:
        with database.transaction():
            query_customer_status = (Customer
                                     .select(fn.count(Customer.customerid).alias('count'))
                                     .where(Customer.status == 0)
                                     .scalar())
            logging.info('Active customer count is %s', query_customer_status)
            return query_customer_status
    except Exception as customererror:
        LOGGER.error(str(customererror))
        raise customererror

def main():
    """ Main function for basic operations. """
    setup_database()


if __name__ == "__main__":
    main()