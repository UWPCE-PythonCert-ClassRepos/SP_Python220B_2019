'''
Insert docstring
'''

from unittest import TestCase
from database import *
import os
from pymongo import MongoClient

class DBTests(TestCase):
    '''
    Test suite for testing the database module
    '''
    @classmethod
    def setUpClass(cls):
        cls.product_json = [{'product_id': 'prd001', 'description': 'sofa',
         'product_type': 'livingroom', 'quantity_available': '4'},
         {'product_id': 'prd002', 'description': 'coffee table',
         'product_type': 'livingroom', 'quantity_available': '2'},
         {'product_id': 'prd003', 'description': 'lounge chair',
         'product_type': 'livingroom', 'quantity_available': '0'},
         {'product_id': 'prd004', 'description': 'refrigerator',
         'product_type': 'kitchen', 'quantity_available': '2'},
         {'product_id': 'prd005', 'description': 'microwave',
         'product_type': 'kitchen', 'quantity_available': '5'},
         {'product_id': 'prd006', 'description': 'toaster',
         'product_type': 'kitchen', 'quantity_available': '1'},
         {'product_id': 'prd007', 'description': 'night stand',
         'product_type': 'bedroom', 'quantity_available': '6'},
         {'product_id': 'prd008', 'description': 'dresser',
         'product_type': 'bedroom', 'quantity_available': '0'},
         {'product_id': 'prd009', 'description': 'queen mattress',
         'product_type': 'bedroom', 'quantity_available': '3'},
         {'product_id': 'prd010', 'description': 'queen box spring',
         'product_type': 'bedroom', 'quantity_available': '3'}]

        cls.customer_json = [{'user_id': 'user001', 'name': 'Jake Peralta',
        'address': '123 Precinct Lane', 'phone_number': '917-555-0001',
        'email': 'jperalta@brooklyn.pd'}, {'user_id': 'user002',
        'name': 'Rose Diaz', 'address': '123 Precinct Lane',
        'phone_number': '917-555-0002', 'email': 'rdiaz@brooklyn.pd'},
        {'user_id': 'user003', 'name': 'Terry Jeffords',
        'address': '123 Precinct Lane', 'phone_number': '917-555-0003',
        'email': 'tjeffords@brooklyn.pd'}, {'user_id': 'user004',
        'name': 'Amy Santiago', 'address': '123 Precinct Lane',
        'phone_number': '917-555-0004', 'email': 'asantiago@brooklyn.pd'},
        {'user_id': 'user005', 'name': 'Charles Boyle',
        'address': '123 Precinct Lane', 'phone_number': '917-555-0005',
        'email': 'cboyle@brooklyn.pd'}, {'user_id': 'user006',
        'name': 'Ray Holt', 'address': '123 Precinct Lane',
        'phone_number': '917-555-0006', 'email': 'rholt@brooklyn.pd'},
        {'user_id': 'user007', 'name': 'Gina Linetti',
        'address': '123 Precinct Lane', 'phone_number': '917-555-0007',
        'email': 'glinetti@brooklyn.pd'}]

        cls.rentals_json = [{'rental_id': 'rnt001', 'customer_id': 'user003',
        'product_id': 'prd001'}, {'rental_id': 'rnt002', 'customer_id': 'user005',
        'product_id': 'prd005'}, {'rental_id': 'rnt003', 'customer_id': 'user002',
        'product_id': 'prd004'}, {'rental_id': 'rnt004', 'customer_id': 'user006',
        'product_id': 'prd009'}, {'rental_id': 'rnt005', 'customer_id': 'user006',
        'product_id': 'prd010'}, {'rental_id': 'rnt006', 'customer_id': 'user001',
        'product_id': 'prd002'}]

    @classmethod
    def tearDown(cls):
        '''
        Drop mongo collections after each test to ensure a fresh start
        '''
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.HPNorton
            db['product'].drop()
            db['customer'].drop()
            db['rentals'].drop()

    def test_csv_to_json(self):
        directory = 'data'
        product_file = 'products.csv'
        customer_file = 'customers.csv'
        rentals_file = 'rentals.csv'

        product_json_actual, product_errors = import_csv_to_json(os.path.join(directory,product_file))
        customer_json_actual, customer_errors = import_csv_to_json(os.path.join(directory,customer_file))
        rentals_json_actual, rentals_errors = import_csv_to_json(os.path.join(directory,rentals_file))

        self.assertEqual(self.product_json, product_json_actual)
        self.assertEqual(self.customer_json, customer_json_actual)
        self.assertEqual(self.rentals_json, rentals_json_actual)

    def test_bad_csv_to_json(self):
        return_data, error_count = import_csv_to_json('fake_file')
        self.assertEqual(return_data,[])
        self.assertEqual(error_count, 1)

    def test_json_to_mongo(self):
        product_counts = add_json_to_mongodb(self.product_json,'product')
        customer_counts = add_json_to_mongodb(self.customer_json,'customer')
        rentals_counts = add_json_to_mongodb(self.rentals_json,'rentals')
        self.assertEqual(product_counts,(10,0))
        self.assertEqual(customer_counts,(7,0))
        self.assertEqual(rentals_counts,(6,0))

    def test_import_data(self):
        counts, errors = import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(counts,(10,7,6))
        self.assertEqual(errors,(0,0,0))
