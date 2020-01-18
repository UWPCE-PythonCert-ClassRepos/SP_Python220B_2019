"""Test the basic operation modeule. Need to set the sys path to the
directory up where basic_operations.py"""

#pylint: disable=unused-wildcard-import
#pylint: disable=wildcard-import
#pylint: disable=too-many-arguments
#pylint: disable=invalid-name

import unittest
import logging
import sys
import peewee
from customer_model import *
import basic_operations

sys.path.append('/Users/nicholaslenssen/Desktop/Python/Py220/SP_Python220B_2019/'
                'students/Nick_Lenssen/lesson04')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
TEST_DB = SqliteDatabase('test.db')

def clear_database():
    """clears a given database for testing purposes"""
    logging.info('Clearing database...')
    TEST_DB.drop_tables([Customer])
    logging.info('Creating table in database..')
    TEST_DB.create_tables([Customer])

class TestBasicOperation(unittest.TestCase):
    """class to test the add search and delete operations.
    Create example data entries to test functions in module"""

    customer_list = [('1', 'Nick', 'Lenssen', '801 Clay Ave',
                      '6709807722', 'myemail@hotspot.com', 'Active', 5000.07),
                     ('2', 'Alvin', 'Boyd', '1600 State St',
                      '5673459876', 'getaround@hotmail.com', 'Inactive', 15000.0),
                     ('3', 'Ben', 'Franklin', '20401 Electric Ave',
                      '1234567890', 'ben@elecave.com', 'Inactive', 23400.00)]

    def test_add_customer(self):
        """tests the add_customer function"""
        clear_database()
        logging.info('Testing the add_customer function')
        basic_operations.add_customer(*self.customer_list[0])
        basic_operations.add_customer(*self.customer_list[1])
        basic_operations.add_customer(*self.customer_list[2])

        try:
            customer_one_test = Customer.get(Customer.cust_id == '1')
            customer_two_test = Customer.get(Customer.cust_id == '2')
            customer_three_test = Customer.get(Customer.cust_id == '3')

            self.assertEqual(customer_one_test.f_name, self.customer_list[0][1])
            self.assertEqual(customer_two_test.l_name, self.customer_list[1][2])
            self.assertEqual(customer_one_test.cust_phone_num, self.customer_list[0][4])
            self.assertEqual(customer_three_test.cust_status, self.customer_list[2][6])

        except peewee.IntegrityError:
            assert False

    def test_add_existing_customer(self):
        """tests the exception handling in add_customer"""
        clear_database()
        logging.info('Testing the add_customer exception handle')
        basic_operations.add_customer(*self.customer_list[0])
        try:
            #test that an Integrity Error is raised if the same customer is entered
            with self.assertRaises(IntegrityError):
                basic_operations.add_customer(*self.customer_list[0])

        except peewee.IntegrityError:
            assert False

    def test_search_customer(self):
        """will test for the search for the customer_id in the database"""
        clear_database()
        logging.info('Testing the search_database function in basic operations')
        basic_operations.add_customer(*self.customer_list[0])
        logging.info('The entries in the database are...')

        for entry in Customer:
            logging.info(entry)

        expected_dic_1 = {'first name': 'Nick', 'last name': 'Lenssen',
                          'email address': 'myemail@hotspot.com',
                          'phone number': '6709807722'}

        try:
            test_entry = basic_operations.search_customer('1')
            #test_no_entry = basic_operations.search_customer('4')
            self.assertEqual(test_entry, expected_dic_1)
            #self.assertEqual(test_no_entry, {})
        except peewee.IntegrityError:
            assert False

    def test_search_invalid_customer(self):
        clear_database()
        logging.info('Testing the search_database function to raise Integrity Error')
        basic_operations.add_customer(*self.customer_list[0])
        empty_dict = {}
        try:
            self.assertEqual(empty_dict, basic_operations.search_customer('30'))
        except peewee.IntegrityError:
            assert False


    def test_delete_customer(self):
        """tests the function delete_customer that will delete there
        customer with the entered customer id in the database"""
        clear_database()
        logging.info('testing the delete_customer function')
        basic_operations.add_customer(*self.customer_list[0])
        basic_operations.add_customer(*self.customer_list[1])
        try:
            basic_operations.delete_customer('1')
            self.assertEqual(self.customer_list[1][1], Customer.get(Customer.cust_id == '2').f_name)
            try:
                self.assertEqual(self.customer_list[0][1],
                                 Customer.get(Customer.cust_id == '1').f_name)
            except peewee.DoesNotExist:
                logging.info('Customer no longer exists')
                assert True
        except peewee.DoesNotExist:
            assert False

    def test_update_customer_credit(self):
        """tests the function update_customer_credit that will count
                the active customers in the database"""
        logging.info('Testing update_customer_credit...')
        clear_database()
        basic_operations.add_customer(*self.customer_list[2])
        new_credit = 40000

        try:
            # Confirm that the existing credit limit field exists.
            acustomer = Customer.get(Customer.cust_id == '3')
            exist_limit = acustomer.cust_credit_limit
            self.assertEqual(self.customer_list[2][7], exist_limit)
            # Update the credit limit.
            basic_operations.update_customer_credit('3', new_credit)
            # Confirm that the credit limit changed for the customer.
            self.assertEqual(new_credit, Customer.get(Customer.cust_id == '3').cust_credit_limit)

            # Test that a ValueError is raised for a customer that isn't in the database
            with self.assertRaises(ValueError):
                basic_operations.update_customer_credit('2', new_credit)

        except peewee.DoesNotExist:
            assert False

    def test_list_active_customers(self):
        """tests the function list_active_customers that will count
        the active customers in the database"""
        logging.info('Testing list_active_customer...')
        # Clean the database so that it is empty.
        clear_database()
        try:
            # Confirm empty database.
            self.assertEqual(basic_operations.list_active_customers(), 0)

            # Add new Customer.
            basic_operations.add_customer(*self.customer_list[0])
            basic_operations.add_customer(*self.customer_list[1])
            basic_operations.add_customer(*self.customer_list[2])
            # Confirm there is one active Customer in database.
            self.assertEqual(basic_operations.list_active_customers(), 1)

        except peewee.DoesNotExist:
            assert False
