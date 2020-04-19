"""
test_database.py
Assignment 9
Joli Umetsu
PY220
"""
from unittest import TestCase
from database import import_data, show_available_products, show_rentals, clear_collections


class TestDatabase(TestCase):
    """ Unit tests for database functions """

    def test_import_data(self):
        """ Tests function to import data """
        clear_collections()
        prod_file = "files/products.csv"
        cust_file = "files/customers.csv"
        rent_file = "files/rentals.csv"
        records, errors = import_data(prod_file, cust_file, rent_file)

        self.assertEqual(records, (7, 4, 6))
        self.assertEqual(errors, (0, 0, 0))


    def test_show_available_products(self):
        """ Tests function to show available product data """
        expected = {"prd001": {"desc": "60-inch TV stand", "prod_type": "livingroom", \
                    "qty_avail": "3"}, "prd002": {"desc": "L-shaped sofa",  "prod_type": \
                    "livingroom", "qty_avail": "1"}, "prd003": {"desc": "Bar stool", \
                    "prod_type": "kitchen", "qty_avail": "10"}, "prd004": {"desc": \
                    "Bed frame", "prod_type": "bedroom", "qty_avail": "3"}, "prd005": \
                    {"desc": "Desk", "prod_type": "bedroom", "qty_avail": "5"}}
        self.assertEqual(expected, show_available_products())


    def test_show_rentals(self):
        """ Tests function to show renter info """
        expected = {"user003": {"name": "John Doe", "address": "4532 2nd Ave", "phone": \
                    "206-415-5241", "email": "johndoe@gmail.com"}, "user004": {"name": \
                    "Jane Young", "address": "3234 Belmont Ave", "phone": "206-245-4511", \
                    "email": "jane.young@gmail.com"}}
        self.assertEqual(expected, show_rentals("prd007"))
