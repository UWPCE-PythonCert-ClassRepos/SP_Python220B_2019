"""
test_database.py
Assignment 5
Joli Umetsu
PY220
"""
from unittest import TestCase
import sys
sys.path.append('..')
from database import import_data, show_available_products, show_rentals, clear_collections


class TestDatabase(TestCase):
    """ Unit tests for database functions """

    def test_import_data(self):
        """ Tests function to import data """
        clear_collections()
        fdr = "files"
        prod_f = "products.csv"
        cust_f = "customers.csv"
        rent_f = "rentals.csv"
        records, errors = import_data(fdr, prod_f, cust_f, rent_f)

        self.assertEqual(records, (7, 4, 6))
        self.assertEqual(errors, (0, 0, 0))

    def test_show_available_products(self):
        """ Tests function to show available product data """
        expected = {"prd001": {"description": "60-inch TV stand", "product_type": "livingroom", \
                    "quantity_available": "3"}, "prd002": {"description": "L-shaped sofa", \
                    "product_type": "livingroom", "quantity_available": "1"}, "prd003": \
                    {"description": "Bar stool", "product_type": "kitchen", "quantity_available": \
                    "10"}, "prd004": {"description": "Bed frame", "product_type": "bedroom", \
                    "quantity_available": "3"}, "prd005": {"description": "Desk", "product_type": \
                    "bedroom", "quantity_available": "5"}}
        self.assertEqual(expected, show_available_products())

    def test_show_rentals(self):
        """ Tests function to show renter info """
        expected = {"user003": {"name": "John Doe", "address": "4532 2nd Ave", "phone_number": \
                    "206-415-5241", "email": "johndoe@gmail.com"}, "user004": {"name": \
                    "Jane Young", "address": "3234 Belmont Ave", "phone_number": "206-245-4511", \
                    "email": "jane.young@gmail.com"}}
        self.assertEqual(expected, show_rentals("prd007"))
