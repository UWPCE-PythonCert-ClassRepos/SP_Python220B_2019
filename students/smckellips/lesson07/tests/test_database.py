# pylint: disable=W0401,W0614
'''
UnitTest Module for database.py
Copied from lesson05.  Data is no longer accurate.
'''
from unittest import TestCase
from parallel import *


class TestDatabase(TestCase):
    '''UnitTest class to test database.py'''

    def setUp(self):
        '''setup module for unittests.'''
        self.context_mgr = MongoDBConnection()

        self.product_list = ['prd001', 'prd002', 'prd003',
                             'prd004', 'prd005', 'prd006', 'prd007', 'prd008']
        self.available_product = [
            {'description': '60-inch TV stand', 'product_id': 'prd001',
             'product_type': 'livingroom', 'quantity_available': '3'},
            {'description': 'L-shaped sofa', 'product_id': 'prd002',
             'product_type': 'livingroom', 'quantity_available': '1'},
            {'description': 'Queen size bed frame', 'product_id': 'prd003',
             'product_type': 'bedroom', 'quantity_available': '2'},
            {'description': 'Table with leaves', 'product_id': 'prd004',
             'product_type': 'diningroom', 'quantity_available': '1'},
            {'description': 'Desk', 'product_id': 'prd005',
             'product_type': 'den', 'quantity_available': '3'},
            {'description': 'Desk Light', 'product_id': 'prd006',
             'product_type': 'den', 'quantity_available': '4'},
            {'description': 'Throw Pillow', 'product_id': 'prd008',
             'product_type': 'livingroom', 'quantity_available': '10'}
        ]
        self.rental_list = [
            {'address': '12567 N 23rd St', 'customer_id': 'user004', 'email': 'dd@gmail.com',
             'name': 'Daniel Danielson', 'phone_number': '509-233-9932'},
            {'address': '3434 Swing St', 'customer_id': 'user007', 'email': 'gertie1000@gmail.com',
             'name': 'Greta Gershwin', 'phone_number': '206-725-1222'}
        ]

    def test_purge_data(self):
        '''tet new concurrent import.'''
        # First reset the db
        with self.context_mgr:
            self.context_mgr.connection.drop_database(DB_NAME)
        prod_count = document_count('Product')
        cust_count = document_count('Customer')
        self.assertEqual(prod_count, 0)
        self.assertEqual(cust_count, 0)


    def test_orig_import_data(self):
        '''test import data function.'''
        # First reset the db
        with self.context_mgr:
            self.context_mgr.connection.drop_database(DB_NAME)

        count, errors = orig_import_data(
            'data', 'products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(count, (999, 999, 12))
        self.assertEqual(errors, (0, 0, 0))

    def test_new_import_data(self):
        '''test import data function.'''
        # First reset the db
        with self.context_mgr:
            self.context_mgr.connection.drop_database(DB_NAME)

        product_tuple, customer_tuple = import_data(
            'data', 'products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(product_tuple[0], 999)
        self.assertEqual(product_tuple[1], 0)
        self.assertEqual(product_tuple[2], 999)
        self.assertEqual(customer_tuple[0], 999)
        self.assertEqual(customer_tuple[1], 0)
        self.assertEqual(customer_tuple[2], 999)


    def test_list_products(self):
        '''test list all products.'''
        all_products = list_products()
        self.assertEqual(all_products, self.product_list)

    def test_list_available_products(self):
        '''test list all products.'''
        avail_products = list_available_products()
        self.assertEqual(avail_products, self.available_product)
        self.assertEqual(len(avail_products), 7)

    def test_show_rentals(self):
        '''test show rentals.'''
        rentals = show_rentals('prd005')
        self.assertEqual(rentals, self.rental_list)
