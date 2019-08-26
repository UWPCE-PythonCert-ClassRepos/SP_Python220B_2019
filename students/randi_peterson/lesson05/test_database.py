"""This module tests database.py"""

from unittest import TestCase
import database


class TestDatabase(TestCase):
    """This class holds the tests for database.py"""

    def test_clear_database(self):
        """This tests that the database is cleared """

        database.clear_database()
        real = database.show_available_products()
        expected = {}
        self.assertEqual(real, expected)

    def test_create_dict_from_csv(self):
        """Tests creation of dict from csv file"""

        real_dict = database.create_dict_from_csv('test_files/test_test.csv')
        expected_dict = [{'user_id': '543', 'name': 'Bob Builder', 'address': 'Bricktown',
                         'phone_number': '7594930584', 'email': 'buildit@bricks.com'},
        {'user_id': '65', 'name': 'Walter White', 'address': 'New Mexico', 'phone_number':
            '7503850854', 'email': 'babyblue@ww.com'}, {'user_id': '345', 'name': 'Russell Wilson',
                                                        'address': 'Seattle', 'phone_number':
                                                                    '1234567890', 'email':
                                                                    'seattleqb@seahawks.com'}]
        self.assertEqual(real_dict, expected_dict)

    def test_import_data(self):
        """Tests the function for importing data"""

        database.clear_database()
        real = database.import_data('', 'test_files/products_test.csv',
                                    'test_files/customers_test.csv', 'test_files/rentals_test.csv')
        expected = (4, 5, 4), (0, 0, 0)
        self.assertEqual(real, expected)

        real_negative = database.import_data('', 'test_files/madeup.csv',
                         'test_files/doesntexist.csv', 'test_files/fakefile.csv')
        expected_negative = (0, 0, 0), (1, 1, 1)
        self.assertEqual(real_negative, expected_negative)


    def test_show_available_products(self):
        """Tests displaying available products"""
        database.clear_database()
        database.import_data('', 'test_files/products_test.csv',
                                    'test_files/customers_test.csv', 'test_files/rentals_test.csv')
        real = database.show_available_products()
        expected = {'Couch': {'description': 'You sit on it', 'product_type': 'living room', 'quantity_available': '1'}, 'Desk': {'description': 'You do work at it', 'product_type': 'bedroom', 'quantity_available': '4'} , 'TV': {'description': 'You watch it', 'product_type': 'den', 'quantity_available': '3'}, 'Table': {'description': 'You eat at it', 'product_type': 'dining room',
                   'quantity_available': '2'}}
        self.assertEqual(real, expected)

    def test_show_rentals(self):
        """Tests displaying rentals of certain product ID"""
        database.clear_database()
        database.import_data('', 'test_files/products_test.csv',
                             'test_files/customers_test.csv', 'test_files/rentals_test.csv')

        real = database.show_rentals('Couch')
        expected = {'123': {'name': 'Luke Skywalker', 'address': 'Tattooine', 'phone': '1234567890', 'email': 'moonwalk@jedi.com'}, '234': {'name': 'Sherlock Holmes', 'address': 'London', 'phone': '9857493647', 'email': 'clues@221b.com'}}
        self.assertEqual(real, expected)