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

EXPECTED_PRODUCT_DICT = {
    "V0032-100":{
        'product_id':"V0032-100", 
        'descriptin':"Spice Harvester", 
        'market_price':50000000.00, 
        'rental_price':3000.00, 
        'brand':"Spice World", 
        'voltage': '1kV'
    },
    "T0072-401":{
        'product_id':"T0072-401", 
        'description':"Thumper", 
        'market_price':2000.00, 
        'rental_price':49.95, 
        'brand':"Sandy Tools", 
        'voltage':12, 
    },
    "F1001-223":{
        'product_id':"F1001-223", 
        'description':"Harkonnen Chair", 
        'market_price':820.00, 
        'rental_price':12.40,
        'material':"bone", 
        'size':"large"
    },
    "F1001-052":{
        'product_id':"F1001-052", 
        'descriptinon':"Chair dog",  
        'market_price':4000.00, 
        'rental_price':70.00, 
        'material':"bio", 
        'size':"medium"
    }
}

class GeneratorTests(TestCase):
    """ Tests for MongoDB database functions """
    def setUp(self):
        """ Database Setup """
        pass
    def tearDown(self):
        """ Database teardown """
        pass

    def test_error_counter(self):
        """ Test the generator error_counter """
        # Given
        err = db.error_counter()

        # When
        next(err)
        next(err)
        next(err)

        # Then
        self.assertEqual(3, next(err))

    def test_error_counter_for_multiple_errors(self):
        """ Test the generator error_counter for multiple errors """
        # Given
        err1 = db.error_counter()
        err2 = db.error_counter()
        err3 = db.error_counter()

        # When
        for i in range(0,50):
            next(err1)
        for i in range(0,300):
            next(err2)
        for i in range(0,7000):
            next(err3)

        # Then
        self.assertEqual(50, next(err1))
        self.assertEqual(300, next(err2))
        self.assertEqual(7000, next(err3))
    
class ImportFilesTests(TestCase):
    """ Tests the functions responsible for importing data files (CSVs)"""
    def setUp(self):
        """ Set-up prior to running test"""
        pass
    def tearDown(self):
        """ Teardown after each test"""
        pass
    def test_import_product_csv(self):
        """Test the _import_product_csv function"""
        # Given
        directory_name = "csv_files"
        product_file = "products.csv"

        # When

        # Then
        result_dict = db.import_product_csv(directory_name, product_file)

        self.assertDictEqual(EXPECTED_PRODUCT_DICT, result_dict)

class ParserTests(TestCase):
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


class DatabaseTest(TestCase):
    """ Tests for MongoDB database functions """
    def setUp(self):
        """ Database Setup """
        pass
    def tearDown(self):
        """ Database teardown """
        pass
    def test_import_data_should_increment_error_count_for_bad_product_file(self):
        """ Tests the import_data function when bad product_file is given """
        # Given
        directory_name = './'
        product_file = 'does_not_exist.csv'
        customer_file = 'also_dne.csv'
        rentals_file = 'still_also_dne.csv'

        # When 

        # Then
        # with self.assertRaises(IOError):
        #     db.import_data(directory_name, product_file, customer_file, rentals_file)
