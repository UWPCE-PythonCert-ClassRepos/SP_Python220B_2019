#!/usr/bin/env python3

# Russell Felts
# Assignment 10 - Unit Tests

""" Unit tests """

# pylint: disable=no-self-use

from unittest import TestCase
import logging
import database

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class DatabaseUnitTest(TestCase):
    """ Unit tests for the database class """

    def test_get_timing_data(self):
        """ Unit test for the show_available_products function """
        database.drop_all_collections()
        database.import_data("../csv_files", "products.csv", "customers.csv", "rentals.csv")
        database.show_available_products()
        database.show_rentals("005")
        database.drop_all_collections()
