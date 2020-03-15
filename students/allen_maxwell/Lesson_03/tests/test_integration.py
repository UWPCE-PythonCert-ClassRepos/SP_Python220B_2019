'''Integrated testing of the basic_operations module'''

# pylint disabled: C0413, E0401

from unittest import TestCase
import sys
import peewee

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

        test_dict = {'f_name': 'Bugs', 'l_name': 'Bunny', 'email': 'bugs_bunny@gmail.com',
                     'phone': '425-123-4567'}

        # Test adding customers
        basic_operations.add_customer(*cust_list[0])
        basic_operations.add_customer(*cust_list[1])
        basic_operations.add_customer(*cust_list[2])

        cust_0 = Customer.get(Customer.cust_id == 101)
        cust_1 = Customer.get(Customer.cust_id == 123)
        cust_2 = Customer.get(Customer.cust_id == 53)

        # Verify customers were added
        try:
            self.assertEqual(cust_0.f_name, cust_list[0][1])
            self.assertEqual(cust_1.f_name, cust_list[1][1])
            self.assertEqual(cust_2.f_name, cust_list[2][1])
        except peewee.IntegrityError:
            assert False

        # Verify duplicate customers are not added
        try:
            with self.assertRaises(ValueError):
                basic_operations.add_customer(*cust_list[2])
        except peewee.IntegrityError:
            assert False

        # Verify able to search and find a customer
        self.assertEqual(basic_operations.search_customer(101), test_dict)

        # Verify searching for a non-existant customer is empty
        self.assertEqual(basic_operations.search_customer(3), {})

        # Verify able to update customer credit limit
        try:
            basic_operations.update_customer_credit(123, 100000)
            cust_1 = Customer.get(Customer.cust_id == 123)
            self.assertEqual(cust_1.credit, 100000)
        except peewee.IntegrityError:
            assert False

        # Verify customer credit limit cannot be updated for non-customer
        with self.assertRaises(ValueError):
            basic_operations.update_customer_credit(42, 1000)

        # Verify active customers are counted
        self.assertEqual(basic_operations.list_active_customers(), 2)

        # Verify a customer can be deleted
        try:
            basic_operations.delete_customer(53)
            self.assertEqual(cust_0.f_name, cust_list[0][1])
            self.assertEqual(cust_1.f_name, cust_list[1][1])
            try:
                Customer.get(Customer.cust_id == 53)
                assert False
            except peewee.DoesNotExist:
                assert True
        except peewee.IntegrityError:
            assert False

        # Verify a non-customer cannot be deleted
        with self.assertRaises(ValueError):
            basic_operations.delete_customer(55)
