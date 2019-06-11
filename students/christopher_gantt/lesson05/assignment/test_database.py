'''tests for database.py'''
import logging
from unittest import TestCase
from database import import_data, show_available_products
from database import show_rentals, drop_dbs

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class TestsImportData(TestCase):
    '''tests for importing csv files using database.py'''
    def test_import_data(self):
        '''testing import_data function'''
        LOGGER.info('Testing import_data')
        data = import_data('csv_files',
                           'product_file.csv',
                           'customer_file.csv',
                           'rentals_file.csv')
        expected_data = ((4, 5, 5), (2, 2, 1))
        self.assertEqual(data, expected_data)

        LOGGER.info('test FileNotFoundError for Product File')
        data = import_data('csv_files',
                           'product.csv',
                           'customer_file.csv',
                           'rentals_file.csv')
        expected_data = ((0, 5, 5), (1, 2, 1))
        self.assertEqual(data, expected_data)

        LOGGER.info('test FileNotFoundError for Customer File')
        data = import_data('csv_files',
                           'product_file.csv',
                           'customer.csv',
                           'rentals_file.csv')
        expected_data = ((4, 0, 5), (2, 1, 1))
        self.assertEqual(data, expected_data)

        LOGGER.info('test FileNotFoundError for Rentals File')
        data = import_data('csv_files',
                           'product_file.csv',
                           'customer_file.csv',
                           'rentals.csv')
        expected_data = ((4, 5, 0), (2, 2, 1))
        self.assertEqual(data, expected_data)

        LOGGER.info('import_data tests passed')

class TestsDatabase(TestCase):
    '''tests for database.py functions'''
    def setUp(self):
        '''importing csv files for tests'''
        LOGGER.info('importing csv files for database function tests')
        import_data('csv_files',
                    'product_file.csv',
                    'customer_file.csv',
                    'rentals_file.csv')
        LOGGER.info('csv files successfully imported')

    def test_show_available_products(self):
        '''testing show_available_products function'''
        LOGGER.info('testing show_available_products function')
        my_dict = show_available_products()
        expected_dict = {'p123': {'description': 'Washer',
                                  'product_type': 'Laundry',
                                  'quantity_available': '5'},
                         'p456': {'description': 'Oven',
                                  'product_type': 'Kitchen',
                                  'quantity_available': '2'}}
        self.assertEqual(my_dict, expected_dict)
        LOGGER.info('show_available_products tests successful')

    def test_show_rentals(self):
        '''testing show_rentals function'''
        LOGGER.info('testing show_rentals function')
        my_dict = show_rentals('p123')
        expected_dict = {'c345': {'address': '',
                                  'email': '',
                                  'name': 'Fred Armisen',
                                  'phone_number': '2065647382'},
                         'c876': {'address': '9876 Imaginary Dr W.',
                                  'email': 'teager@gmail.com',
                                  'name': 'Tim Eager',
                                  'phone_number': '3609208765'},
                         'c987': {'address': '13462 Doesnexist St W.',
                                  'email': 'sjones@gmail.com',
                                  'name': 'Sam Jones',
                                  'phone_number': '4259876543'}}
        self.assertEqual(my_dict, expected_dict)
        LOGGER.info('show_rentals tests sucessful')

    def test_drop_dbs(self):
        '''testing drop_dbs function'''
        dropped = drop_dbs()
        expected = 'Databases have been dropped'
        self.assertEqual(dropped, expected)
