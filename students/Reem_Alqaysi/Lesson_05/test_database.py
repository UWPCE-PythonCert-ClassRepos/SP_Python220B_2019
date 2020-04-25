"""
Module for testing database.py function.
"""
from unittest import TestCase
from database import import_data, show_available_products, show_rentals

class TestDataBase(TestCase):

    def test_import_data_good(self):
        # Test import data Function
        results = import_data('input_csv', 'products.csv', 'customer.csv', 'rentals.csv')
        self.assertEqual(results, ((4,4,4), (0,0,0)))

    def test_import_data_bad(self):
        #Test import function.
        results = import_data('input_wrong.csv', 'products_wrong.csv', 'customer1_wrong.csv', 'rentals_wrong.csv')
        self.assertEqual(results, ((0, 0, 0), (1, 1, 1)))

    def test_show_available_products(self):
        #list all avilable data in database
        import_data('input_csv', 'products.csv', 'customer.csv', 'rentals.csv')
        results = show_available_products()
        self.assertEqual(results, {'prd001': {'description': '60_inch_tv', 'product_type': 'Living_room', 'quantity_available': '1'},
                                   'prd002': {'description': 'sofa', 'product_type': 'Living_room', 'quantity_available': '1'},
                                   'prd003': {'description': 'Queen_bed', 'product_type': 'Bed_room', 'quantity_available': '2'},
                                   'prd004': {'description': 'Stove', 'product_type': 'Kitchen', 'quantity_available': '1'}})

    def test_show_rentals(self):
        #check a return information of customers that have rented a certain product
        import_data('input_csv', 'products.csv', 'customer.csv', 'rentals.csv')
        results = show_rentals('prd003')
        self.assertEqual(results, {'user001': {'name': 'Elisa Miles', 'address': '4490 Union Street',
                                              'phone_number': '206-922-0882', 'email': 'elisa.miles@yahoo.com'}})
