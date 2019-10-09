# pylint: disable=W0614, W0401
'''
tests for the basic operations/customer database
'''

from unittest import TestCase
from peewee import *
from customer_db_model import Customer
from basic_operations import *

TEST_DB = SqliteDatabase('test.db')

def db_setup():
    '''sets up an empty database for testing'''
    TEST_DB.drop_tables([Customer])
    TEST_DB.create_tables([Customer])


class BasicOperationsTest(TestCase):
    '''tests for basic operations'''

    def test_add_customer(self):
        '''test add customer function'''
        db_setup()

        add_customer(1234, 'Zach', 'Thomson', '1000 John St', '2068675309',
                     'ScubaSteve@gmail.com', True, 1000.00)
        generic = Customer.get(Customer.customer_id == 1234)
        self.assertEqual(generic.customer_id, 1234)
        self.assertEqual(generic.name, 'Zach')
        self.assertEqual(generic.last_name, 'Thomson')
        self.assertEqual(generic.home_address, '1000 John St')
        self.assertEqual(generic.phone_number, '2068675309')
        self.assertEqual(generic.email_address, 'ScubaSteve@gmail.com')
        self.assertEqual(generic.status, True)
        self.assertEqual(generic.credit_limit, 1000.00)

    def test_search_customer(self):
        '''tests search_customer function'''
        db_setup()

        add_customer(1234, 'Zach', 'Thomson', '1000 John St', '2068675309',
                     'ScubaSteve@gmail.com', True, 1000.00)
        search = search_customer(1234)
        expected_dict = {'name': 'Zach', 'last_name': 'Thomson',
                         'email_address': 'ScubaSteve@gmail.com', 'phone_number': '2068675309'}
        self.assertEqual(search, expected_dict)

    def test_search_fail(self):
        '''tests exception handling of a search for a customer that is not in
        the database'''
        db_setup()

        add_customer(1234, 'Zach', 'Thomson', '1000 John St', '2068675309',
                     'ScubaSteve@gmail.com', True, 1000.00)
        search_2 = search_customer(900)
        new_exp_dict = {}
        self.assertEqual(search_2, new_exp_dict)


    def test_delete_customer(self):
        '''tests delete_customer function'''
        db_setup()

        add_customer(1234, 'Zach', 'Thomson', '1000 John St', '2068675309',
                     'ScubaSteve@gmail.com', True, 1000.00)
        delete_customer(1234)
        search = search_customer(1234)
        exp_dict = {}
        self.assertEqual(search, exp_dict)

    def test_delete_fail(self):
        '''tests exception handling of attemting to delete a customer that
        is not in the system'''
        db_setup()
        self.assertRaises(ValueError, delete_customer, 1)

    def test_update_customer_credit(self):
        '''tests updating a customers credit'''
        db_setup()

        add_customer(1234, 'Zach', 'Thomson', '1000 John St', '2068675309',
                     'ScubaSteve@gmail.com', True, 1000.00)
        #test credit update success
        update_customer_credit(1234, 2000.00)
        new_credit = Customer.get(Customer.customer_id == 1234)
        self.assertEqual(new_credit.credit_limit, 2000.00)

        #test credit update failure
        self.assertRaises(ValueError, update_customer_credit, 9000, 10.00)

    def test_list_active_customers(self):
        '''tests the return of list_active_customers function'''
        db_setup()

        add_customer(1234, 'Zach', 'Thomson', '1000 John St', '2068675309',
                     'ScubaSteve@gmail.com', True, 1000.00)
        add_customer(1235, 'Bob', 'Doe', '1001 John St', '2068675310',
                     'ScubaSteve1@gmail.com', False, 1000.00)
        add_customer(1236, 'Sally', 'Field', '1002 John St', '2068675311',
                     'ScubaSteve2@gmail.com', True, 1000.00)

        self.assertEqual(list_active_customers(), 2)
