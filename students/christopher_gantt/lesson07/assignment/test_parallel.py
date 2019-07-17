'''test_parallel'''
import logging
from unittest import TestCase
from parallel import import_product_file, import_customer_file
from parallel import import_rentals_file, drop_dbs, main

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class TestsImportData(TestCase):
    '''tests for importing csv files using database.py'''
    def test_import_product_file(self):
        '''testing product file import'''
        products_import = import_product_file()
        self.assertEqual(products_import[0], 900)
        self.assertEqual(products_import[1], 0)
        self.assertEqual(products_import[2], 900)
        drop_dbs()

    def test_import_customer_file(self):
        '''testing customer file import'''
        customers_import = import_customer_file()
        self.assertEqual(customers_import[0], 900)
        self.assertEqual(customers_import[1], 0)
        self.assertEqual(customers_import[2], 900)
        drop_dbs()

    def test_import_rentals_file(self):
        '''tests import rental file function'''
        rentals_import = import_rentals_file()
        self.assertEqual(rentals_import[0], 900)
        self.assertEqual(rentals_import[1], 1)
        drop_dbs()

    def test_drop_dbs(self):
        '''tests drop dbs function'''
        returns = drop_dbs()
        self.assertEqual(returns, 'Databases have been dropped')

    def test_main(self):
        '''tests main function'''
        returns = main()
        self.assertTrue(returns)
        self.assertEqual(returns[0][0], 900)
        self.assertEqual(returns[0][1], 0)
        self.assertEqual(returns[0][2], 900)
        self.assertEqual(returns[1][0], 900)
        self.assertEqual(returns[1][1], 0)
        self.assertEqual(returns[1][2], 900)
        drop_dbs()
