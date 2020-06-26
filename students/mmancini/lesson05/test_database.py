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
        data = import_data('csv_files',
                           'product_file.csv',
                           'customer_file.csv',
                           'rentals_file.csv')

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
        ''' test show available products '''
        pass

    def test_show_rentals(self):
        ''' test show rentals '''
        pass
