"""UNIT TEST for database.py"""
from unittest import TestCase
from pymongo import MongoClient
from database import import_data, add_data, csv_convert
from database import show_available_products, show_rentals, drop_all
# pylint: disable=C0103

class TestDatabase(TestCase):
    """Unittest functions for testing database.py"""

    def test_import_data(self):
        """Test for import_data function from database.py"""
        client = MongoClient()
        db = client['database']
        self.assertEqual(((4, 4, 4), (0, 0, 0)),
                         import_data(db, '', 'products.csv', 'customers.csv',
                                     'rentals.csv'))
        drop_all(db)

    def test_add_data(self):
        """Test for add_data function from database.py"""
        client = MongoClient()
        db = client['database']
        product = db['product']
        customer = db['customer']
        rentals = db['rentals']
        self.assertEqual(0, add_data(product, 'products.csv'))
        self.assertEqual(0, add_data(customer, 'customers.csv'))
        self.assertEqual(0, add_data(rentals, 'rentals.csv'))
        self.assertEqual(['customer', 'rentals', 'product'], db.list_collection_names())
        drop_all(db)

    def test_csv_convert(self):
        """Test for csv_convert function from database.py"""
        self.assertEqual(4, len(csv_convert('products.csv')))
        test_result = csv_convert('products.csv')
        self.assertEqual('4451', test_result[2]['product_id'])
        self.assertTrue(next(item for item in test_result
                             if item['description'] == 'horse'))
        self.assertTrue(next(item for item in test_result
                             if item['description'] != 'pony'))

    def test_show_available_products(self):
        """Test for show_available_products function from database.py"""
        client = MongoClient()
        db = client['database']
        product = db['product']
        add_data(product, 'products.csv')
        self.assertEqual(3, len(show_available_products(db)))
        test_result = show_available_products(db)
        self.assertTrue('5564' in test_result)
        self.assertTrue('14445' not in test_result)
        drop_all(db)

    def test_show_rentals(self):
        """Test for show_rentals function from database.py"""
        client = MongoClient()
        db = client['database']
        customer = db['customer']
        rentals = db['rentals']
        add_data(customer, 'customers.csv')
        add_data(rentals, 'rentals.csv')
        test_result = show_rentals(db, '1234')
        self.assertTrue('user001' in test_result)
        test_result2 = show_rentals(db, '9567')
        self.assertTrue('user004' in test_result2)
        test_result3 = show_rentals(db, '0000')
        self.assertEqual(None, test_result3)
        drop_all(db)

    def test_drop_all(self):
        """Test for drop_all function from database.py"""
        client = MongoClient()
        db = client['database']
        product = db['product']
        customer = db['customer']
        rentals = db['rentals']
        add_data(product, 'products.csv')
        add_data(customer, 'customers.csv')
        add_data(rentals, 'rentals.csv')
        self.assertEqual(['customer', 'rentals', 'product'],
                         db.list_collection_names())
        drop_all(db)
        self.assertEqual([], db.list_collection_names())
