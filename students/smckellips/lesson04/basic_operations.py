# pylint: disable=R0913,W0401,W0614
'''basic operations module.  For access from front_end.'''
import logging
from peewee import *
from customer_model import Customer, DB

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'db.log'
FORMATTER = logging.Formatter(LOG_FORMAT)

FH = logging.FileHandler(LOG_FILE)
CH = logging.StreamHandler()
FH.setFormatter(FORMATTER)
CH.setFormatter(FORMATTER)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(FH)
LOGGER.addHandler(CH)


def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    '''add new customer function.'''
    try:
        with DB.atomic():
            Customer.create(
                customer_id=customer_id,
                name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status,
                credit_limit=credit_limit
            )
        LOGGER.info("Adding customer %s to database.", customer_id)
    except IntegrityError:
        LOGGER.warning("Customer ID %s is already taken.", customer_id)


def search_customer(customer_id):
    '''locate customer by id and return as dictionary.'''
    try:
        result = Customer.select().where(Customer.customer_id == customer_id).dicts().get()
    # except CustomerDoesNotExist as e:
    #     print(e)
    except DoesNotExist:
        result = {}
    return result


def delete_customer(customer_id):
    '''delete a customer by id.'''
    try:
        with DB.atomic():
            delete_query = Customer.delete().where(Customer.customer_id == customer_id)
            delete_query.execute()
            LOGGER.info("Deleting customer %s from database.", customer_id)
    except IntegrityError:
        LOGGER.warning("Customer ID %s not found.", customer_id)


def update_customer_credit(customer_id, credit_limit):
    '''update a customers credit limit by id.'''
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
        LOGGER.info("Updating customer %s credit limit to %s.", customer_id, credit_limit)
    except DoesNotExist:
        raise ValueError


def list_active_customers():
    '''list number of active customers.'''
    return Customer.select().where(Customer.status).count()


def get_customer_list():
    '''Retrieve ordered list of customer'''
    query = Customer.select(Customer.customer_id).order_by(
        Customer.customer_id)
    result = [customer.customer_id for customer in query]
    return result

def id_generator():
    '''
    Create generator to iterate through customer list.
    Option 2 would be to retrieve count of records.  If number of records
    becomes too long, it would be more memory efficient, but more process
    intensive.
    '''
    customers = get_customer_list()
    index = 0
    while index < len(customers):
        yield customers[index]
        # Option to return full customer record for UI display
        # yield search_customer(customers[index])
        index += 1
    return
