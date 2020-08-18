'''Testing database.py'''

from unittest import TestCase
import logging
import os
import database

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
PATH = (os.getcwd())

class TestDatabase(TestCase):
    '''test the basic functions in database.py'''

    def test_import_data(self):
        '''Test import_data function'''
        LOGGER.info('dropping db tables')
        database.clear_all()
        LOGGER.info('importing data from bad path')
        import_1 = database.import_data(PATH, 'products.csv', 'customers.csv',
                                        'rentals.csv')
        LOGGER.info('importing data from correct path')
        import_2 = database.import_data(PATH, 'data/products.csv',
                                        'data/customers.csv', 'data/rentals.csv')
        self.assertEqual(list(import_1), [(0, 0, 0), (1, 1, 1)]) # File Not Found
        self.assertEqual(list(import_2), [(4, 3, 3), (0, 0, 0)]) # File exists

    def test_show_available_products(self):
        '''Test show_available_products function'''
        LOGGER.info('dropping db tables')
        database.clear_all()
        LOGGER.info('importing data test_show_available_products')
        database.import_data(PATH, 'data/products.csv', 'data/customers.csv', 'data/rentals.csv')
        expected = {'p2': {'description': 'couch', 'product_type': 'livingroom',
                           'quantity_available': '1'},
                    'p3': {'description': 'chair', 'product_type': 'office',
                           'quantity_available': '4'},
                    'p4': {'description': 'table', 'product_type': 'diningroom',
                           'quantity_available': '2'}}
        dict_test = database.show_available_products()
        self.assertEqual(expected, dict_test)
        LOGGER.info('dropping db tables')
        database.clear_all()

    def test_show_rentals(self):
        '''Test show_available_products function'''
        LOGGER.info('dropping db tables')
        database.clear_all()
        LOGGER.info('importing data test_show_rentals')
        database.import_data(PATH, 'data/products.csv', 'data/customers.csv',
                             'data/rentals.csv')
        expected_1 = {'c1': {'firstname': 'Susan', 'lastname': 'Anderson',
                             'address': '1 A Ave Davis CA 95630',
                             'phone_number': '9161234567',
                             'email': 'emaila@gmail.com'}}
        dict_test_1 = database.show_rentals('p2')
        self.assertEqual(expected_1, dict_test_1)
        LOGGER.info('dropping db tables')
        database.clear_all()
