#! /usr/bin/env python3
"""
The Database Basic Operations Module

    REQUIREMENTS

    store the following data:
        Customer ID.
        Name.
        Lastname.
        Home address.
        Phone number.
        Email address.
        Status (active or inactive customer).
        Credit limit.

        Customer { [id], status, credit_limit}
        Customer_Detail { [id], customer_id, name, last_name,
        address, phone_number, email}

    enable the following functions:
        database creation

        add_customer(customer_id, name, lastname, home_address,
        phone_number, email_address, status, credit_limit): This
        function will add a new customer to the sqlite3 database.

        search_customer(customer_id): This function will return
        a dictionary object with name, lastname, email address and
        phone number of a customer or an empty dictionary object if
        no customer was found.

        delete_customer(customer_id): This function will delete a
        customer from the sqlite3 database.

        update_customer_credit(customer_id, credit_limit): This
        function will search an existing customer by customer_id
        and update their credit limit or raise a ValueError exception
        if the customer does not exist.

        list_active_customers(): This function will return an integer
        with the number of customers whose status is currently active.
"""
import logging
import json
import os
from peewee import SqliteDatabase, Model
from peewee import CharField, BooleanField
from peewee import IntegerField, ForeignKeyField
from peewee import IntegrityError, DatabaseError


DATABASE_NAME = 'customer.db'
DATABASE = SqliteDatabase(DATABASE_NAME)
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger('console')
FH = logging.FileHandler('db.log', 'w+')
FH.setLevel(logging.DEBUG)
FORMATTER = logging.Formatter(FORMAT)
FH.setFormatter(FORMATTER)
LOGGER.addHandler(FH)


class BaseModel(Model):
    """ The BaseModel Database Class """
    class Meta:
        """ The Meta Class """
        database = DATABASE


# the cusomter details table :
# Customer { [id], customer_id, name, last_name,
# address, phone_number, email}
class Customer(BaseModel):
    """ The Customer Database Class """
    name = CharField(max_length=256)
    last_name = CharField(max_length=256)
    address = CharField(max_length=1024, null=True)
    phone_number = CharField(max_length=64, null=True)
    email = CharField(max_length=512, null=True)


# the customer :Customer { [id], customer_id, status,
# credit_limit}
class CustomerStatus(BaseModel):
    """ The CustomerStatus Database Class """
    customer_id = ForeignKeyField(Customer,
                                  to_field=Customer.id,
                                  backref='status',
                                  null=False)
    status = BooleanField(default=False)
    credit_limit = IntegerField(default=0)


def create_database():
    """ Create the database if needed """
    try:
        LOGGER.debug("Create database: %s", DATABASE_NAME)
        DATABASE.create_tables([Customer, CustomerStatus])
        DATABASE.close()
        LOGGER.debug("Database is closed: %s", DATABASE.is_closed())
        return True
    except DatabaseError as exception:
        LOGGER.debug("ERROR: %s", exception)
        return False


def load_customers():
    """ Load the database with data """
    LOGGER.debug("Load data from file: customer.json")
    with open('customer.json') as json_file:
        data = json.load(json_file)
        for customer in data['customers']:  # itertable collection
            add_customer(0, customer['name'], customer['last_name'],
                         customer['address'], customer['phone_number'],
                         customer['email'], customer['active'],
                         customer['credit_limit'])


def create_or_get_customer(customer_id, name, last_name,
                           address, phone_number, email):
    """ Function to create or get a customer """
    customer = None

    try:
        DATABASE.connect(reuse_if_open=True)
        count = Customer.select().where(Customer.name == name,
                                        Customer.last_name == last_name,
                                        Customer.address == address,
                                        Customer.phone_number == phone_number,
                                        Customer.email == email).count()
        if customer_id > 0 and count > 0:
            customer = Customer.get_by_id(customer_id)
        elif count > 0:
            customer = Customer.get(name=name,
                                    last_name=last_name,
                                    address=address,
                                    phone_number=phone_number,
                                    email=email)

            LOGGER.debug("Retrieved Existing User: %s", str(customer))
        else:
            customer = Customer.create(name=name,
                                       last_name=last_name,
                                       address=address,
                                       phone_number=phone_number,
                                       email=email)

            LOGGER.debug("Created User: %s", str(customer))
    finally:
        DATABASE.close()

    return customer


def create_or_get_customer_status(customer_id, status, credit_limit):
    """ Function to create or get the customer status details """
    customer_status = None
    try:
        DATABASE.connect(reuse_if_open=True)
        count = CustomerStatus.select() \
                              .where(
                                  CustomerStatus.customer_id == customer_id) \
                              .count()

        if count > 0:
            customer_status = CustomerStatus.get(customer_id=customer_id)
            LOGGER.debug("Retrieved Existing Status: %s", customer_status)
        else:
            customer_status = CustomerStatus.create(customer_id=customer_id,
                                                    status=status,
                                                    credit_limit=credit_limit)
            LOGGER.debug("Created User Status: %s", customer_status)
    finally:
        DATABASE.close()

    return customer_status


def add_customer(customer_id, name, last_name, address,
                 phone_number, email, status, credit_limit):
    """ Add a customer to the database """
    DATABASE.connect(reuse_if_open=True)
    customer = create_or_get_customer(customer_id, name, last_name,
                                      address, phone_number, email)
    customer_status = create_or_get_customer_status(customer.id, status,
                                                    credit_limit)
    LOGGER.debug("Create Customer: %s", str(customer))
    DATABASE.close()
    return {"customer_id": customer.id,
            "customer_status_id": customer_status.id}


def search_customer(customer_id):
    """ Search for a customer in the database """
    DATABASE.connect(reuse_if_open=True)
    query = Customer.select().where(Customer.id == customer_id).dicts()
    for customer in query:
        LOGGER.debug("Found Customer: %s", str(customer))
        print(customer)

    DATABASE.close()
    return query or None


def search_customer_status(customer_id):
    """ Search the customer status in the database """
    DATABASE.connect(reuse_if_open=True)
    LOGGER.debug("Searching for CustomerStatus for ID: %s", customer_id)
    query = CustomerStatus.select() \
                          .where(
                              CustomerStatus.customer_id == customer_id)  \
                          .dicts()

    return query


def delete_customers():
    """ Delete all customers from the database """
    try:
        DATABASE.connect(reuse_if_open=True)
        for customer in Customer.select():  # iterable
            _customer = Customer.delete().where(Customer.id == customer.id)
            status = CustomerStatus.delete() \
                                   .where(CustomerStatus.customer_id ==
                                          customer.id)
            status.execute()
            _customer.execute()
            LOGGER.debug("Customer %s:%s deleted", customer.id, customer.name)
    except DatabaseError:
        logging.error("Unable to connect to the database")
    finally:
        DATABASE.close()


def delete_customer(customer_id):
    """ Delete a customer from the database """
    try:
        DATABASE.connect(reuse_if_open=True)
        customer = Customer.delete().where(Customer.id == customer_id)
        status = CustomerStatus.delete().where(CustomerStatus.customer_id ==
                                               customer_id)
        status.execute()
        customer.execute()
        LOGGER.debug("Customer %s deleted", customer_id)
        return True
    except IntegrityError:
        LOGGER.debug("Customer %s deletion failed", customer_id)
        return False
    finally:
        DATABASE.close()


def update_customer_credit(customer_id, credit_limit):
    """ Update a customer's credit limit """
    try:
        DATABASE.connect(reuse_if_open=True)
        if CustomerStatus.select() \
                         .where(CustomerStatus.customer_id == customer_id):
            current = CustomerStatus.get(CustomerStatus.customer_id ==
                                         customer_id)
            current.credit_limit = credit_limit
            current.save()
            LOGGER.debug("Updated credit limit to %s for customer %s",
                         credit_limit, customer_id)
            return True

        LOGGER.debug("Invalid customer id provided: %s", customer_id)
        return False
    finally:
        DATABASE.close()


def get_active_customer_count():
    """ List the count of all active cusomters in the database """
    DATABASE.connect(reuse_if_open=True)
    active_count = CustomerStatus.select().where(CustomerStatus.status).count()
    DATABASE.close()
    LOGGER.debug("Active customer count: %s", active_count)
    return active_count


def list_active_customers():
    """ List the customer data for each active customer """
    DATABASE.connect(reuse_if_open=True)
    active_customers = Customer.select(Customer, CustomerStatus.credit_limit) \
                               .join(CustomerStatus,
                                     on=(CustomerStatus.customer_id ==
                                         Customer.id)) \
                               .where(CustomerStatus.status).dicts()

    for customer in active_customers.iterator():  # convert to interator
        LOGGER.debug("Active Customer: %s", str(customer))
        print(customer)


def list_inactive_customers():
    """ List the inactive customers in the databse """
    DATABASE.connect(reuse_if_open=True)
    inactive_customers = Customer.select(Customer,
                                         CustomerStatus.credit_limit) \
                                 .join(CustomerStatus,
                                       on=(CustomerStatus.customer_id ==
                                           Customer.id)) \
                                 .where(CustomerStatus.status == False) \
                                 .dicts()  # noqa: E712

    for customer in inactive_customers.iterator():
        LOGGER.debug("Inactive Customer: %s", str(customer))
        print(customer)


def delete_database():
    """ Remove the database from the filesystem """
    LOGGER.debug("Deleting Database: %s", DATABASE_NAME)
    os.remove(DATABASE_NAME)


if __name__ == '__main__':  # pragma: no cover
    create_database()
    ADDED_CUSTOMER = add_customer(0,
                                  'Joe',
                                  'Nunnelley',
                                  '1234-45th Ave SW Seattle, WA 98116',
                                  '206-218-7999',
                                  'jcnunnelley@gmail.com',
                                  True,
                                  1000)
    LOGGER.debug("\nAdd Customers")
    load_customers()
    LOGGER.debug("\nList Active Customers")
    list_active_customers()
    LOGGER.debug("\nList Inactive Customers")
    list_inactive_customers()
    LOGGER.debug("\nSearch Valid Customer")
    LOGGER.debug(search_customer(ADDED_CUSTOMER['customer_id']))
    LOGGER.debug("\nSearch Invalid Customer")
    LOGGER.debug(search_customer(20))
    LOGGER.debug("\nUpdate Customer")
    update_customer_credit(ADDED_CUSTOMER['customer_id'], 2000)
    LOGGER.debug("\nCustomers with Active status: %s", list_active_customers())
    LOGGER.debug("\nActive Customer Details")
    list_active_customers()
    LOGGER.debug("\nDelete the customer : %s", ADDED_CUSTOMER['customer_id'])
    delete_customer(ADDED_CUSTOMER['customer_id'])
    list_active_customers()
    LOGGER.debug("\nDelete all customers from the database")
    delete_customers()
    list_active_customers()
    LOGGER.debug("\nCustomers with Active status: %s",
                 get_active_customer_count())
    delete_database()
    LOGGER.debug("\nDatabase removed")
