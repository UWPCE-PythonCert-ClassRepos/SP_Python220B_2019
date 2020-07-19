'''Basic database operations for Rental application'''
import logging
from customer_model import Customer, database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the Customer database if it doesn't exists already
logger.info('One off program to build the classes from the model in the database')
database.create_tables([Customer])


def add_customer(customer_id, customer_name, customer_lastname,
                 customer_home_address, customer_phone_number,
                 customer_email_address, customer_status,
                 customer_credit_limit):
    '''Adds a customer to the database'''
    with database.transaction():
        new_customer = Customer.create(customer_id=customer_id,
                                       name=customer_name,
                                       lastname=customer_lastname,
                                       home_address=customer_home_address,
                                       phone_number=customer_phone_number,
                                       email_address=customer_email_address,
                                       status=customer_status,
                                       credit_limit=customer_credit_limit)
        new_customer.save()
        logger.info('Database add successful')
        return new_customer


def search_customer(customer_id):
    '''Find customer by customer id.  Return None if no matching customer id found.'''
    return Customer.get_or_none(customer_id=customer_id)


def delete_customer(customer_id):
    '''Deletes a customer with the given customer id.  Returns false if no delete happened.'''
    successful_delete = False
    with database.transaction():
        cust = search_customer(customer_id)
        if cust is not None:
            successful_delete = cust.delete_instance() > 0
    return successful_delete


def update_customer_credit(customer_id, new_credit_limit):
    '''Updates the customer's credit limit'''
    cust = None
    with database.transaction():
        cust = search_customer(customer_id)
        if cust is not None:
            cust.credit_limit = new_credit_limit
            cust.save()
    return cust


def list_active_customers():
    '''Retuns the number of active customers'''
    return Customer.select().where(Customer.status).count()


database.close()
