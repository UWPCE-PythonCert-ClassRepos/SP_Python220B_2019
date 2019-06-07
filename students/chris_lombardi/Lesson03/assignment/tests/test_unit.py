import sys
sys.path.append('C:\\Users\\chris\\documents\\PY220_Git\\SP_Python220B_2019\\'
                '\\students\\chris_lombardi\\Lesson03\\assignment')

import unittest
import peewee
import logging
import basic_operations
import create_customers
from customer_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class test_basic_operations(unittest.TestCase):

    DATABASE = SqliteDatabase('customers.db')
    DATABASE.connect()
    DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

    CUST_LIST = [('001', 'Abe', 'Lincoln', '1600 Pennsylvania Ave NW',
                  '9999990000', 'abe@whitehouse.com', 'Active', 10000.0),
                  ('002', 'George', 'Washington', '1600 State St',
                   '5601321111', 'george@whitehouse.com', 'Active', 5000.0),
                  ('003', 'Ben', 'Franklin', '20401 Electric Ave',
                   '1234567890', 'ben@elecave.com', 'Inactive', 23400.00)]

    def test_add_customer(self):

        self.clear_database()
        logging.info('Testing add_customer...')
        basic_operations.add_customer(*self.CUST_LIST[0])
        basic_operations.add_customer(*self.CUST_LIST[1])
        basic_operations.add_customer(*self.CUST_LIST[2])

        try:
            test_cust_one = Customer.get(Customer.cust_id == '001')
            test_cust_two = Customer.get(Customer.cust_id == '002')
            test_cust_three = Customer.get(Customer.cust_id == '003')

            self.assertEqual(test_cust_one.cust_firstname, self.CUST_LIST[0][1])
            self.assertEqual(test_cust_one.cust_lastname, self.CUST_LIST[0][2])
            self.assertEqual(test_cust_one.cust_address, self.CUST_LIST[0][3])

        except peewee.IntegrityError as e:
            assert False

    def test_search_customer(self):

        logging.info('Testing search_customer...')
        self.clear_database()
        basic_operations.add_customer(*self.CUST_LIST[0])
        expected_dict = {
                         'name': 'Abe', 'lastname': 'Lincoln',
                         'email address': 'abe@whitehouse.com',
                         'phone number': '9999990000'
                         }
        empty_dict = {}
        for cust in Customer:
            logging.info(f'{cust.cust_id}')

        try:
            test_dict = basic_operations.search_customer('001')
            test_no_entry = basic_operations.search_customer('002')

            self.assertEqual(test_dict, expected_dict)
            self.assertDictEqual(test_no_entry, empty_dict)

        except peewee.DoesNotExist as e:
            assert False

    def test_delete_customer(self):

        logging.info('Testing delete_customer...')
        self.clear_database()
        basic_operations.add_customer(*self.CUST_LIST[0])
        basic_operations.add_customer(*self.CUST_LIST[1])

        try:
            # Check that the customer has been successfully added to the database.
            self.assertEqual(self.CUST_LIST[0][1], Customer.get(Customer.cust_id =='001').cust_firstname)
            basic_operations.delete_customer('001')
            # Check that the customer is no longer in the database.
            # What will a get return if there is no object?
            self.assertEqual(None, basic_operations.delete_customer('001'))
            # Check that the whole database was not deleted.
            self.assertEqual(self.CUST_LIST[1][1], Customer.get(Customer.cust_id =='002').cust_firstname)
        except peewee.DoesNotExist as e:
            assert False

    def test_update_customer_credit(self):

        logging.info('Testing update_customer_credit...')
        self.clear_database()
        basic_operations.add_customer(*self.CUST_LIST[2])
        new_credit = 505050

        try:
            # Confirm that the existing credit limit field exists.
            acust = Customer.get(Customer.cust_id == '003')
            exist_limit = acust.cust_credit_limit
            self.assertEqual(self.CUST_LIST[2][7], exist_limit)
            # Update the credit limit.
            basic_operations.update_customer_credit('003', new_credit)
            # Confirm that the credit limit changed for the customer.
            self.assertEqual(new_credit, Customer.get(Customer.cust_id == '003').cust_credit_limit)

            # Test that a ValueError is raised for a credit limit that isn't available.
            with self.assertRaises(ValueError):
                basic_operations.update_customer_credit('002', new_credit)

        except peewee.DoesNotExist as e:
            assert False

    def test_list_active_customers(self):

        logging.info('Testing list_active_customer...')
        # Clean the database so that it is empty.
        self.clear_database()
        try:
            # Confirm empty database.
            self.assertEqual(basic_operations.list_active_customers(), 0)

            # Add new Customer.
            basic_operations.add_customer(*self.CUST_LIST[0])
            basic_operations.add_customer(*self.CUST_LIST[1])
            basic_operations.add_customer(*self.CUST_LIST[2])
            # Confirm there are two active Customer in database.
            self.assertEqual(basic_operations.list_active_customers(), 2)

        except peewee.DoesNotExist as e:
            assert False

    def clear_database(self):

        logging.info('Clearing database...')
        for cust in self.CUST_LIST:
            try:
                cust_exit = Customer.get(Customer.cust_id == cust[0])
                cust_exit.delete_instance()
            except peewee.DoesNotExist as e:
                logger.info('DNE')
        logger.info('Database Clear!')
