''' Testing Database.py'''

from unittest import TestCase
import database as db

class TestDatabase(TestCase):
    ''' Testing the Parts of Database.py '''
    def test_import_data(self):
        ''' Test Importing Data '''
        count = db.import_data('D:\\UW\\PY220\\Examples and Assignments\\lesson05\\csv_files\\',
                               'products.csv', 'customers.csv', 'rentals.csv')
        expected_count = ((4, 3, 4), (0, 0, 0))
        self.assertEqual(count, expected_count)


    def test_show_available_products(self):
        ''' Test Showing Available Products'''
        data = db
        data.import_data('D:\\UW\\PY220\\Examples and Assignments\\lesson05\\csv_files\\',
                         'products.csv', 'customers.csv', 'rentals.csv')

        expected_dict = {'1177': {'product_id': '1177', 'description': 'Television',
                                  'product_type': 'Electronic', 'quantity_available': '5'},
                         '5550': {'product_id': '5550', 'description': 'Chair',
                                  'product_type': 'Furniture', 'quantity_available': '2'},
                         '5198': {'product_id': '5198', 'description': 'Couch',
                                  'product_type': 'Furniture', 'quantity_available': '4'},
                         '1356': {'product_id': '1356', 'description': 'Radio',
                                  'product_type': 'Electronic', 'quantity_available': '3'}}

        self.assertEqual(data.show_available_products(), expected_dict)

    def test_show_rentals(self):
        ''' Test Showing Rentals '''
        data = db
        data.import_data('D:\\UW\\PY220\\Examples and Assignments\\lesson05\\csv_files\\',
                         'products.csv', 'customers.csv', 'rentals.csv')

        expected_rental = {'1150': {'name': 'Mark Rollins', 'rental_id': '0144',
                                    'address': '46 Hawthorne Lane, Great Falls, MT 59404',
                                    'phone_number': '406-604-4060',
                                    'email': 'rockinrollins@gmail.com'},
                           '3030': {'name': 'Joseph Tribbiani', 'rental_id': '0255',
                                    'address': '43 Foster Avenue, New York, NY 10003',
                                    'phone_number': '212-013-7564',
                                    'email': 'joeytribbiani@gmail.com'}}

        self.assertEqual(data.show_rentals('1177'), expected_rental)
