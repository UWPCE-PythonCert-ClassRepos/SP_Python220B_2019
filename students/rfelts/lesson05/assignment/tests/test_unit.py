#!/usr/bin/env python3

# Russell Felts
# Assignment 5 - Unit Tests

""" Unit tests """

from unittest import TestCase
import logging
import database

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class DatabaseUnitTest(TestCase):
    """ Unit tests for the database class """

    def test_import_data(self):
        """ Unit test for the import_data function """
        database.drop_all_collections()
        record_total, error_total = database.import_data("../csv_files",
                                                         "products.csv",
                                                         "customers.csv",
                                                         "rentals.csv")
        self.assertEqual((5, 4, 5), record_total)
        self.assertEqual((0, 0, 0), error_total)

    def test_import_data_errors(self):
        """ Unit test for the error count of the import_data function """
        database.drop_all_collections()
        record_total, error_total = database.import_data("csv_files",
                                                         "products.csv",
                                                         "customers.csv",
                                                         "rentals.csv")
        self.assertEqual((0, 0, 0), record_total)
        self.assertEqual((1, 1, 1), error_total)

    def test_show_available_products(self):
        """ Unit test for the show_available_products function """
        expected_result = {'001': {'available': '25',
                                   'description': 'Mafex Justice League Superman',
                                   'type': '6 inch Action Figure'},
                           '002': {'available': '12',
                                   'description': 'One 12 Justice League Tactical Suit Batman',
                                   'type': '6 inch Action Figure'},
                           '003': {'available': '1',
                                   'description': 'S.H. Figuarts Iron Man Mark LXXXV',
                                   'type': '6 inch Action Figure'},
                           '004': {'available': '15',
                                   'description': 'Black Series Stormtrooper',
                                   'type': '6 inch Action Figure'}}
        database.drop_all_collections()
        database.import_data("../csv_files", "products.csv", "customers.csv", "rentals.csv")
        self.assertDictEqual(expected_result, database.show_available_products())

    def test_show_rentals(self):
        """ Unit test for the show_rentals function """
        expected_result = {"001": {"id": "001", "first_name": "Bruce", "last_name": "Wayne",
                                   "address": "1007 Mountain Drive Gotham",
                                   "phone_number": "228-626-7699", "email": "b_wayne@gotham.net"},
                           "003": {"id": "003", "first_name": "Tony", "last_name": "Stark",
                                   "address": "10880 Malibu Point",
                                   "phone_number": "4766626769", "email": "tony@starkinc.com"}}
        database.drop_all_collections()
        database.import_data("../csv_files", "products.csv", "customers.csv", "rentals.csv")
        self.assertDictEqual(expected_result, database.show_rentals("005"))
