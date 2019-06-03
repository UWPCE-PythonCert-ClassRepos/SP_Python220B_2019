#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 13:40:32 2019

@author: lauraannf
"""

from unittest import TestCase
from database_new import import_data, delete_database, show_available_products
from database_new import show_rentals

class TestDatabase(TestCase):
    """"test for database.py"""

    def test_import_data(self):
        """test import_data"""

        delete_database()
        test_import = import_data('csvfiles', 'inventory.csv', 'customers.csv',
                                  'rental.csv')
        self.assertEqual(test_import, ((4, 4, 4), (0, 0, 0)))
        delete_database()
        test_import = import_data('csvfiles', 'inventory1.csv', 'customers.csv',
                                  'rental.csv')
        self.assertEqual(test_import, ((0, 4, 4), (1, 0, 0)))
        delete_database()
        test_import = import_data('csvfiles', 'inventory.csv', 'customers1.csv',
                                  'rental.csv')
        self.assertEqual(test_import, ((4, 0, 4), (0, 1, 0)))
        delete_database()
        test_import = import_data('csvfiles', 'inventory.csv', 'customers.csv',
                                  'rental1.csv')
        self.assertEqual(test_import, ((4, 4, 0), (0, 0, 1)))

    def test_show_rentals(self):
        """test for show_rentals"""

        delete_database()
        import_data('csvfiles', 'inventory.csv', 'customers.csv',
                    'rental.csv')
        rental_dict = show_rentals('p00001')
        test_rental = {'customer_id': 'c00001',
                       'customer_name': 'Dorothy Zbornak',
                       'customer_address':
                       '6151 Richmond Street, Miami, FL, 33133',
                       'phone_number': '555-111-1111',
                       'email': 'd.zbornak@gmail.com',
                       'quantity': '1'}
        self.assertEqual(rental_dict['r00001'], test_rental)
        self.assertEqual(len(rental_dict), 2)

    def test_show_available_products(self):
        """rest for show_available_products"""
        delete_database()
        import_data('csvfiles', 'inventory.csv', 'customers.csv',
                    'rental.csv')
        product_dict = show_available_products()
        test_show = {'description': 'television',
                     'product_type': 'electronic',
                     'total_quantity': '5',
                     'available_quantity': 3}
        self.assertEqual(product_dict['p00001'], test_show)
