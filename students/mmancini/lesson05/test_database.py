'''
    test suite for mongoDB
'''

import logging
from unittest import TestCase
from database import import_data, show_available_products
from database import show_rentals

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
        ''' import data files '''
        LOGGER.info('setup start')
        LOGGER.info('setup import data file to database')
        import_data('csv_files',
                    'product_file.csv',
                    'customer_file.csv',
                    'rentals_file.csv')
        LOGGER.info('setup end')

    def test_show_available_products(self):
        pass
    
    def test_show_rentals(self):
        pass
