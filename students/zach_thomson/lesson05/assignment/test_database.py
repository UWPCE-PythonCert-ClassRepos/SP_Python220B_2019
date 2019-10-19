'''
tests for the MongoDB database assignment
'''
import csv
import os
from unittest import TestCase
from database import import_data, show_available_products, show_rentals

class MongoDBTest(TestCase):
    '''tests for basic operations'''

    def test_import_data(self):
        '''tests csv files are imported correctly with
        correct tuples being returned'''
        test_import = import_data('csv_files', 'product_file.csv',
                                  'customer_file.csv', 'rental_file.csv')
        self.assertEqual(test_import, [(4, 2, 2), (0, 0, 0)])

    def test_show_available_products(self):
        import_data('csv_files', 'product_file.csv', 'customer_file.csv', 'rental_file.csv')
        actual_output = show_available_products()
        expected_dict = {'prd001':{'description':'60-inch TV stand',
                                   'product_type':'livingroom', 'quantity_available':'3'},
                         'prd002':{'description':'L-shaped sofa',
                                   'product_type':'livingroom', 'quantity_available':'1'},
                         'prd004':{'description': '60-inch dining table',
                                   'product_type': 'diningroom', 'quantity_available': '2'}}
        self.assertEqual(actual_output, expected_dict)

    def test_show_rentals(self):
        import_data('csv_files', 'product_file.csv', 'customer_file.csv', 'rental_file.csv')
        actual_output = show_rentals('prd002')
        expected_dict = {'user001':{'name':'Elisa Miles', 'address':'4490 Union Street',
                                    'phone_number':'206-922-0882', 'email':'elisa.miles@yahoo.com'}}
        self.assertEqual(actual_output, expected_dict)
