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
        test_import = import_data('csv_files', 'product_file.csv', 'customer_file.csv', 'rental_file.csv')
        self.assertEqual(test_import, [(4, 2, 2), (0, 0, 0)])

    def test_show_available_products(self):
        pass

    def test_show_rentals(self):
        pass
