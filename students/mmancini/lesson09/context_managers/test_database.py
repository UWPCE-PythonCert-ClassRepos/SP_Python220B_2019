'''
    test suite for mongoDB
'''

#pylint: disable=too-many-statements
#pylint: disable=invalid-name
#pylint: disable=too-many-locals
#pylint: disable=no-self-use
#pylint: disable=unnecessary-pass
#pylint: disable=pointless-string-statement

import logging
from unittest import TestCase
from database import import_data, show_available_products
from database import show_rentals, dbs_cleanup

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class TestImportDataToDb(TestCase):
    '''test import data files to db'''
    def test_import_data(self):
        '''test importing data files'''
        LOGGER.info('Test import_data')
        result_count, result_errors = import_data('csv_files',
                                                  'product_file.csv',
                                                  'customer_file.csv',
                                                  'rentals_file.csv')
        LOGGER.info('test_import_data, result_count = %s, result_errors = %s',
                    str(result_count), str(result_errors))
        self.assertEqual(result_count, (6, 6, 6))
        self.assertEqual(result_errors, (0, 0, 0))

        # err check filenotfound
        result_count, result_errors = import_data('csv_files',
                                                  'product_file.csvXXX',
                                                  'customer_file.csvXXX',
                                                  'rentals_file.csvXXX')
        LOGGER.info('test_import_data, result_count = %s, result_errors = %s',
                    str(result_count), str(result_errors))
        self.assertEqual(result_count, (0, 0, 0))
        self.assertEqual(result_errors, (1, 1, 1))

        LOGGER.info('test_import_data completed')

class TestsDatabase(TestCase):
    ''' test suite database '''
    def setUp(self):
        ''' test setup '''
        LOGGER.info('setup start')

        dropped_status = dbs_cleanup()
        LOGGER.info('test setup, dbs cleanup status = %s', dropped_status)

        ''' import data files '''
        LOGGER.info('setup import data file to database')
        import_data('csv_files',
                    'product_file.csv',
                    'customer_file.csv',
                    'rentals_file.csv')

        LOGGER.info('test setup completed')

    def test_show_available_products(self):
        '''testing show_available_products function'''
        pass
        LOGGER.info('test show products with quantities available')
        result_dict = show_available_products()
        expected_dict = {'pid001': {'description': 'sofa',
                                    'product_type': 'livingroom',
                                    'quantity_available': '5'},
                         'pid002': {'description': 'washer',
                                    'product_type': 'laundry',
                                    'quantity_available': '4'},
                         'pid004': {'description': 'edger',
                                    'product_type': 'garage',
                                    'quantity_available': '2'},
                         'pid005': {'description': 'desk',
                                    'product_type': 'office',
                                    'quantity_available': '1'}}
        self.assertEqual(result_dict, expected_dict)
        LOGGER.info('available products are %s', result_dict)
        LOGGER.info('test show_available_products tests completed')


    def test_show_rentals(self):
        ''' test show rentals '''
        LOGGER.info('test start show_rentals')
        expected_data = {'cid001': {'name': 'JohnSmith', 'address': '111 Broad St.',
                                    'phone_number': '111-222-3333',
                                    'email': 'JohnSmith@gmail.com'},
                         'cid004': {'name': 'BettySims', 'address': '444 First St.',
                                    'phone_number': '444-555-6666',
                                    'email': 'BettySims@gmail.com'}}
        result_dict = show_rentals('pid001')
        self.assertEqual(result_dict, expected_data)
        LOGGER.info('test show_rentals customer who rented product %s, are %s',
                    'pid001', result_dict)
        LOGGER.info('test show_rentals completed')

        pass


    def test_dbs_cleanup(self):
        '''test drop dbs'''
        pass
        result_status = dbs_cleanup()
        expected_status = 'databases dropped'
        self.assertEqual(result_status, expected_status)
