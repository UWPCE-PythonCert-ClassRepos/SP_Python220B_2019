# test_database.py
""" This module defines all the test functions for database.py """
from unittest import TestCase
import database as db


class database_Tests(TestCase):
    """ This class defines unit test fuctions for database.py """
    def setUp(self):
        self.csv_file = 'csv_files_dr'
        self.product_file = 'products.csv'
        self.product_failure_file = 'failure_file'
        self.customer_file = 'customers.csv'
        self.rental_file = 'rentals.csv'

    def test_import_data(self):
        """ Test import_data() function """
        db.LOGGER.info('--- Start Test import_data() ---')
        actual_res = db.import_data(self.csv_file, self.product_file,
                                    self.customer_file, self.rental_file)
        client = db.MongoDBConnection()
        with client:
            hp_norton_db = client.connection.rental
            products = hp_norton_db['products']
            customers = hp_norton_db['customers']
            rentals = hp_norton_db['rentals']
            self.assertEqual(products.count(), 5)
            self.assertEqual(customers.count(), 5)
            self.assertEqual(rentals.count(), 9)
        expect_res = [(5, 5, 9), (0, 0, 0)]
        self.assertEqual(actual_res, expect_res)
        db.LOGGER.info('--- End Test import_data() ---')

    def test_import_data_failure(self):
        """ Test import_data() function """
        db.LOGGER.info('--- Start Test failure import_data() ---')
        actual_res = db.import_data(self.csv_file, self.product_failure_file,
                                    self.customer_file, self.rental_file)
        expect_res = [(0, 5, 9), (1, 0, 0)]
        self.assertEqual(actual_res, expect_res)
        db.LOGGER.info('--- End Test failure import_data() ---')

    def test_show_available_products(self):
        """ Test show_available_products() function """
        db.LOGGER.info('--- Start Test show_available_products() ---')
        db.import_data(self.csv_file, self.product_file,
                       self.customer_file, self.rental_file)
        the_dict = db.show_available_products()
        expect_dict = {'prd001': {'description': '60-inch TV stand',
                                  'product_type': 'livingroom',
                                  'quantity_available': '3'},
                       'prd002': {'description': 'L-shaped sofa',
                                  'product_type': 'livingroom',
                                  'quantity_available': '1'},
                       'prd004': {'description': 'microwave oven',
                                  'product_type': 'kitchen',
                                  'quantity_available': '2'},
                       'prd005': {'description': 'queen size bed',
                                  'product_type': 'bedroom',
                                  'quantity_available': '3'}}
        self.assertEqual(expect_dict, the_dict)
        for key, val in the_dict.items():
            db.LOGGER.info(f"-- \'{key}\': {val}")
        db.LOGGER.info('--- End Test show_available_products() ---')

    def test_show_rentals(self):
        """ Test show_rentals() function """
        db.LOGGER.info('--- Start Test show_rentals() ---')
        db.import_data(self.csv_file, self.product_file,
                       self.customer_file, self.rental_file)
        the_dict = db.show_rentals('prd001')
        expect_dict = {'user002': {'name': 'Maya Data',
                                   'address': '4936 Elliot Avenue',
                                   'phone_number': '206-777-1927',
                                   'email': 'mdata@uw.edu'},
                       'user003': {'name': 'Alen King',
                                   'address': '1234 Main Street',
                                   'phone_number': '425-889-1200',
                                   'email': 'kinga@hotmail.com'}}
        self.assertEqual(expect_dict, the_dict)
        db.LOGGER.info(f'The customers info for renting product: prd001')
        for key, val in the_dict.items():
            db.LOGGER.info(f"-- \'{key}\': {val}")
        db.LOGGER.info('--- End Test show_rentals() ---')
