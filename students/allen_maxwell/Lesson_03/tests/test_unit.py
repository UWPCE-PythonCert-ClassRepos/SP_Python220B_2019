'''Tests the basic_operations module'''

# pylint disabled: C0413, E0401

from unittest import TestCase
import logging
import sys
import peewee

sys.path.insert(1, '../')
from customer_model import DATABASE, Customer
import basic_operations

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

TEST_LIST = [(101, 'Bugs', 'Bunny', '123 NE 160th Ave, Kirkland, WA 98034', '425-123-4567',
              'bugs_bunny@gmail.com', 'Active', 100.00),
             (123, 'Donald', 'Duck', '456 SE 45th St, Bellevue, WA 98004', '425-234-5678',
              'donald_duck@gmail.com', 'Active', 500.00),
             (53, 'Elmer', 'Fudd', '789 W 52nd Pl, Bothell, WA 98077', '425-345-6789',
              'elmer_fudd@gmail.com', 'Inactive', 12000.00)]

def reset_db():
    '''Resets the database'''
    DATABASE.drop_tables([Customer])
    DATABASE.create_tables([Customer])

class TestBasicOperations(TestCase):
    '''Test Basic operations Class'''
    def test_add_customer(self):
        '''Tests add a new customer to the database.'''
        reset_db()
        LOGGER.info('Testing the add_customer function')

        basic_operations.add_customer(*TEST_LIST[0])
        basic_operations.add_customer(*TEST_LIST[1])
        basic_operations.add_customer(*TEST_LIST[2])

        cust_0 = Customer.get(Customer.cust_id == 101)
        cust_1 = Customer.get(Customer.cust_id == 123)
        cust_2 = Customer.get(Customer.cust_id == 53)

        try:
            self.assertEqual(cust_0.f_name, TEST_LIST[0][1])
            self.assertEqual(cust_0.l_name, TEST_LIST[0][2])
            self.assertEqual(cust_0.address, TEST_LIST[0][3])
            self.assertEqual(cust_0.phone, TEST_LIST[0][4])
            self.assertEqual(cust_0.email, TEST_LIST[0][5])
            self.assertEqual(cust_0.status, TEST_LIST[0][6])
            self.assertEqual(cust_0.credit, TEST_LIST[0][7])

            self.assertEqual(cust_1.f_name, TEST_LIST[1][1])
            self.assertEqual(cust_1.address, TEST_LIST[1][3])
            self.assertEqual(cust_1.phone, TEST_LIST[1][4])
            self.assertEqual(cust_1.email, TEST_LIST[1][5])
            self.assertEqual(cust_1.status, TEST_LIST[1][6])
            self.assertEqual(cust_1.credit, TEST_LIST[1][7])

            self.assertEqual(cust_2.f_name, TEST_LIST[2][1])
            self.assertEqual(cust_2.address, TEST_LIST[2][3])
            self.assertEqual(cust_2.phone, TEST_LIST[2][4])
            self.assertEqual(cust_2.email, TEST_LIST[2][5])
            self.assertEqual(cust_2.status, TEST_LIST[2][6])
            self.assertEqual(cust_2.credit, TEST_LIST[2][7])

        except peewee.IntegrityError:
            assert False

        LOGGER.info('Test adding an existing customer')
        try:
            with self.assertRaises(ValueError):
                basic_operations.add_customer(*TEST_LIST[2])
        except peewee.IntegrityError:
            assert False

    def test_search_customer(self):
        '''Tests search_customer function.'''
        reset_db()
        LOGGER.info('Testing the search_customer function')
        test_dict = {'f_name': 'Bugs', 'l_name': 'Bunny', 'email': 'bugs_bunny@gmail.com',
                     'phone': '425-123-4567'}

        basic_operations.add_customer(*TEST_LIST[0])
        basic_operations.add_customer(*TEST_LIST[1])
        basic_operations.add_customer(*TEST_LIST[2])

        LOGGER.info('Test searching for a customer')
        self.assertEqual(basic_operations.search_customer(101), test_dict)
        LOGGER.info('Test searching for a non-existing customer')
        self.assertEqual(basic_operations.search_customer(3), {})

    def test_delete_customer(self):
        '''Tests the delete_customer function.'''
        reset_db()
        LOGGER.info('Testing the delete_customer function')

        basic_operations.add_customer(*TEST_LIST[0])
        basic_operations.add_customer(*TEST_LIST[1])
        basic_operations.add_customer(*TEST_LIST[2])
        cust_0 = Customer.get(Customer.cust_id == 101)
        cust_2 = Customer.get(Customer.cust_id == 53)

        try:
            basic_operations.delete_customer(123)
            self.assertEqual(cust_0.f_name, TEST_LIST[0][1])
            self.assertEqual(cust_2.f_name, TEST_LIST[2][1])
            try:
                Customer.get(Customer.cust_id == 123)
                assert False
            except peewee.DoesNotExist:
                assert True
        except peewee.IntegrityError:
            assert False

        LOGGER.info('Testing the delete_customer not in the database')
        with self.assertRaises(ValueError):
            basic_operations.delete_customer(55)

    def test_update_customer_credit(self):
        '''Tests the update_customer_credit limit function.'''
        reset_db()
        LOGGER.info('Testing the update_customer_credit function')

        basic_operations.add_customer(*TEST_LIST[0])
        basic_operations.add_customer(*TEST_LIST[1])
        basic_operations.add_customer(*TEST_LIST[2])

        LOGGER.info('Testing the update_customer_credit for customers in the database')
        try:
            basic_operations.update_customer_credit(123, 100000)
            cust_1 = Customer.get(Customer.cust_id == 123)
            self.assertEqual(cust_1.credit, 100000)
            LOGGER.info('Testing the update_customer_credit for customers in the database Passed')
        except peewee.IntegrityError:
            LOGGER.info('Testing the update_customer_credit for customers in the database Failed')
            assert False

        LOGGER.info('Testing the update_customer_credit for customers not in the database')
        with self.assertRaises(ValueError):
            basic_operations.update_customer_credit(42, 1000)

    def test_list_active_customers(self):
        '''Tests the list_active_customers whose status is currently active.'''
        reset_db()
        try:
            LOGGER.info('Testing no active customers')
            self.assertEqual(basic_operations.list_active_customers(), 0)
            basic_operations.add_customer(*TEST_LIST[0])
            basic_operations.add_customer(*TEST_LIST[1])
            basic_operations.add_customer(*TEST_LIST[2])
            LOGGER.info('Testing some active customers')
            self.assertEqual(basic_operations.list_active_customers(), 2)
        except peewee.DoesNotExist:
            assert False
