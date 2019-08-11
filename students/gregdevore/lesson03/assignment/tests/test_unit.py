'''
Unit tests for basic_operations module (Customer database API)
'''

import sys
# Add path to files
sys.path.append('/Users/gdevore21/Documents/Certificate Programs/Python/PYTHON220/ \
SP_Python220B_2019/students/gregdevore/lesson03/assignment')

from unittest import TestCase
from peewee import DoesNotExist
from customer_model import database, Customer
import basic_operations

class CustomerTests(TestCase):
    '''
    Test suite for unit testing the basic_operations module

    Methods:
        setUpClass(cls):
            Class method, run before any tests, clears Customer database,
            creates new customer

        clear_database():
            Static method, resets database before tests are run

        add_customer_to_database(self):
            Method called by multiple tests, adds customer if not in database

        test_customer_add(self):
            Test method to add customer to database

        test_search_customer(self):
            Test method to search for customer

        test_search_fake_customer(self):
            Tests case where customer being searched does not exist

        test_delete_customer(self):
            Tests method to delete customer from database

        test_delete_fake_customer(self):
            Tests case where customer being deleted does not exist

        test_update_customer_credit(self):
            Tests method to update customer credit, verifies new limit

        test_update_fake_customer_credit(self):
            Tests case where customer being updated does not exist

        test_active_customers(self):
            Tests method to return integer count of active customers
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Run before any tests. Clears Customer database, creates new customer
        '''
        # Clear database for tests
        cls.clear_database()
        # Create new customers, visible by all test cases
        cls.new_customer = {'id':'00001', 'firstname':'Ron', 'lastname':'Swanson',
                            'address':'123 Fake Street', 'phone':'555-867-5309',
                            'email':'ronswanson@pawnee.gov', 'status':0,
                            'credit_limit':10000}

    @staticmethod
    def clear_database():
        '''
        Resets database before tests are run
        '''
        # Set up empty table for testing
        database.drop_tables([Customer])
        database.create_tables([Customer])

    def add_customer_to_database(self):
        '''
        Method called by multiple tests, adds customer if not in database
        '''
        # Add customer if not part of database (certain tests add/delete records)
        query = Customer.select().where(Customer.id == self.new_customer['id'])
        if not query.exists():
            # Add customer (used by multiple tests)
            basic_operations.add_customer(self.new_customer['id'],
                                          self.new_customer['firstname'],
                                          self.new_customer['lastname'],
                                          self.new_customer['address'],
                                          self.new_customer['phone'],
                                          self.new_customer['email'],
                                          self.new_customer['status'],
                                          self.new_customer['credit_limit'])

    def test_customer_add(self):
        '''
        Test method to add customer to database
        '''
        # Add customer to database
        self.add_customer_to_database()
        # Retrieve customer to ensure all fields were added
        customer = Customer.get(Customer.id == self.new_customer['id'])
        self.assertEqual(customer.id, self.new_customer['id'])
        self.assertEqual(customer.firstname, self.new_customer['firstname'])
        self.assertEqual(customer.lastname, self.new_customer['lastname'])
        self.assertEqual(customer.address, self.new_customer['address'])
        self.assertEqual(customer.phone, self.new_customer['phone'])
        self.assertEqual(customer.email, self.new_customer['email'])
        self.assertEqual(customer.status, self.new_customer['status'])
        self.assertEqual(customer.credit_limit, self.new_customer['credit_limit'])

        # Add customer again, should handle exception
        basic_operations.add_customer(self.new_customer['id'],
                                      self.new_customer['firstname'],
                                      self.new_customer['lastname'],
                                      self.new_customer['address'],
                                      self.new_customer['phone'],
                                      self.new_customer['email'],
                                      self.new_customer['status'],
                                      self.new_customer['credit_limit'])

    def test_search_customer(self):
        '''
        Test method to search for customer
        '''
        # Add customer to database
        self.add_customer_to_database()
        # Define expected return value
        return_dict = {'firstname':'Ron', 'lastname':'Swanson',
                       'phone':'555-867-5309', 'email':'ronswanson@pawnee.gov'}
        # Search for customer in database
        customer_dict = basic_operations.search_customer(self.new_customer['id'])
        self.assertEqual(return_dict, customer_dict)

    def test_search_fake_customer(self):
        '''
        Tests case where customer being searched does not exist
        '''
        # Search for nonexistant customer, should return empty dictionary
        fake_customer_dict = basic_operations.search_customer('99999')
        self.assertEqual({}, fake_customer_dict)

    def test_delete_customer(self):
        '''
        Tests method to delete customer from database
        '''
        # Add customer to database
        self.add_customer_to_database()
        # Delete customer from database
        basic_operations.delete_customer(self.new_customer['id'])
        # Verify that trying to retrive the customer yields a DoesNotExist Error
        with self.assertRaises(DoesNotExist):
            Customer.get(Customer.id == self.new_customer['id'])

    def test_delete_fake_customer(self):
        '''
        Tests case where customer being deleted does not exist
        '''
        # Deleting a nonexistant customer should raise an error
        with self.assertRaises(DoesNotExist):
            basic_operations.delete_customer('99999')

    def test_update_customer_credit(self):
        '''
        Tests method to update customer credit, verifies new limit
        '''
        self.add_customer_to_database()
        # Update credit limit
        basic_operations.update_customer_credit(self.new_customer['id'], 15000)
        # Verify that credit limit has been updated
        updated_customer = Customer.get(Customer.id == self.new_customer['id'])
        self.assertEqual(updated_customer.credit_limit, 15000)

    def test_update_fake_customer_credit(self):
        '''
        Tests case where customer being updated does not exist
        '''
        # Ensure that updating a fake customer's credit raises a value error
        with self.assertRaises(ValueError):
            basic_operations.update_customer_credit('99999', 5000)

    def test_active_customers(self):
        '''
        Tests method to return integer count of active customers
        '''
        # Empty database should have no active customers
        num_active = basic_operations.list_active_customers()
        self.assertEqual(num_active, 0)

        # Add first customer and ensure that active count returns 0
        self.add_customer_to_database()
        num_active = basic_operations.list_active_customers()
        self.assertEqual(num_active, 0)

        # Change customer status to active
        customer = Customer.get(Customer.id == self.new_customer['id'])
        customer.status = 1
        customer.save()

        # Query number of active customers, should now be 1
        num_active = basic_operations.list_active_customers()
        self.assertEqual(num_active, 1)

        # Change customer status back to inactive (for other tests)
        customer.status = 0
        customer.save()
