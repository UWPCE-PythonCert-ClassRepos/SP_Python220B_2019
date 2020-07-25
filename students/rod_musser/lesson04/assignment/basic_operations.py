'''Basic database operations for Rental application'''
import logging
from customer_model import Customer, database, IntegrityError

logger = logging.getLogger()
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)

LOG_FILE = 'db.log'
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
#logger.addHandler(console_handler)

# Create the Customer database if it doesn't exists already
logger.info('One off program to build the classes from the model in the database')
database.create_tables([Customer])


def add_customer(customer_id, customer_name, customer_lastname,
                 customer_home_address, customer_phone_number,
                 customer_email_address, customer_status,
                 customer_credit_limit):
    '''Adds a customer to the database'''
    try:
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
    except IntegrityError as i_e:
        logger.error(i_e)
        logger.info('Customer was not saved.'
                    'A customer with id of %s already exists.', customer_id)
        raise IntegrityError


def search_customer(customer_id):
    '''Find customer by customer id.  Return None if no matching customer id found.'''
    customer = Customer.get_or_none(customer_id=customer_id)
    if customer is None:
        logger.info('Customer with id %s could not be found.', customer_id)
    else:
        logger.info('Customer was %s was found.', customer_id)
    return customer


def delete_customer(customer_id):
    '''Deletes a customer with the given customer id.  Returns false if no delete happened.'''
    successful_delete = False
    with database.transaction():
        cust = search_customer(customer_id)
        if cust is not None:
            successful_delete = cust.delete_instance() > 0
            logger.info('Customer %s was deleted.', customer_id)
        else:
            logger.info('Customer not deleted.'
                        'Customer with id %s could not be found.', customer_id)
    return successful_delete


def update_customer_credit(customer_id, new_credit_limit):
    '''Updates the customer's credit limit'''
    cust = None
    with database.transaction():
        cust = search_customer(customer_id)
        if cust is not None:
            old_credit_limit = cust.credit_limit
            cust.credit_limit = new_credit_limit
            cust.save()
            logger.info('Customer %s credit was updated from %s to %s.',
                        customer_id, old_credit_limit, new_credit_limit)
        else:
            logger.info('Customer credit not updated.'
                        'Customer with id %s could not be found.', customer_id)
    return cust


def list_active_customers():
    '''Retuns the number of active customers'''
    active_count = Customer.select().where(Customer.status).count()
    logger.info('%s active customers.')
    return active_count

def list_all_customers():
    '''This function returns a list of lists of all the customers'''
    cust_pp = 'Cust ID#{:5} {:30} Ph: {:11}, Address: {:30}, Active:{:3}, Limit:{:11}'
    query = Customer.select()
    return [cust_pp.format(x.customer_id, x.name + ' ' + x.lastname, x.phone_number,
                           x.home_address, 'Yes' if x.status == 1 else 'No', x.credit_limit)
            for x in query]


database.close()
