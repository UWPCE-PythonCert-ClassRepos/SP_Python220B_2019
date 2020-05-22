'''Basic Operations Module for customer database'''

# Advanced Programming in Python -- Lesson 4 Assignment 1
# Jason Virtue
# Start Date 2/17/2020

#Supress pylint warnings here
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name,too-few-public-methods,wrong-import-order,singleton-comparison,too-many-arguments,logging-format-interpolation

from peewee import *
import logging

# Set up log file
logging.basicConfig(filename="db.log", format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M %p', level=logging.INFO)


DATABASE = SqliteDatabase('customer.db')
logging.info('Create customer database in sqlite3')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
DATABASE.close()

class BaseModel(Model):
    """Class to enable peewee and link it to customer.db"""
    class Meta:
        """Database meta file for peewee"""
        database = DATABASE

class Customer(BaseModel):
    """
        This class defines Customer for HP Norton customers. This will be table for SalesManagers
        persons and accountants to search for them
    """
    customer_id = IntegerField(primary_key=True)
    name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    home_address = CharField(max_length=255)
    phone_number = CharField(max_length=30)
    email_address = CharField(max_length=50)
    status = BooleanField()
    credit_limit = DecimalField(max_digits=10, decimal_places=2)
    logging.info('Created schema for customer table')

def create_tables():
    """ Method to create customer table in database"""
    DATABASE.close()
    DATABASE.connect()
    DATABASE.create_tables([Customer])
    logging.info('Create customer table')
    DATABASE.close()

def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    """Add a customer to the customer table"""
    with DATABASE.transaction():
        try:
            new_customer = Customer.create(
                customer_id=customer_id,
                name=name,
                last_name=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status,
                credit_limit=credit_limit)
            new_customer.save()
            logging.info(f'Added new customer with name {name} {lastname} to customer.db')
        except IntegrityError as error:
            logging.info(error)
            logging.info(f'Primary key constraint. Key {customer_id} is a duplicate')

def add_customers(customers):
    """ Add multiple customers to table"""
    #Comprehension
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

    with DATABASE.transaction():
        try:
            xcustomer = Customer.get(Customer.customer_id == customer_id)
        except DoesNotExist:
            return customer_data

        customer_data["name"] = xcustomer.name
        customer_data["last_name"] = xcustomer.last_name
        customer_data["email_address"] = xcustomer.email_address
        customer_data["phone_number"] = xcustomer.phone_number

    return customer_data

def delete_customer_table():
    """ Delete all the rows in the Customer table"""
    with DATABASE.transaction():
        query = Customer.delete()
        query.execute(DATABASE)
    logging.info('Trunctate customer table')

def delete_customer(customer_id):
    """ Delete the customer with customer_id from the database. """
    with DATABASE.transaction():
        try:
            xcustomer = Customer.get(Customer.customer_id == customer_id)
            logging.info(f'Delete customer with id {customer_id} in customer table')
        except DoesNotExist as err:
            raise ValueError(f'{err}: Customer with customer id {customer_id} not found')

        return xcustomer.delete_instance()

def update_customer_credit(customer_id, credit_limit):
    """Update credit limit field in customer table"""
    with DATABASE.transaction():
        try:
            xcustomer = Customer.get(Customer.customer_id == customer_id)
            xcustomer.credit_limit = credit_limit
            xcustomer.save()
            logging.info(f'Update credit limit to {credit_limit} for' +\
                f' customer with id {customer_id}')
        except DoesNotExist as err:
            raise ValueError(f'{err}: Customer with customer id {customer_id} not found')

def list_active_customers():
    """Query table to get a list of active customers"""
    #Setup comprehension to count active customers
    num_active_customers = 0
    with DATABASE.transaction():
        #query = Customer.select().where(Customer.status == True) --OLD CODE
        for customer in Customer.select():
            if customer.status is True:
                num_active_customers += 1
        #num_active_customers = len(query) --OLD CODE
        logging.info(f'Number of active customers is {num_active_customers}')
    return num_active_customers

def display_customer_table():
    """Function to display rows in customer table"""
    ##Using Comprehension; New statement
    customer_rows = Customer.select()
    customer_names = [customer.name + " " + customer.last_name for customer in customer_rows]
    logging.info(f"Remaining customers in table {customer_names}")
    return customer_names
