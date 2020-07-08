"""
    functions:
        add_customer()
        search_customer()
        delete_customer()
        update_customer_credit()
        list_active_customer()
"""
# pylint: disable=too-many-arguments
# pylint: disable=broad-except

import logging
from .customer_model import Customer, db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    """
    This function will add a new customer to the sqlite3 database
    """
    try:
        with db.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                customer_name=name,
                customer_lastname=lastname,
                customer_address=home_address,
                customer_phone_number=phone_number,
                customer_email=email_address,
                credit_limit=credit_limit,
                status=status
            )
            new_customer.save()
            logger.info('Customer successfully added.')

    except Exception as err:
        logger.info('Error creating %s', name)
        logger.info(err)

def search_customer(customer_id):
    """
    This function will search for a customer using the id field
    then it will return a dictionary object.
    """
    db_customer = Customer.get(Customer.customer_id == customer_id)
    dict_customer = {
        'customer_id': db_customer.customer_id,
        'name': db_customer.customer_name,
        'lastname': db_customer.customer_lastname,
        'home_address': db_customer.customer_home_address,
        'phone_number': db_customer.customer_phone_number,
        'email_address': db_customer.customer_email_address,
        'credit_limit': db_customer.credit_limit,
        'status': db_customer.status
    }
    return dict_customer

def delete_customer(customer_id):
    """
    This function will delete a customer uisng the id field
    """
    nrows = Customer.delete().where(Customer.customer_id == customer_id).execute()
    logger.info('%d row(s) deleted.', nrows)

def update_customer_credit(customer_id, credit_limit):
    """
    This function will update a customer's credit limit using the id field.
    """
    db_customer = Customer.get(Customer.customer_id == customer_id)

    if db_customer is not None:
        (Customer
         .update({Customer.credit_limit: credit_limit})
         .where(Customer.customer_id == customer_id)
         .execute())
    else:
        logging.error('Customer ID: %s does not exist.', customer_id)
        raise ValueError()

def list_active_customers():
    """ This function will list the number of active customers """
    db_count = (Customer.select().where(Customer.status)).count()
    return db_count
