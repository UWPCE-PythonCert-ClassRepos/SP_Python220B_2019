""" Unit tests for Lesson 05 MongoDB Operations"""

# pylint: disable=protected-access

import logging
from unittest import TestCase, TestLoader

from src import database as db

TestLoader.sortTestMethodsUsing = None

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("START: test_database")
LOGGER.setLevel(logging.INFO)

EXPECTED_PRODUCT_DICT = [
    {
        "product_id": "V0032-100",
        "description": "Spice Harvester",
        "market_price": "50000000.00",
        "rental_price": "3000.00",
        "product_type": "Electric",
        "brand": "Spice World",
        "voltage": "1kV",
        "material": "",
        "size": "",
        "quantity_available": "2",
    },
    {
        "product_id": "T0072-401",
        "description": "Thumper",
        "market_price": "2000.00",
        "rental_price": "49.95",
        "product_type": "Electric",
        "brand": "Sandy Tools",
        "voltage": "12",
        "material": "",
        "size": "",
        "quantity_available": "100",
    },
    {
        "product_id": "F1001-223",
        "description": "Harkonnen Chair",
        "market_price": "820.00",
        "rental_price": "12.40",
        "product_type": "Furniture",
        "material": "bone",
        "size": "large",
        "brand": "",
        "voltage": "",
        "quantity_available": "23",
    },
    {
        "product_id": "F1001-052",
        "description": "Chair dog",
        "market_price": "4000.00",
        "rental_price": "70.00",
        "product_type": "Furniture",
        "material": "bio",
        "size": "medium",
        "brand": "",
        "voltage": "",
        "quantity_available": "14",
    },
]

EXPECTED_CUSTOMERS_DICT = [
    {
        "customer_id": "C1950991",
        "name": "Paul",
        "last_name": "Atreides",
        "address": "Arrakis",
        "phone_number": "888-778-6668",
        "email_address": "thewormisspice@dune.net",
        "status": "True",
        "credit_limit": "999999.99",
    }
]

EXPECTED_RENTALS_DICT = [
    {"product_id": "V0032-100", "customer_id": "C1955810", "rental_quantity": "2"}
]

class ParserTests(TestCase):
    """ Tests for MongoDB database functions """

    def setUp(self):
        """ Database Setup """

    def tearDown(self):
        """ Database teardown """

    def test_file_parser_with_valid_data(self):
        """ Test product_file_parser with valid data """
        # Given
        data = ["ID001", "Voice Modulator", "9999.99", "129.50"]
        headers = ["product_id", "description", "market_price", "rental_price"]
        # When
        expected_data = {
            "product_id": "ID001",
            "description": "Voice Modulator",
            "market_price": "9999.99",
            "rental_price": "129.50",
        }

        # Then
        actual_data = db._file_parser(data, headers)
        LOGGER.info(actual_data)
        self.assertEqual(expected_data, actual_data)

    def test_product_file_parser_fails_with_invalid_data(self):
        """ Test product_file_parser with invalid data """
        # Given
        data_val = [5, 6, 7, 8]
        # When

        # Then
        with self.assertRaises(IndexError):
            db._file_parser(data_val, "products")

    def test_validate_headers_should_pass(self):
        """ Test if headers provided are valid with _validate_headers method"""
        # Given
        headers = [
            "product_id",
            "description",
            "market_price",
            "rental_price",
            "material",
            "size",
            "brand",
            "voltage",
        ]

        # When
        result = db._validate_headers(headers, "products")

        # Then
        self.assertTrue(result)

    def test_validate_headers_has_bad_header_name(self):
        """ Test _validate_headers with a bad header value"""
        # Given
        headers = ["product_id", "description", "mkt_value", "rental_value"]
        # When

        # Then
        with self.assertRaises(ValueError):
            db._validate_headers(headers, "rentals")


class ImportFilesTests(TestCase):
    """ Tests the functions responsible for importing data files (CSVs)"""

    def setUp(self):
        """ Set-up prior to running test"""

    def tearDown(self):
        """ Teardown after each test"""

    def test_import_product_csv(self):
        """Test the _import_csv function for products"""
        # Given
        directory_name = "csv_files"
        product_file = "products"

        # When

        # Then
        error_cnt, result_dict = db.import_csv(directory_name, product_file)

        self.assertEqual(len(EXPECTED_PRODUCT_DICT), len(result_dict))
        self.assertDictEqual(EXPECTED_PRODUCT_DICT[0], result_dict[0])
        self.assertEqual(0, error_cnt)

    def test_import_customer_csv(self):
        """Test the _import_csv function for customers"""
        # Given
        directory_name = "csv_files"
        product_file = "customers"

        # When

        # Then
        [error_cnt, result_dict] = db.import_csv(directory_name, product_file)
        self.assertDictEqual(EXPECTED_CUSTOMERS_DICT[0], result_dict[0])
        self.assertEqual(0, error_cnt)

    def test_import_rental_csv(self):
        """Test the _import_csv function for rentalss"""
        # Given
        directory_name = "csv_files"
        product_file = "rentals"

        # When

        # Then
        [error_cnt, result_dict] = db.import_csv(directory_name, product_file)
        self.assertDictEqual(EXPECTED_RENTALS_DICT[0], result_dict[0])
        self.assertEqual(0, error_cnt)

class DatabaseTest(TestCase):
    """ Tests for MongoDB database functions """

    def setUp(self):
        """ Database Setup """

    def tearDown(self):
        """ Database teardown """
        db._drop_collections()

    def test_populate_database(self):
        """ Test the populate_database method"""
        # Given
        data = [
            {
                "customer_id": "ID001",
                "name": "Paul",
                "last_name": "Atreides",
                "address": "Arrakis",
                "phone_number": "888-778-6668",
                "email_address": "thewormisspice@dune.net",
                "status": "True",
                "credit_limit": "999999.99",
            }
        ]
        mongo = db.MongoDBConnection()
        with mongo:
            test_db = mongo.connection.test_db

            # When
            (r_cnt, e_cnt) = db.populate_database(test_db, "customers", data)

            customers = test_db.customers.find()
            # test_db.customers.customer_id.find()
            LOGGER.debug(customers)
            actual_id = customers[0]["customer_id"]
            LOGGER.debug(actual_id)

            # Then
            self.assertEqual(1, r_cnt)
            self.assertEqual(0, e_cnt)
            self.assertIn("ID001", actual_id)

            db._drop_collections(test_db)

    def test_import_data(self):
        """ Test the import_data method"""
        # Given
        product_file = "products"
        directory_name = "./csv_files"
        customer_file = "customers"
        rental_file = "rentals"

        # When
        [records, errors] = db.import_data(
            directory_name, product_file, customer_file, rental_file
        )

        # Then
        self.assertEqual(0, errors[0])
        self.assertEqual(0, errors[1])
        self.assertEqual(0, errors[2])

        self.assertEqual(4, records[0])
        self.assertEqual(4, records[1])
        self.assertEqual(5, records[2])
        db._drop_collections()


class CallsToDatabase(TestCase):
    """ Handles all tests involving calls to DB for data"""

    def setUp(self):
        """ Database Setup """
        product_file = "products"
        directory_name = "./csv_files"
        customer_file = "customers"
        rental_file = "rentals"
        db.import_data(directory_name, product_file, customer_file, rental_file)

    def tearDown(self):
        """ Database teardown """
        db._drop_collections()

    def test_show_available_products(self):
        """ Test the show_available_product data from database """

        # Given
        expected_result = {
            "V0032-100": {
                "description": "Spice Harvester",
                "product_type": "Electric",
                "quantity_available": "2",
            },
            "T0072-401": {
                "description": "Thumper",
                "product_type": "Electric",
                "quantity_available": "100",
            },
            "F1001-223": {
                "description": "Harkonnen Chair",
                "product_type": "Furniture",
                "quantity_available": "23",
            },
            "F1001-052": {
                "description": "Chair dog",
                "product_type": "Furniture",
                "quantity_available": "14",
            },
        }

        # When
        products = db.show_available_products()

        # Then
        self.assertDictEqual(expected_result, products)

    def test_show_rentals(self):
        """ Test the show_rentals method """
        # Given
        product_id = "V0032-100"

        # When
        expected_result = {
            "C1955810": {
                "name": "Atreides, LetoII",
                "address": "Arrakis",
                "phone_number": "899-123-5432",
                "email_address": "godemperor@dune.net",
            },
            "C3281830": {
                "name": "Corino, Irulan",
                "address": "Kaitain",
                "phone_number": "001-000-0002",
                "email_address": "princessofthepadishah@arrakis.com",
            },
        }

        # Then
        customers = db.show_rentals(product_id)
        LOGGER.debug(customers)
        self.assertDictEqual(expected_result, customers)
        db._drop_collections()
