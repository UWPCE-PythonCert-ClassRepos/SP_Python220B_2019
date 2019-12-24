""" Contains all the code for the lesson04 assignment.

This code refactors the lesson03 code to:
    1. use comprehensions, iterators / iterables, and generators appropriately and
    2. log all db changes to a file called db.log
"""

# pylint: disable=unused-wildcard-import


import logging
from peewee import *  # pylint: disable=wildcard-import

FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file=None, level=logging.INFO):
    """Since I want to have one general logger output to a stream and another one for database
    events log to a file I need multiple loggers. This code is based on an answer at
    https://stackoverflow.com/questions/11232230/logging-to-two-files-with-different-settings ."""

    if log_file:
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(FORMATTER)

    alogger = logging.getLogger(name)
    alogger.setLevel(level)
    alogger.addHandler(handler)

    return alogger

G_LOGGER = setup_logger(name="general_logger", level=logging.ERROR)
# G_LOGGER.setLevel(logging.ERROR)

DB_LOGGER = setup_logger(name="database_logger", log_file="db.log")

DATABASE = SqliteDatabase('customer.db')  # the DATABASE global is referenced throughout the code
DATABASE.connect(reuse_if_open=True)
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
G_LOGGER.info("db created")

class BaseModel(Model):
    """ This class in the base class for Customer and enables using peewee.
    """
    class Meta:  # pylint: disable=too-few-public-methods,missing-docstring
        database = DATABASE


class Customer(BaseModel):
    """ This class defines Customer, which maintains details of HP Norton's customers.
    """
    customer_id = IntegerField(primary_key=True)  # Note there was no specification for this field.
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=255)
    phone_number = CharField(max_length=30)
    email_address = CharField(max_length=50)
    status = BooleanField()
    credit_limit = DecimalField(max_digits=9, decimal_places=2)  # Likely totally unrealistic
                                                                 # to have a credit limit
                                                                 # greater than $999,999,999.99 :)


def create_tables():
    """ Add the Customer model as a table in the database.
    """
    DATABASE.connect(reuse_if_open=True)
    DATABASE.create_tables([Customer])
    G_LOGGER.info('created tables')
    DB_LOGGER.info('created tables')
    DATABASE.close()


def delete_customer_table():
    """ Delete all the rows in the table associated with the Customer model. (Used for testing.)
    """
    with DATABASE.transaction():
        query = Customer.delete()
        query.execute(DATABASE)
        DB_LOGGER.info("deleted customer table data")


def add_customer(customer_id, name, lastname, home_address,  # pylint: disable=too-many-arguments
                 phone_number, email_address, status, credit_limit):
    """ Add data for a single customer to the DATABASE.

    Note: I am leaving the keyword arguments with the same names as in the
    assignment description.

    Note: I keep getting a peewee IntegrityError about a non-unique customer_id so I am catching
    the exception and just logging it only. The final tested version should show no errors in the
    log output.
    """
    with DATABASE.transaction():
        try:
            new_customer = Customer.create(
                customer_id=customer_id,
                first_name=name,
                last_name=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status,
                credit_limit=credit_limit)
            new_customer.save()
            G_LOGGER.info("added customer %d", customer_id)
            DB_LOGGER.info("added customer %d, %s %s", customer_id, name, lastname)
        except IntegrityError as err:
            G_LOGGER.error(err)
            G_LOGGER.error("add_customer: customer_id %d not unique", customer_id)
            DB_LOGGER.error(err)
            DB_LOGGER.error("add_customer: customer_id %d not unique", customer_id)


def add_customers(customers):
    """ Add data for multiple customers to the database.
    """
    for customer in customers.values():
        add_customer(customer["customer_id"],
                     customer["first_name"],
                     customer["last_name"],
                     customer["address"],
                     customer["phone"],
                     customer["email_address"],
                     customer["status"],
                     customer["credit_limit"])


def search_customer(customer_id):
    """ Search for a customer in the db and return a dictionary object with name, lastname, email
    address and phone number of a customer or an empty dictionary object if no customer was found.
    """
    customer_data = {}

    with DATABASE.transaction():
        try:
            acustomer = Customer.get(Customer.customer_id == customer_id)
        except DoesNotExist:
            return customer_data  # empty dictionary

        customer_data["name"] = acustomer.first_name
        customer_data["last_name"] = acustomer.last_name
        customer_data["email_address"] = acustomer.email_address
        customer_data["phone_number"] = acustomer.phone_number

    return customer_data


def delete_customer(customer_id):
    """ Delete the customer with customer_id from the database. If the customer does not exist
    in the database raise a ValueError exception.
    """
    with DATABASE.transaction():
        try:
            acustomer = Customer.get(Customer.customer_id == customer_id)
        except DoesNotExist as err:  # Note that I would prefer to raise a DoesNotExist exception
                                     # but the instructions for update_customer_credit says to
                                     # raise a ValueError if the customer is not found. For
                                     # consistency ValueError will be raised instead.
            G_LOGGER.error('%s: Customer with customer id %d not found.', err, customer_id)
            raise ValueError(f'{err}: Customer with customer id {customer_id} not found.')

        DB_LOGGER.info("deleted customer %d, %s %s",
                       acustomer.customer_id,
                       acustomer.first_name,
                       acustomer.last_name)

        return acustomer.delete_instance()


def update_customer_credit(customer_id, credit_limit):
    """ Search an existing customer by customer_id and update their credit limit or raise a
    ValueError exception if the customer does not exist.
    """
    with DATABASE.transaction():
        try:
            acustomer = Customer.get(Customer.customer_id == customer_id)
            acustomer.credit_limit = credit_limit
            acustomer.save()
            DB_LOGGER.info("updated credit for customer %d, %s %s, to $%.2f",
                           acustomer.customer_id,
                           acustomer.first_name,
                           acustomer.last_name,
                           acustomer.credit_limit)
            return credit_limit
        except DoesNotExist as err:
            # Raise ValueError per the assignment instructions.
            raise ValueError(f'{err}: Customer with customer id {customer_id} not found.')


def update_multiple_customers_credit(customer_credit_data):
    """ Update the credit limit for multiple customers. customer_credit_data is a tuple of tuples
    ((customer_id1, credit_limit1), (customer_id2, credit_limit2), ...). Return a generator
    comprehension of tuples (customer_id1, result1), (customer_id2, result2), ... showing the
    customer_id's and the result of trying to update their credit. The result is the new
    credit_limit if the update is successful, False if not.

    Note: 1. This is here to show a generator comprehension for the lesson04 assignment.
          2. This circumvents handling the ValueError (DoesNotExist) exception that is raised by
             update_customer_credit when it is given a customer_id for a customer not in the db
             by first checking that the customer_id's passed to it are actualy in the database
             and only passing the valid customer id's to update_customer_credit.
    """
    return ((id, update_customer_credit(id, credit)) if get_customer_from_id(id)
            else (id, False)
            for id, credit in customer_credit_data)


def list_active_customers():
    """ Return an integer with the number of customers whose status is currently active.
    """
    num_active_customers = 0

    with DATABASE.transaction():
        query = Customer.select().where(Customer.status == True)  # pylint: disable=E1111,C0121
        num_active_customers = len(query)

    return num_active_customers


def get_customer_from_id(customer_id):
    """ Return a customer if it exists in the database, if not return False.

    Note: This does not raise an exception when a customer record isn't found in the db, rather it
    returns False.
    """
    with DATABASE.transaction():
        try:
            return Customer.get(Customer.customer_id == customer_id)
        except DoesNotExist:
            return False
