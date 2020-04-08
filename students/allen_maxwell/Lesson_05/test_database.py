'''Unit Test for database.py'''

from unittest import TestCase
import database as db

class TestDatabase(TestCase):
    '''Setup test files'''

    def setUp(self):
        # create test files
        with open('tests/products.csv', 'w') as file:
            file.writelines(
                'product_id,description,product_type,quantity_available\n'
                'prd001,60-inch TV stand,livingroom,3\n'
                'prd002,L-shaped sofa,livingroom,1\n'
                'prd003,Queen Bed,bedroom,0\n')
        with open('tests/customers.csv', 'w') as file:
            file.writelines(
                'user_id,name,address,phone_number,email\n'
                'user001,Elisa Miles,4490 Union Street,206-922-0882,elisa.miles@yahoo.com\n'
                'user002,Maya Data,4936 Elliot Avenue,206-777-1927,mdata@uw.edu\n')
        with open('tests/customers_fail.csv', 'w') as file:
            file.writelines(
                'user_id,name,address,phone_number,email\n')
        with open('tests/rentals.csv', 'w') as file:
            file.writelines(
                'user_id,name,product_id\n'
                'user001,Elisa Miles,prd002\n'
                'user002,Maya Data,prd001\n')

    def test_import_data(self):
        '''Test importing data'''
        counts, errors = db.import_data('tests', 'products', 'customers', 'rentals')
        self.assertEqual(counts, (3, 2, 2))
        self.assertEqual(errors, (0, 0, 0))

    def test_import_data_fail(self):
        '''Tests importing invalid file_name and empty data file errors'''
        counts, errors = db.import_data('tests', 'products_fail', 'customers_fail', 'rentals')
        self.assertEqual(counts, (0, 0, 2))
        self.assertEqual(errors, (1, 1, 0))

    def test_show_available_products(self):
        '''Tests shows available products'''
        db.import_data('tests', 'products', 'customers', 'rentals')
        result = db.show_available_products()
        expected = {'prd001': {'description': '60-inch TV stand',
                               'product_type': 'livingroom',
                               'quantity_available': '3'},
                    'prd002': {'description': 'L-shaped sofa',
                               'product_type': 'livingroom',
                               'quantity_available': '1'}}
        self.assertEqual(expected, result)

    def test_show_rentals(self):
        '''Test show rentals'''
        db.import_data('tests', 'products', 'customers', 'rentals')
        result = db.show_rentals('prd001')
        expected = {'user002': {'name': 'Maya Data', 'address': '4936 Elliot Avenue',
                                'phone_number': '206-777-1927', 'email': 'mdata@uw.edu'}}
        self.assertEqual(expected, result)
        # Tests for non-existant product
        result = db.show_rentals('prd003')
        self.assertEqual({}, result)
