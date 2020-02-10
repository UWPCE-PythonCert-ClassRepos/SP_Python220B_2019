'''Contain module tests for database.py'''

from unittest import TestCase
from database import *


class DatabaseTests(TestCase):
    '''Contains all of the tests for HP Norton's MongoDB database.'''
    def test_import_data(self):
        '''Test the database.py import_data function.'''
        directory = 'testfiles'
        prod_file = 'prod_file.csv'
        cust_file = 'cust_file.csv'
        rental_file = 'rental_file.csv'
        counts = import_data(directory, prod_file, cust_file, rental_file)

        # One incomplete customer record added to customer file
        self.assertEqual(counts, ((3, 3, 4), (2, 1, 1)))

    def test_show_available_products(self):
        '''Test the database.py show_available_products function.'''
        products_available = show_available_products()
        expected_dict = {
            'prd001': {
                'description': 'chair',
                'product_type': 'livingroom',
                'quantity_available': '3'},
            'prd003': {
                'description': 'refrigerator',
                'product_type': 'kitchen',
                'quantity_available': '5'}
        }
        self.assertEqual(products_available, expected_dict)

    def test_show_rentals(self):
        '''Test the database.py show_rentals function.'''
        p1_rentals = show_rentals('prd001')
        p2_rentals = show_rentals('prd002')
        p3_rentals = show_rentals('prd003')

        self.assertEqual(p1_rentals, {
            'user002': {
                'name': 'homer simpson',
                'address': '123 springfield dr',
                'phone_number': '1112223334',
                'email': 'homers@gmail.com'
            }
        })

        self.assertEqual(p2_rentals, {
            'user002': {
                'name': 'homer simpson',
                'address': '123 springfield dr',
                'phone_number': '1112223334',
                'email': 'homers@gmail.com'
            }
        })

        self.assertEqual(p3_rentals, {
            'user001': {
                'name': 'jeff bezos',
                'address': '123 main st',
                'phone_number': '1234567890',
                'email': 'jeffb@gmail.com'
            },
            'user003': {
                'name': 'justin bieber',
                'address': '123 canada rd',
                'phone_number': '0987654321',
                'email': 'justinb@gmail.com'
            }
        })
