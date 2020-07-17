# Stella Kim
# Assignment 4: Iterables, Iterators & Generators

"""Create customer database with Peewee ORM, SQLite and Python"""


import logging
from peewee import IntegrityError, DoesNotExist
from customer_model import CUSTOMER_DB, Customer

# Format logs
LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'

# Setup logging format
FORMATTER = logging.Formatter(LOG_FORMAT)

# Setup file handler
FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setFormatter(FORMATTER)

# Setup console handler
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.info('Logger has initiated.')

CUSTOMER_DB.create_tables([Customer])
LOGGER.info('Customer table created.')


def add_customer(customer_id, first_name, last_name, home_address,
                 phone, email, status, credit_limit):
    """Create a new customer.  Raises error if ID in use."""
    try:
        with CUSTOMER_DB.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                first_name=first_name,
                last_name=last_name,
                home_address=home_address,
                phone=phone,
                email=email,
                status=status,
                credit_limit=credit_limit
            )
        new_customer.save()
        LOGGER.debug('New customer %s %s (ID: %s) has been added to DB',
                     first_name, last_name, customer_id)

    except IntegrityError as error:
        LOGGER.error('Failure: ID %s already in use.', customer_id)
        LOGGER.info(error)
        raise ValueError


def search_customer(customer_id):
    """Search for a customer in the database by ID."""
    try:
        search = Customer.get(Customer.customer_id == customer_id)
        LOGGER.debug('Searching for customer %s...', customer_id)
        return {'First Name': search.first_name,
                'Last Name': search.last_name,
                'Email Address': search.email,
                'Phone Number': search.phone}

    except DoesNotExist:
        LOGGER.error('Customer %s does not exist.', customer_id)
        return {}


def search_all_customers():
    """List all customers in the database."""
    all_customers = Customer.select().where(Customer.customer_id)
    LOGGER.debug('Listing all customers in database.')
    return [{'First Name': customer.first_name,
             'Last Name': customer.last_name,
             'Email Address': customer.email,
             'Phone Number': customer.phone}
            for customer in all_customers]


def delete_customer(customer_id):
    """Delete a customer from the database by ID."""
    try:
        search = Customer.get(Customer.customer_id == customer_id)
        LOGGER.debug('Searching for customer %s...', customer_id)
        search.delete_instance()
        LOGGER.debug('Customer %s has been deleted from database.',
                     customer_id)
        return search

    except DoesNotExist:
        LOGGER.error('Customer %s does not exist.', customer_id)
        return None


def update_customer_credit(customer_id, credit_limit):
    """Update a customer's credit limit by ID."""
    try:
        search = Customer.get(Customer.customer_id == customer_id)
        LOGGER.debug('Searching for customer %s...', customer_id)
        with CUSTOMER_DB.transaction():
            search.credit_limit = credit_limit
            search.save()
        LOGGER.debug('Credit limit for %s has been updated.', customer_id)
        return search.credit_limit

    except DoesNotExist:
        LOGGER.error('Customer %s does not exist.', customer_id)
        return None


def list_active_count():
    """Display a count of active customers in the database."""
    active_customers = Customer.select().where(Customer.status).count()
    LOGGER.debug('Number of customers whose status is currently active: %s.',
                 active_customers)
    return active_customers


def list_active_customers():
    """Display a list of active customers in the database."""
    active_customers = Customer.select().where(Customer.status).order_by(
        Customer.last_name)
    LOGGER.debug('List of customers whose status is currently active: %s.',
                 active_customers)
    return [customer.last_name + ', ' + customer.first_name for customer
            in active_customers]


def list_generator():
    """
    Create generator to iterate through active customers list in
    case user would like to print by line.
    """
    active_customers = list_active_customers()
    index = 0
    while index < len(active_customers):
        yield active_customers[index]
        index += 1
