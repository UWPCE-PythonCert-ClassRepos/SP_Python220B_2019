'''tests for database.py'''
import logging
from unittest import TestCase
from linear import import_data, drop_dbs, main

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
        LOGGER.info('Testing import_data return')
        self.assertEqual(data[0], (900, 900))
        self.assertEqual(data[1], (0, 0))
        self.assertEqual(data[2], (900, 900, 900))
        LOGGER.info('test FileNotFoundError')
        self.assertEqual(data[4], (2, 2, 1))
        LOGGER.info('import_data returns successful')
        drop_dbs()

    def test_import_data_product_file_not_found(self):
        '''testing file not found error for product file'''
        LOGGER.info('Testing import_data product_file_not_found')
        import_data('csv_files',
                    'prod_file.csv',
                    'customer_file.csv',
                    'rentals_file.csv')
        self.assertRaises(FileNotFoundError)
        drop_dbs()

    def test_import_data_customer_file_not_found(self):
        '''testing file not found error for customer file'''
        LOGGER.info('Testing import_data customer_file_not_found')
        import_data('csv_files',
                    'product_file.csv',
                    'cust_file.csv',
                    'rentals_file.csv')
        self.assertRaises(FileNotFoundError)
        drop_dbs()

    def test_import_data_rentals_file_not_found(self):
        '''testing file not found error for rentals file'''
        LOGGER.info('Testing import_data rentals_file_not_found')
        import_data('csv_files',
                    'product_file.csv',
                    'customer_file.csv',
                    'rent_file.csv')
        self.assertRaises(FileNotFoundError)
        drop_dbs()

    def test_main(self):
        '''testing main function'''
        LOGGER.info('Testing main()')
        expected = main()
        self.assertEqual(expected[0][0], 900)
        self.assertEqual(expected[0][1], 0)
        self.assertEqual(expected[0][2], 900)
        self.assertEqual(expected[1][0], 900)
        self.assertEqual(expected[1][1], 0)
        self.assertEqual(expected[1][2], 900)
        LOGGER.info('main() tests successful')


class TestsDatabase(TestCase):
    '''tests for database.py functions'''
    def setUp(self):
        '''importing csv files for tests'''
        LOGGER.info('importing csv files for drop_dbs')
        import_data('csv_files',
                    'product_file.csv',
                    'customer_file.csv',
                    'rentals_file.csv')
        LOGGER.info('csv files successfully imported')

    def test_drop_dbs(self):
        '''testing drop_dbs function'''
        dropped = drop_dbs()
        expected = 'Databases have been dropped'
        self.assertEqual(dropped, expected)
        LOGGER.info('drop_dbs successful')
