""" Run unit tests """
import logging

from unittest import TestCase

from peewee import *
from customer_model import Customer
from basic_operations import add_customer, search_customer, delete_customer, update_customer_credit, list_active_customers

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)

MODELS = [Customer]

CLIENTS = [
    {'customer_id': 1, 'name': 'Andrew', 'lastname': 'York', 'home_address': "This is Andrew's home address", 'phone_number': '425-111-1111', 'email_address': 'andrew.york@gmail.com', 'status': True, 'credit_limit': 10000},
    {'customer_id': 2, 'name': 'Peter', 'lastname': 'Young', 'home_address': "This is Peter's home address", 'phone_number': '425-222-2222', 'email_address': 'peter.young@gmail.com', 'status': True, 'credit_limit': 5000},
]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')
test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
test_db.connect()

def set_up():
    """ Set up database connection for Customer model """
    logging.info("set_up()")
    test_db.drop_tables(MODELS)
    test_db.create_tables(MODELS)

def tear_down():
    """ Delete all tables and close database """
    logging.info("tear_down()")
    test_db.drop_tables(MODELS)
    test_db.close()

class BasicOperationsTest(TestCase):
    """ Test basic operations on the Customer database """

    def test_add_customer(self):
        """ Test add_customer() """
        logging.info("test_add_customer()")
        # Initial database set up
        set_up()
        # Populate customers data into the database
        for person in CLIENTS:
            add_customer(**person)
            logging.info(Customer.get_by_id(person['customer_id']).phone_number)
            self.assertEqual(person['phone_number'], Customer.get_by_id(person['customer_id']).phone_number)
        # Remove data and exit database
        tear_down()

    def test_add_customer_invalid_phone(self):
        """ Test add_customer() with an invalid phone number """
        CLIENTS_INVALID_PHONE = [
            {'customer_id': 1, 'name': 'Andrew', 'lastname': 'York', 'home_address': "This is Andrew's home address", 'phone_number': '425-111-1111-dummy', 'email_address': 'andrew.york@gmail.com', 'status': True, 'credit_limit': 10000},
            {'customer_id': 2, 'name': 'Peter', 'lastname': 'Young', 'home_address': "This is Peter's home address", 'phone_number': '425-222-2222-extra', 'email_address': 'peter.young@gmail.com', 'status': False, 'credit_limit': 5000},
        ]
        logging.info("test_add_customer_invalid_phone()")
        # Initial database set up
        set_up()
        # Populate customers data into the database
        for person in CLIENTS_INVALID_PHONE:
            with self.assertRaises(IntegrityError):
                add_customer(**person)
                logging.info(Customer.get_by_id(person['customer_id']).phone_number)
        # Remove data and exit database
        tear_down()

    def test_search_customer(self):
        """ Test search_customer() """
        logging.info("test_search_customer()")
        expected_result = {'name': 'Andrew', 'lastname': 'York', 'email_address': 'andrew.york@gmail.com', 'phone_number': '425-111-1111'}
        # Initial database set up
        set_up()
        # Populate customers data into the database
        for person in CLIENTS:
            add_customer(**person)
        self.assertDictEqual(expected_result, search_customer(1))
        # Remove data and exit database
        tear_down()

    def test_search_customer_not_found(self):
        """ Test search_customer() with a non-existent customer id """
        logging.info("test_search_customer_not_found()")
        # Initial database set up
        set_up()
        # Populate customers data into the database
        for person in CLIENTS:
            add_customer(**person)
        self.assertDictEqual({}, search_customer(-1))
        # Remove data and exit database
        tear_down()

    def test_delete_customer(self):
        """ Test delete_customer() """
        logging.info("test_delete_customer()")
        # Initial database set up
        set_up()
        # Populate customers data into the database
        for person in CLIENTS:
            add_customer(**person)
        # Delete customer with id = 1
        delete_customer(1)
        self.assertDictEqual({}, search_customer(1))
        # Remove data and exit database
        tear_down()

    def test_update_customer_credit(self):
        """ Test update_customer_credit() """
        logging.info("test_update_customer_credit()")
        # Initial database set up
        set_up()
        # Populate customers data into the database
        for person in CLIENTS:
            add_customer(**person)
        # Update credit limit of customer id = 2
        update_customer_credit(2, 15000)
        self.assertEqual(15000, Customer.get_by_id(2).credit_limit)
        # Remove data and exit database
        tear_down()

    def test_update_customer_credit_not_found(self):
        """ Test update_customer_credit() with a non-existent customer id """
        logging.info("test_update_customer_credit_not_found()")
        # Initial database set up
        set_up()
        # Populate customers data into the database
        for person in CLIENTS:
            add_customer(**person)
        # Update credit limit of customer id = 0
        with self.assertRaises(ValueError):
            update_customer_credit(0, 15000)
        # Remove data and exit database
        tear_down()

    def test_list_active_customers(self):
        """ Test list_active_customers() """
        logging.info("test_list_active_customers()")
        # Initial database set up
        set_up()
        # Populate customers data into the database
        for person in CLIENTS:
            add_customer(**person)
        # Get the number of customers whose status is currently active
        self.assertEqual(2, list_active_customers())
        # Remove data and exit database
        tear_down()
