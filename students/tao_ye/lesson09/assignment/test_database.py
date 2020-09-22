"""
    Test module for Mongo database using unittest package
"""
from unittest import TestCase
from unittest.mock import patch
import io
import database as db

DATABASE = "norton_furniture"
CUSTOMER_COLLECTION_1 = "customer1"


class MongoDBTests(TestCase):
    """ unittest class to define all tests """
    def setUp(self):
        """ populate the database with data before each test """
        db.import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')

    def tearDown(self):
        """ empty database after each test """
        db.drop_database(DATABASE)

    def test_import_data_exception(self):
        """ test import_data function when exceptions occur"""
        result = db.import_data('data', 'product.csv', 'customer.csv', 'rental.csv')
        self.assertEqual(result, ((0, 0, 0), (1, 1, 1)))

    def test_show_available_products(self):
        """ test show_available_products function """
        result = db.show_available_products()
        self.assertEqual(result, {'prd001': {'description': '60-inch TV stand',
                                             'product_type': 'livingroom',
                                             'quantity_available': '3'},
                                  'prd002': {'description': 'L-shaped sofa',
                                             'product_type': 'livingroom',
                                             'quantity_available': '1'},
                                  'prd005': {'description': 'Nightstand',
                                             'product_type': 'bedroom',
                                             'quantity_available': '20'}})

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            db.drop_database(DATABASE)
            result = db.show_available_products()
            self.assertEqual(result, {})
            self.assertEqual(fake_stdout.getvalue().strip(), f'Database {DATABASE} not found.')

    def test_show_rentals(self):
        """ test show_rentals function """
        result = db.show_rentals("prd002")
        self.assertEqual(result, {'user001': {'name': 'Albert Einstein',
                                              'address': '7 Vine Drive, Cleveland, TN 37312',
                                              'phone_number': '559-555-0107',
                                              'email': 'albert.einstein@gmail.com'},
                                  'user004': {'name': 'Enrico Fermi',
                                              'address': '468 Wilson St., Solon, OH 44139',
                                              'phone_number': '567-555-0199',
                                              'email': 'enrico.fermi@gmail.com'},
                                  'user005': {'name': 'Jane Goodall',
                                              'address': '52 S. Summer St., Littleton, CO 80123',
                                              'phone_number': '970-555-0171',
                                              'email': 'jane.goodall@gmail.com'}})

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            db.drop_database(DATABASE)
            result = db.show_rentals("prd002")
            self.assertEqual(result, {})
            self.assertEqual(fake_stdout.getvalue().strip(), f'Database {DATABASE} not found.')

    def test_collection_exist(self):
        """ test collection_exist function """
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            db.collection_exist(DATABASE, CUSTOMER_COLLECTION_1)
            self.assertEqual(fake_stdout.getvalue().strip(),
                             f'Collection {CUSTOMER_COLLECTION_1} not found.')
