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
from peewee import SqliteDatabase, Model
from peewee import CharField, BooleanField
from peewee import IntegerField, ForeignKeyField
from peewee import IntegrityError


DATABASE_NAME = './customer.db'
DATABASE = SqliteDatabase(DATABASE_NAME)
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger('console')


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
    DATABASE.create_tables([Customer, CustomerStatus])
    DATABASE.close()
    LOGGER.debug("Database is closed: %s", DATABASE.is_closed())


def create_or_get_customer(customer_id, name, last_name,
                           address, phone_number, email):
    """ Function to create or get a customer """
    customer = None

    try:
        if customer_id > 0:
            customer = Customer.get_by_id(customer_id)
        else:
            customer = Customer.get(name=name,
                                    last_name=last_name,
                                    address=address,
                                    phone_number=phone_number,
                                    email=email)

        LOGGER.debug("Retrieved Existing User: %s", customer)
    except IntegrityError:
        customer = Customer.create(name=name,
                                   last_name=last_name,
                                   address=address,
                                   phone_number=phone_number,
                                   email=email)

        LOGGER.debug("Created User: %s", customer)

    return customer


def create_or_get_customer_status(customer_id, status, credit_limit):
    """ Function to create or get the customer status details """
    customer_status = None
    try:
        customer_status = CustomerStatus.get(customer_id=customer_id)
        LOGGER.debug("Retrieved Existing Status: %s", customer_status)
    except IntegrityError:
        customer_status = CustomerStatus.create(customer_id=customer_id,
                                                status=status,
                                                credit_limit=credit_limit)
        LOGGER.debug("Created User Status: %s", customer_status)

    return customer_status


def add_customer(customer_id, name, last_name, address,
                 phone_number, email, status, credit_limit):
    """ Add a customer ot the database """
    customer = create_or_get_customer(customer_id, name, last_name,
                                      address, phone_number, email)
    customer_status = create_or_get_customer_status(customer.id, status,
                                                    credit_limit)

    return {"customer_id": customer.id,
            "customer_status_id": customer_status.id}


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
        status = CustomerStatus.delete().where(CustomerStatus.customer_id ==
                                               customer_id)
        status.execute()
        customer.execute()
        LOGGER.debug("Customer %s deleted", customer_id)
        return True
    except IntegrityError:
        LOGGER.debug("Customer %s deletion failed", customer_id)
        return False


def update_customer_credit(customer_id, credit_limit):
    """ Update a customer's credit limit """
    try:
        current = CustomerStatus.get(CustomerStatus.customer_id == customer_id)
        current.credit_limit = credit_limit
        current.save()
        LOGGER.debug("Updated credit limit to %s for customer %s",
                     credit_limit, customer_id)
        return True
    except IntegrityError as error:
        LOGGER.debug("Invalid customer id provided: %s\n%s",
                     customer_id,
                     error)
        return False


def list_active_customers():
    """ List all the active cusomters in the database """
    return CustomerStatus.select().where(CustomerStatus.status).count()


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
    print(search_customer(ADDED_CUSTOMER['customer_id']))
    print(search_customer(20))
    update_customer_credit(ADDED_CUSTOMER['customer_id'], 2000)
    print("Customers with Active status: %s", list_active_customers())
    delete_customer(ADDED_CUSTOMER['customer_id'])
    print("Customers with Active status: %s", list_active_customers())
