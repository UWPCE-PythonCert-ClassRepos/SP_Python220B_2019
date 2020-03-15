#!/usr/bin/env python3

"""
Tests for database.py
"""

# pylint: disable= C0301

from unittest import TestCase
import os
import database


class TestDatabase(TestCase):
    """
    Class for testing database functions
    """

    def test_import_data(self):
        """
        Test import_data function
        """
        cwd = os.getcwd()

        # Passing test
        added, errors = database.import_data(cwd, "products.csv", "customers.csv", "rentals.csv")
        self.assertEqual(added, (3, 3, 4))
        self.assertEqual(errors, (0, 0, 0))

        # Failing test
        add_tuple, error_tuple = database.import_data(cwd, "p.csv", "c.csv", "r.csv")
        self.assertEqual(add_tuple, (0, 0, 0))
        self.assertEqual(error_tuple, (1, 1, 1))

    def test_show_available_products(self):
        """
        Test show_available_products functions
        """
        cwd = os.getcwd()
        database.import_data(cwd, "products.csv", "customers.csv", "rentals.csv")

        products = {'pid582': {'description': 'basketball', 'product_type': 'sporting goods',
                               'quantity_available': '100'},
                    'pid629': {'description': 'air jordans', 'product_type': 'clothing', 'quantity_available': '6'},
                    'pid452': {'description': 'water bottle', 'product_type': 'sporting goods',
                               'quantity_available': '50'}}

        available_products = database.show_available_products()
        self.assertEqual(available_products, products)

    def test_show_rentals(self):
        """
        Test show_rentals function
        """
        cwd = os.getcwd()
        database.import_data(cwd, "products.csv", "customers.csv", "rentals.csv")

        users = {'user023': {'name': 'Michael Jordan', 'address': '123 Fake Street', 'phone_number': '847-247-5102',
                             'email': 'mj@gmail.com'},
                 'user033': {'name': 'Scottie Pippen', 'address': '321 Fake Lane', 'phone_number': '630-756-4710',
                             'email': 'pip@gmail.com'}}

        show_rentals = database.show_rentals("pid582")
        self.assertEqual(show_rentals, users)
