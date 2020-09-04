"""Basic Operation Unit Tests"""
import sys
sys.path.append('../')
from unittest import TestCase
import database


class DatabaseTest(TestCase):

    load_results = []

    def setUp(self):
        database.drop_collections()
        self.load_results = database.import_data('../data', 'products.csv', 'customers.csv', 'rentals.csv')

    def test_load_datafiles(self):
        expected_result = [(1000, 1000, 1000), (0, 0, 0)]
        self.assertEqual(expected_result, self.load_results)

    # def test_show_available_products(self):
    #     expected_result = {'prd001': {'description': '55 in LCD TV',
    #                                   'product_type': 'TV',
    #                                   'quantity_available': '2'},
    #                        'prd002': {'description': '35 in LDC TV',
    #                                   'product_type': 'TV',
    #                                   'quantity_available': '5'},
    #                        'prd003': {'description': 'Recliner',
    #                                   'product_type': 'Furniture',
    #                                   'quantity_available': '1'},
    #                        'prd004': {'description': 'End Table',
    #                                   'product_type': 'Furniture',
    #                                   'quantity_available': '2'}}
    #     actual_result = database.show_available_products()
    #     self.assertEqual(expected_result, actual_result)

    # def test_show_rentals(self):
    #     expected_result = {'cust001': {'name': 'Damien Lillard',
    #                                    'address': '523 Trailblazer Way',
    #                                    'phone_number': '3605551212',
    #                                    'email': 'dlillard@blazers.com'},
    #                        'cust002': {'name': 'C.J. McCollum',
    #                                    'address': '123 Point Guard Ln',
    #                                    'phone_number': '5035559876',
    #                                    'email': 'mccollum@blazers.com'}}
    #     actual_result = database.show_rentals('prd001')
    #     self.assertEqual(expected_result, actual_result)

