"""
unit test for lesson05
"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name

import os
from unittest import TestCase
from database import import_data, show_available_products, show_rentals

DATA_FILE_PATH = os.getcwd()
DATA_FILE_CUSTOMER = 'customers.csv'
DATA_FILE_PRODUCT = 'products.csv'
DATA_FILE_RENTAL = 'rentals.csv'

class TestDatabase(TestCase):
    """ unit test for database.py """
    def test_import_data(self):
        """ test import_data """
        expected_record_count = (4, 3, 12)
        expected_error_count = (0, 0, 0)

        (tup_record_count, tup_error_count) = import_data(DATA_FILE_PATH,
                                                          DATA_FILE_PRODUCT,
                                                          DATA_FILE_CUSTOMER,
                                                          DATA_FILE_RENTAL)

        self.assertTupleEqual(tup_record_count, expected_record_count)
        self.assertTupleEqual(tup_error_count, expected_error_count)

    def test_import_data_error(self):
        """ test import_data """
        expected_record_count = (4, 0, 0)
        expected_error_count = (0, 1, 1)

        (tup_record_count, tup_error_count) = import_data(DATA_FILE_PATH,
                                                          'products.csv',
                                                          'customers_bad.csv',
                                                          'rentals_bad.csv')

        self.assertTupleEqual(tup_record_count, expected_record_count)
        self.assertTupleEqual(tup_error_count, expected_error_count)

    def test_show_available_product(self):
        """ test show_available_product """
        import_data(DATA_FILE_PATH, DATA_FILE_PRODUCT, DATA_FILE_CUSTOMER, DATA_FILE_RENTAL)

        expected_product_list = {'E0001': {'description': 'Television', 'product_type': 'electronics', 'quantity_available': 502},
                                 'F0001': {'description': 'Sofa', 'product_type': 'furniture', 'quantity_available': 398},
                                 'I0003': {'description': 'Computer', 'product_type': 'electronics', 'quantity_available': 19}}

        products_available = show_available_products()

        self.assertDictEqual(products_available['E0001'], expected_product_list['E0001'])

    def test_show_rentals(self):
        """ test show_rentals """
        import_data(DATA_FILE_PATH, DATA_FILE_PRODUCT, DATA_FILE_CUSTOMER, DATA_FILE_RENTAL)

        expected_users = {'U001': {'name': 'Steve Jobs', 'address': 'One Infinite Loop, Cupertino, CA 95014', 'phone_number': '800-275-2273', 'email': 'steve@apple.com'},
                          'U002': {'name': 'Bill Gates', 'address': '440 5th Ave N., Seattle, WA 98109440 5th Ave N., Seattle, WA 98109', 'phone_number': '206-709-3100 ext. 7100', 'email': 'bill.gates@gatesfoundation.org'},
                          'U003': {'name': 'Mark Zuckerberg', 'address': '1 Hacker Way, Menlo Park, California 94025', 'phone_number': None, 'email': 'mz@fb.com'}}

        users_F0001 = show_rentals('F0001')

        self.assertDictEqual(users_F0001['U002'], expected_users['U002'])
