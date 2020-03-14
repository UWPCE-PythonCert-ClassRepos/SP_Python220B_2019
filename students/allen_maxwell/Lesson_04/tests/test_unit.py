'''Tests the basic_operations module'''

# pylint disabled: C0413, E0401

from unittest import TestCase
import sys

sys.path.insert(1, '../')
from customer_model import DATABASE, Customer
import basic_operations

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
        # Test Adding individual customers
        cust_0 = basic_operations.add_customer(*TEST_LIST[0])
        cust_1 = basic_operations.add_customer(*TEST_LIST[1])
        cust_2 = basic_operations.add_customer(*TEST_LIST[2])
        # Test instances of added customers
        self.assertIsInstance(cust_0, Customer)
        self.assertIsInstance(cust_1, Customer)
        self.assertIsInstance(cust_2, Customer)
        # Verify added customer data
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
        # Test adding an existing customer
        with self.assertRaises(ValueError):
            basic_operations.add_customer(*TEST_LIST[2])

    def test_add_customers(self):
        '''Tests add a new customer to the database.'''
        reset_db()
        # Test Adding a list of customers
        customers = basic_operations.add_customers(TEST_LIST)
        # Test instances of added customers
        self.assertIsInstance(customers[0], Customer)
        self.assertIsInstance(customers[1], Customer)
        self.assertIsInstance(customers[2], Customer)
        # Verify added customers data
        self.assertEqual(Customer.get(Customer.cust_id == 101).f_name, TEST_LIST[0][1])
        self.assertEqual(Customer.get(Customer.cust_id == 123).f_name, TEST_LIST[1][1])
        self.assertEqual(Customer.get(Customer.cust_id == 53).f_name, TEST_LIST[2][1])

    def test_search_customer(self):
        '''Tests search_customer function.'''
        reset_db()
        basic_operations.add_customers(TEST_LIST)
        # Testing the search_customer function
        self.assertEqual(basic_operations.search_customer(101)['f_name'], TEST_LIST[0][1])
        # Test searching for a non-existing customer
        self.assertEqual(basic_operations.search_customer(3), {})

    def test_search_customers(self):
        '''Tests search_customers function.'''
        reset_db()
        basic_operations.add_customers(TEST_LIST)
        # Testing the search_customers function
        customers_search = basic_operations.search_customers([101, 53])
        self.assertEqual(customers_search[0]['f_name'], TEST_LIST[0][1])
        self.assertEqual(customers_search[1]['f_name'], TEST_LIST[2][1])

    def test_delete_customer(self):
        '''Tests the delete_customer function.'''
        reset_db()
        basic_operations.add_customers(TEST_LIST)
        # Testing the delete_customer function
        basic_operations.delete_customer(123)
        self.assertEqual(basic_operations.search_customer(101)['f_name'], TEST_LIST[0][1])
        self.assertEqual(basic_operations.search_customer(53)['f_name'], TEST_LIST[2][1])
        self.assertEqual(basic_operations.search_customer(123), {})
        # Testing the delete_customer not in the database
        with self.assertRaises(ValueError):
            basic_operations.delete_customer(55)

    def test_delete_customers(self):
        '''Tests delete_customers function.'''
        reset_db()
        basic_operations.add_customers(TEST_LIST)
        # Testing the delete_customers function
        basic_operations.delete_customers([101, 53])
        self.assertEqual(basic_operations.search_customer(101), {})
        self.assertEqual(basic_operations.search_customer(53), {})
        self.assertEqual(basic_operations.search_customer(123)['f_name'], TEST_LIST[1][1])

    def test_update_customer_credit(self):
        '''Tests the update_customer_credit limit function.'''
        reset_db()
        basic_operations.add_customers(TEST_LIST)
        # Testing the update_customer_credit function
        basic_operations.update_customer_credit(123, 100000)
        self.assertEqual(Customer.get(Customer.cust_id == 123).credit, 100000)
        # Testing the update_customer_credit for customers not in the database
        with self.assertRaises(ValueError):
            basic_operations.update_customer_credit(42, 1000)

    def test_list_active_customers(self):
        '''Tests the list_active_customers whose status is currently active.'''
        reset_db()
        # Testing no active customers
        self.assertEqual(basic_operations.list_active_customers(), 0)
        basic_operations.add_customers(TEST_LIST)
        # Testing some active customers
        self.assertEqual(basic_operations.list_active_customers(), 2)
