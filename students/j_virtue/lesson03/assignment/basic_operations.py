# Advanced Programming in Python -- Lesson 3 Assignment 1
# Jason Virtue
# Start Date 2/10/2020

#Supress pylint warnings here
# pylint: disable=unused-wildcard-import

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('customer.db')
logging.info('Create customer database in sqlite3')
database.connect()
logging.info('Connect to customer.db')
database.execute_sql('PRAGMA foreign_keys = ON;')
database.close()

class BaseModel(Model):
    """Class to enable peewee and link it to customer.db"""
    class Meta:
        database = database

class Customer(BaseModel):
    """
        This class defines Customer for HP Norton customers. This will be table for SalesManagers
        persons and accountants to search for them
    """
    customer_id = IntegerField(primary_key = True)
    name = CharField(max_length = 50)
    last_name = CharField(max_length= 50)
    home_address = CharField(max_length= 255)
    phone_number = CharField(max_length= 30)
    email_address = CharField(max_length= 50)
    status = BooleanField()
    credit_limit = DecimalField(max_digits=10, decimal_places=2)
    logging.info('Created schema for customer table')

def create_tables():
    """ Method to create customer table in database"""
    database = SqliteDatabase('customer.db')
    database.connect()
    database.create_tables([Customer])
    logging.info('Create customer table')
    database.close()

def add_customer(customer_id, name, lastname, home_address, phone_number, 
                    email_address, status, credit_limit):
    """Add a customer to the customer table"""
    with database.transaction():
        try:
            new_customer = Customer.create(
                customer_id = customer_id,
                name = name,
                last_name = lastname,
                home_address = home_address,
                phone_number = phone_number,
                email_address = email_address,
                status = status,
                credit_limit = credit_limit)
            new_customer.save()
            logging.info('Added new customer with id %d to customer.db', customer_id)
        except IntegrityError as error:
            logging.info(f'Error inserting %d to customer.db', customer_id)
            logging.info(error)

def add_customers(customers):
    """ Add multiple customers to table"""
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
    """ Search for a customer in the db return name, lastname, email address and phone number"""
    customer_data = {}

    with database.transaction():
        try:
            xcustomer = Customer.get(Customer.customer_id == customer_id)
        except DoesNotExist:
            logging.info('Customer not found')
            return customer_data

        customer_data["name"] = xcustomer.name
        customer_data["last_name"] = xcustomer.last_name
        customer_data["email_address"] = xcustomer.email_address
        customer_data["phone_number"] = xcustomer.phone_number
        customer_data["credit_limit"] = xcustomer.credit_limit

    return customer_data

def delete_customer_table():
    """ Delete all the rows in the Customer table"""
    with database.transaction():
        query = Customer.delete()
        query.execute(database)
    logging.info('Trunctate customer table')

def delete_customer(customer_id):
    """ Delete the customer with customer_id from the database. """
    with database.transaction():
        try:
            xcustomer = Customer.get(Customer.customer_id == customer_id)
        except DoesNotExist as err:  
            raise ValueError(f'{err}: Customer with customer id %d not found.', customer_id)

        return xcustomer.delete_instance()

def update_customer_credit(customer_id, credit_limit):
    """Update credit limit field in customer table"""
    with database.transaction():
        try:
            xcustomer = Customer.get(Customer.customer_id == customer_id)
            xcustomer.credit_limit = credit_limit
            xcustomer.save()
        except DoesNotExist as err:
            # Raise ValueError per the assignment instructions.
            raise ValueError(f'{err}: Customer with customer id %d not found.', customer_id)

def list_active_customers():
    """Query table to get a list of active customers"""
    num_active_customers = 0
    with database.transaction():
        query = Customer.select().where(Customer.status == True)
        num_active_customers = len(query)
    return num_active_customers


if __name__ == "__main__":
    """Initial debug scripts to test out code"""
    create_tables()
    CUSTOMERS = {"cust_01": {"customer_id": 1,
                             "first_name": "Fred",
                             "last_name": "Flintstone",
                             "address": "123 Bedrock Place",
                             "phone": "123.456.7890",
                             "email_address": "fstone@gmail.com",
                             "status": True,
                             "credit_limit": 1000.00},
             "cust_02": {"customer_id": 2,
                             "first_name": "Wilma",
                             "last_name": "Flintstone",
                             "address": "123 Bedrock Place",
                             "phone": "123.456.7890",
                             "email_address": "wstone@gmail.com",
                             "status": True,
                             "credit_limit": 8000.00},
             "cust_03": {"customer_id": 3,
                             "first_name": "Barney",
                             "last_name": "Rubble",
                             "address": "456 Bedrock Lane",
                             "phone": "111.222.3333",
                             "email_address": "troublee@gmail.com",
                             "status": False,
                             "credit_limit": 5000.00}}
    delete_customer_table()
    add_customers(CUSTOMERS)
    print(search_customer(customer_id = 1))
    update_customer_credit(customer_id = 1, credit_limit = 5)
    print(search_customer(customer_id = 1))
    print(list_active_customers())
    delete_customer(customer_id = 1)
    print(search_customer(customer_id = 1))
