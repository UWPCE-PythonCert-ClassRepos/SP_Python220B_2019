"""
Module to test HP Norton MongoDB.
"""

# pylint:disable=line-too-long

from unittest import TestCase
import database

class TestDatabase(TestCase):
    """Tests functionality of MongoDB in database module."""

    #def test_read_data(self):
        #"""Tests data will be read from csv into list of dictionaries."""

    def test_read_data(self):
        """Tests if csv input files will be formatted correctly to list of dictionaries."""

        csv_file = 'data/customers.csv'
        new_data = database.read_data(csv_file)

        expected = [{'user_id': '37431', 'name': 'Bill Gates', 'address': '500 5th Ave, Seattle, WA',
                     'phone_number': '206-709-3100', 'email': 'bgates@microsoft.com'},
                    {'user_id': '18720', 'name': 'Steve Ballmer', 'address': '123 Bel Air Road Los Angeles, CA',
                     'phone_number': '425-882-8080', 'email': 'sballmer@microsoft.com'},
                    {'user_id': '700459', 'name': 'Elliot Alderson', 'address': '135 East 57th Street, New York, NY',
                     'phone_number': '212-867-5309', 'email': 'alderson@ecorp.com'}
                    ]
        self.assertEqual(new_data, expected)

    def test_import_data(self):
        """Tests data will be imported correctly,
        setting up database tables with proper formats."""

        # Setup
        e_1 = (3, 3, 3), (0, 0, 0)
        e_2 = (0, 0, 0), (1, 1, 1)

        directory = 'data'
        product_file = 'products.csv'
        customer_file = 'customers.csv'
        rental_file = 'rentals.csv'

        norton_db = database.import_data(directory, product_file,
                                         customer_file, rental_file)
        bad_input = database.import_data(directory, 'my_products.csv',
                                         'new_customers.csv', 'rental.csv')

        self.assertEqual(norton_db, e_1)
        self.assertEqual(bad_input, e_2)

    def test_show_available_products(self):
        """Tests if correct dictionary of available products will be returned."""

        #database.import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
        available_products = database.show_available_products()

        expected = {'742': {'description': 'chair',
                            'product_type': 'office',
                            'quantity_available': '4'},
                    '230': {'description': 'sofa',
                            'product_type': 'livingroom',
                            'quantity_available': '2'},
                    '1005': {'description': 'espressomachine',
                             'product_type': 'kitchen',
                             'quantity_available': '3'}
                    }

        self.assertEqual(expected, available_products)

    def test_show_rentals(self):
        """Tests if dictionary of rentals will be returned."""

        rentals_data = database.show_rentals()

        expected = {'37431': {'name': 'Bill Gates', 'address': '500 5th Ave, Seattle, WA',
                              'phone_number': '206-709-3100', 'email': 'bgates@microsoft.com'},
                    '18720': {'name': 'Steve Ballmer', 'address': '123 Bel Air Road Los Angeles, CA',
                              'phone_number': '425-882-8080', 'email': 'sballmer@microsoft.com'},
                    '700459': {'name': 'Elliot Alderson', 'address': '135 East 57th Street, New York, NY',
                               'phone_number': '212-867-5309', 'email': 'alderson@ecorp.com'}
                    }

        self.assertEqual(rentals_data, expected)

    def test_clear_database(self):
        """Tests if all data will be removed from HP Norton database."""

        database.clear_database()

        test = database.show_rentals()
        expected = {}

        self.assertEqual(test, expected)
