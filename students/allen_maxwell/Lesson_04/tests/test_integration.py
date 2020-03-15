'''Integrated testing of the basic_operations module'''

# pylint disabled: C0413, E0401

from unittest import TestCase
import sys

sys.path.insert(1, '../')
from customer_model import DATABASE, Customer
import basic_operations

DATABASE.drop_tables([Customer])
DATABASE.create_tables([Customer])

class TestBasicOperations(TestCase):
    '''Testing basic_operations functioanlity'''
    def test_integration(self):
        '''Integrated test set'''
        cust_list = [(101, 'Bugs', 'Bunny', '123 NE 160th Ave, Kirkland, WA 98034', '425-123-4567',
                      'bugs_bunny@gmail.com', 'Active', 100.00),
                     (123, 'Donald', 'Duck', '456 SE 45th St, Bellevue, WA 98004', '425-234-5678',
                      'donald_duck@gmail.com', 'Active', 500.00),
                     (53, 'Elmer', 'Fudd', '789 W 52nd Pl, Bothell, WA 98077', '425-345-6789',
                      'elmer_fudd@gmail.com', 'Inactive', 12000.00)]

        test_list = [{'f_name': 'Elmer', 'l_name': 'Fudd', 'email': 'elmer_fudd@gmail.com',
                      'phone': '425-345-6789'},
                     {'f_name': 'Bugs', 'l_name': 'Bunny', 'email': 'bugs_bunny@gmail.com',
                      'phone': '425-123-4567'}]

        # Test adding customers
        basic_operations.add_customers(cust_list)

        # Verify customers were added
        self.assertEqual(Customer.get(Customer.cust_id == 101).f_name, cust_list[0][1])
        self.assertEqual(Customer.get(Customer.cust_id == 123).f_name, cust_list[1][1])
        self.assertEqual(Customer.get(Customer.cust_id == 53).f_name, cust_list[2][1])

        # Verify duplicate customers are not added
        with self.assertRaises(ValueError):
            basic_operations.add_customer(*cust_list[2])

        # Verify able to search for customers
        customers = basic_operations.search_customers([53, 101, 33])
        self.assertEqual(customers[0], test_list[0])
        self.assertEqual(customers[1], test_list[1])

        # Verify searching for a non-existant customer is empty
        self.assertEqual(customers[2], {})

        # Verify able to update customer credit limit
        basic_operations.update_customer_credit(123, 100000)
        cust_1 = Customer.get(Customer.cust_id == 123)
        self.assertEqual(cust_1.credit, 100000)

        # Verify customer credit limit cannot be updated for non-customer
        with self.assertRaises(ValueError):
            basic_operations.update_customer_credit(42, 1000)

        # Verify active customers are counted
        self.assertEqual(basic_operations.list_active_customers(), 2)

        # Verify a customer can be deleted
        basic_operations.delete_customers([53, 123])
        self.assertEqual(Customer.get(Customer.cust_id == 101).f_name, cust_list[0][1])
        self.assertEqual(basic_operations.search_customer(123), {})
        self.assertEqual(basic_operations.search_customer(53), {})

        # Verify handling of deleting non-customers
        with self.assertRaises(ValueError):
            basic_operations.delete_customer(53)
