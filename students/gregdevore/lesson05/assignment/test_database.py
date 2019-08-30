'''
Insert docstring
'''

from unittest import TestCase
import database
import os

class DBTests(TestCase):
    '''
    Test suite for testing the database module
    '''
    def test_csv_to_json(self):
        directory = 'data'
        product_file = 'products.csv'
        customer_file = 'customers.csv'
        rentals_file = 'rentals.csv'

        product_json_expected = [{'product_id': 'prd001', 'description': 'sofa',
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

        product_json_actual = database.import_csv_to_json(os.path.join(directory,product_file))

        customer_json_expected = [{'user_id': 'user001', 'name': 'Jake Peralta',
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

        customer_json_actual = database.import_csv_to_json(os.path.join(directory,customer_file))

        rentals_json_expected = [{'rental_id': 'rnt001', 'customer_id': 'user003',
        'product_id': 'prd001'}, {'rental_id': 'rnt002', 'customer_id': 'user005',
        'product_id': 'prd005'}, {'rental_id': 'rnt003', 'customer_id': 'user002',
        'product_id': 'prd004'}, {'rental_id': 'rnt004', 'customer_id': 'user006',
        'product_id': 'prd009'}, {'rental_id': 'rnt005', 'customer_id': 'user006',
        'product_id': 'prd010'}, {'rental_id': 'rnt006', 'customer_id': 'user001',
        'product_id': 'prd002'}]

        rentals_json_actual = database.import_csv_to_json(os.path.join(directory,rentals_file))

        self.assertEqual(product_json_expected, product_json_actual)
        self.assertEqual(customer_json_expected, customer_json_actual)
        self.assertEqual(rentals_json_expected, rentals_json_actual)
