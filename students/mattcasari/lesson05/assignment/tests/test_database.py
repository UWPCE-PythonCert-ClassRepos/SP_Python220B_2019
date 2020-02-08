""" Unit tests for Lesson 05 MongoDB Operations"""

# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=broad-except

import logging
import io
from unittest import TestCase

from src import database as db


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("START: test_database")


class DatabaseTest(TestCase):
    """ Tests for MongoDB database functions """
    def setUp(self):
        """ Database Setup """
        pass
    def tearDown(self):
        """ Database teardown """
        pass

    def test_product_file_parser_with_valid_data(self):
        """ Test product_file_parser with valid data """
        # Given
        header_val = ['A', 'B', 'C', 'D']
        data_val = [1, 2, 3, 4]

        # When
        expected_data = {'A':1, 'B':2, 'C':3, 'D':4}
        
        # Then
        actual_data = db._product_file_parser(header_val, data_val)
        LOGGER.info(actual_data)
        self.assertEqual(expected_data, actual_data)

    def test_product_file_parser_fails_with_invalid_data(self):
        """ Test product_file_parser with invalid data """
        # Given
        header_val = ['X', 'Y', 'Z']
        data_val = [5, 6, 7, 8]

        # When

        # Then
        with self.assertRaises(IndexError):
            db._product_file_parser(header_val, data_val)

    def test_import_data_should_raise_exception_for_bad_product_file(self):
        """ Tests the import_data function when bad product_file is given """
        # Given
        directory_name = './'
        product_file = 'does_not_exist.csv'
        customer_file = 'also_dne.csv'
        rentals_file = 'still_also_dne.csv'

        # When 

        # Then
        with self.assertRaises(IOError):
            db.import_data(directory_name, product_file, customer_file, rentals_file)