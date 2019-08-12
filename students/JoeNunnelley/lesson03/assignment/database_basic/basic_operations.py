#! /usr/bin/env python3

import logging
from peewee import *

"""
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
        Customer_Detail { [id], customer_id, name, last_name, address, phone_number, email}

    enable the following functions:
        database creation

        add_customer(customer_id, name, lastname, home_address, phone_number, email_address,
        status, credit_limit): This function will add a new customer to the sqlite3 database.

        search_customer(customer_id): This function will return a dictionary object with name,
        lastname, email address and phone number of a customer or an empty dictionary object if
        no customer was found.

        delete_customer(customer_id): This function will delete a customer from the sqlite3
        database.

        update_customer_credit(customer_id, credit_limit): This function will search an existing
        customer by customer_id and update their credit limit or raise a ValueError exception if
        the customer does not exist.

        list_active_customers(): This function will return an integer with the number of customers
        whose status is currently active.
"""
DATABASE = './customer.db'

database = SqliteDatabase(DATABASE)
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('console')

class BaseModel(Model):
    class Meta:
        database = database


# the cusomter details table :
# Customer { [id], customer_id, name, last_name, address, phone_number, email}
class Customer(BaseModel):
    name = CharField(max_length=256)
    last_name = CharField(max_length=256)
    address = CharField(max_length=1024, null=True)
    phone_number = CharField(max_length=64, null=True)
    email = CharField(max_length=512, null=True)


# the customer :Customer { [id], customer_id, status, credit_limit}
class CustomerStatus(BaseModel):
    customer_id = ForeignKeyField(Customer, to_field=Customer.id, backref='status', null=False)
    status = BooleanField(default=False)
    credit_limit = IntegerField(default=0)


def create_database():
    """ Create the database if needed """
    database.create_tables([Customer, CustomerStatus])
    database.close()
    logger.debug("Database is closed: {}".format(database.is_closed()))


def create_or_get_customer(name, last_name, address, phone_number, email):
    customer = None

    try:
        customer = Customer.get(name=name,
                                last_name=last_name,
                                address=address,
                                phone_number=phone_number,
                                email=email)
        logger.debug("Retrieved Existing User: {}".format(customer))
    except:
        customer = Customer.create(name=name,
                                   last_name=last_name,
                                   address=address,
                                   phone_number=phone_number,
                                   email=email)
        logger.debug("Created User: {}".format(customer))

    return customer


def create_or_get_customer_status(customer_id, status, credit_limit):
    customer_status = None
    try:
        customer_status = CustomerStatus.get(customer_id=customer_id)
        logger.debug("Retrieved Existing Status: {}".format(customer_status))
    except:
        customer_status = CustomerStatus.create(customer_id=customer_id,
                                                status=status,
                                                credit_limit=credit_limit)
        logger.debug("Created User Status: {}".format(customer_status))

    return customer_status


def add_customer(customer_id, name, last_name, address,
                 phone_number, email, status, credit_limit):
    """ Add a customer ot the database """
    customer=create_or_get_customer(name, last_name, address, phone_number, email)
    customer_status=create_or_get_customer_status(customer.id, status, credit_limit)

    return { "customer_id": customer.id, "customer_status_id": customer_status.id}


def search_customer(customer_id):
    """ Search for a customer in the database """
    query = Customer.select().where(Customer.id == customer_id).dicts()
    for customer in query:
        print(customer)

    return query or None


def delete_customer(customer_id):
    """ Delete a customer from the database """
    try:
        customer = Customer.delete().where(Customer.id == customer_id)
        customer_status = CustomerStatus.delete().where(CustomerStatus.customer_id == customer_id)
        customer_status.execute()
        customer.execute()
        logger.debug("Customer {} deleted".format(customer_id))
        return True
    except:
        logger.debug("Customer {} deletion failed".format(customer_id))
        return False


def update_customer_credit(customer_id, credit_limit):
    """ Update a customer's credit limit """
    try:
        current = CustomerStatus.get(CustomerStatus.customer_id == customer_id)
        current.credit_limit = credit_limit
        current.save()
        logger.debug("Updated credit limit to {} for customer {}".format(credit_limit, customer_id))
        return True
    except Exception as error:
        logger.debug("Invalid customer id provided: {}\n{}".format(customer_id, error))
        return False


def list_active_customers():
    """ List all the active cusomters in the database """
    return CustomerStatus.select().where(CustomerStatus.status).count()


create_database()
added_customer = add_customer(0, 'Joe', 'Nunnelley', '1234-45th Ave SW Seattle, WA 98116', '206-218-7999', 'jcnunnelley@gmail.com', True, 1000)
print(search_customer(added_customer['customer_id']))
print(search_customer(20))
update_customer_credit(added_customer['customer_id'], 2000)
print("Customers with Active status: {}".format(list_active_customers()))
delete_customer(added_customer['customer_id'])
print("Customers with Active status: {}".format(list_active_customers()))