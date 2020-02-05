# Advanced Programming In Python - Lesson 9 Assignment 1.2: Context Managers
# RedMine Issue - SchoolOps-15
# Code Poet: Anthony McKeever
# Start Date: 01/22/2019
# End Date: 01/23/2019

"""
Unit tests for Database.py
"""

from unittest import TestCase
from unittest import mock
from unittest.mock import patch
from unittest.mock import MagicMock

import pymongo
from pymongo.errors import DuplicateKeyError

import database as Database

# Disable linting that we don't care about for unit testing but might care
# about in other classes.

# pylint: disable=unused-argument
# pylint: disable=unnecessary-pass
# pylint: disable=no-self-use
# pylint: disable=too-few-public-methods


def mock_db_connection_success(*args, **kwargs):
    """
    Basic Mock Database connection for handling
    DuplicateKeyError and count mocking
    """
    class TestCollection():
        """ Mock Collection """
        @staticmethod
        def __init__(*args, **kwargs):
            pass

        def insert_one(self, *args, **kwargs):
            """
            Raise a DuplicateKeyError on call.
            """
            raise DuplicateKeyError("test")

        @staticmethod
        def count(*args, **kwargs):
            """
            Return a mock count of 1
            """
            return 1

        def __enter__(self, *args, **kwargs):
            return self

        def __exit__(self, *args, **kwargs):
            pass

    test_collection = TestCollection()
    return {"hp_norton": {"test": test_collection}}


class MockMongoDBConnection():
    """
    Mock Mongo DB Connection to simulate the real HP Norton DB
    """

    class MockProducts():
        """
        Mock Products Collection
        """
        def __init__(self, insert_fail=False):
            self.insert_fail = insert_fail
            self.products = [{"_id": "1",
                              "product_type": "abc",
                              "description": "abc",
                              "quantity_available": 2},
                             {"_id": "2",
                              "product_type": "efg",
                              "description": "xyz",
                              "quantity_available": 2}]

        def find(self, *args, **kwargs):
            """
            Mocks MongoDB Collection.Find method and retunrs list of products.
            """
            return self.products

        def insert_one(self, *args, **kwargs):
            """
            Mocks MongoDB Collection.insert_one
            """
            if self.insert_fail:
                raise DuplicateKeyError("test")

        def count(self):
            """
            Mocks MongoDB Collection.count
            """
            return 1

    class MockRentals():
        """
        Mock Rentals Collection
        """
        def __init__(self, insert_fail=False):
            self.insert_fail = insert_fail
            self.rentals = [{"_id": "1",
                             "customer_id": "a",
                             "product_id": "1"}]

        def find(self, *args, **kwargs):
            """
            Mocks MongoDB Collection.Find method and retunrs list of rentals.
            """
            return self.rentals

        def insert_one(self, *args, **kwargs):
            """
            Mocks MongoDB Collection.insert_one
            """
            if self.insert_fail:
                raise DuplicateKeyError("test")

        def count(self, with_limit_and_skip=False):
            """
            Mocks MongoDB Collection.count
            """
            return 1

    class MockCustomers():
        """
        Mock Customers Collection
        """
        def __init__(self, insert_fail=False):
            self.customer = {"_id": "a",
                             "name": "a",
                             "address": "123",
                             "phone": "abc",
                             "email_address": "1@abc.xyz"}
            self.insert_fail = insert_fail

        def find_one(self, *args, **kwargs):
            """
            Mocks MongoDB Collection.Find method and retunr a single customer.
            """
            return self.customer

        def insert_one(self, *args, **kwargs):
            """
            Mocks MongoDB Collection.insert_one
            """
            if self.insert_fail:
                raise DuplicateKeyError("test")

        def count(self):
            """
            Mocks MongoDB Collection.count
            """
            return 1

    class MockConnection():
        """
        Mock DB Connection setting collection.hp_norton as a dictionary.
        """
        def __init__(self, insert_fail=False):
            mock_product = MockMongoDBConnection.MockProducts(insert_fail)
            mock_rentals = MockMongoDBConnection.MockRentals(insert_fail)
            mock_customers = MockMongoDBConnection.MockCustomers(insert_fail)
            self.database = {"products": mock_product,
                             "rentals": mock_rentals,
                             "customers": mock_customers}

    def __init__(self, host='127.0.0.1', port=27017, insert_fail=False):
        self.connection = self.MockConnection(insert_fail)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockHpNorton(MockMongoDBConnection):
    """
    Mocks the HPNorton object inside database.py
    """
    def __init__(self):
        super().__init__()
        self.database = None

    def __enter__(self):
        mock_product = MockMongoDBConnection.MockProducts(False)
        mock_rentals = MockMongoDBConnection.MockRentals(False)
        mock_customers = MockMongoDBConnection.MockCustomers(False)
        self.database = {"products": mock_product,
                         "rentals": mock_rentals,
                         "customers": mock_customers}
        return self

    def get_collection(self, collection):
        """
        Mock HPNorton.get_collection.

        :collection:    The collection to get.
        """
        return self.database[collection]


class TestDatabase(TestCase):
    """
    Unit Tests for database.py
    """
    def setUp(self):
        """
        Set up the class, mocking the logger to silence it.
        """
        Database.LOGGER = MagicMock()

    def test_format_row_integers(self):
        """
        Validates that any row containing strings with integers converts that
        string type to an integer type
        """
        row = {"test_string": "three", "test_int": "3", "test_dec": "3.14"}
        row = Database.format_row_integers(row)

        self.assertEqual("three", row["test_string"])
        self.assertEqual(3, row["test_int"])
        self.assertEqual("3.14", row["test_dec"])

    def test_ingest_file_golden_path(self):
        """
        Validates ingesting files work without incident.
        """
        hold_connection = Database.MongoDBConnection
        Database.MongoDBConnection = MockMongoDBConnection
        contents = str("test1,test2,test3" +
                       "\nval1:1,val1:2,val1:3" +
                       "\nval2:1,val2:2,val2:3" +
                       "\nval3:1,val3:2,val3:3")
        open_mock = mock.mock_open(read_data=contents)
        mock_db = MockMongoDBConnection().MockConnection()

        with patch("builtins.open", open_mock):
            pymongo.database.Collection = MagicMock()
            pymongo.database.Collection.insert_one = MagicMock()

            ingest_val = Database.ingest_file(mock_db.database["products"],
                                              ".",
                                              "file")
            self.assertEqual(2, len(ingest_val))
            self.assertEqual(0, ingest_val[0])  # Validate no errors occured.

        Database.MongoDBConnection = hold_connection

    def test_ingest_file_duplicate_key(self):
        """
        Validates that a duplicate key error is handled correctly.
        """
        hold_connection = Database.MongoDBConnection
        Database.MongoDBConnection = MockMongoDBConnection

        contents = str("test1,test2,test3" +
                       "\ndup_key:1,val1:2,val1:3")
        open_mock = mock.mock_open(read_data=contents)
        mock_db = MockMongoDBConnection().MockConnection(insert_fail=True)

        with patch("builtins.open", open_mock):
            ingest_val = Database.ingest_file(mock_db.database["customers"],
                                              ".",
                                              "file")

            self.assertEqual(2, len(ingest_val))
            self.assertEqual(1, ingest_val[0])

        Database.MongoDBConnection = hold_connection

    def test_ingest_file_not_found(self):
        """
        Validates that a file not found erorr is handled correctly.
        """
        hold_connection = Database.MongoDBConnection
        Database.MongoDBConnection = MockMongoDBConnection
        open_mock = mock.mock_open()
        open_mock.side_effect = [FileNotFoundError("test")]

        mock_db = MockMongoDBConnection().MockConnection()

        with patch("builtins.open", open_mock):
            ingest_val = Database.ingest_file(mock_db.database["rentals"],
                                              ".",
                                              "file")

            self.assertEqual(2, len(ingest_val))
            self.assertEqual(1, ingest_val[0])

        Database.MongoDBConnection = hold_connection

    def test_import_data(self):
        """
        Validates that import data reports failures and successes accurately
        """
        with patch("database.ingest_file") as ingest_mock:
            ingest_mock.return_value = ((1, 2, 3), (4, 5, 6))
            values = Database.import_data(".", ".", ".", ".")

            self.assertEqual(3, len(values[0]))
            self.assertEqual(3, len(values[1]))

    def test_show_available_products(self):
        """
        Validates that show_available_products returns the expected dictionary
        """
        hold_connection = Database.MongoDBConnection
        hold_hp = Database.HPNorton

        Database.MongoDBConnection = MockMongoDBConnection
        Database.HPNorton = MockHpNorton

        products = Database.show_available_products()
        expected_products = MockMongoDBConnection.MockProducts().products

        for product in expected_products:
            prod_id = product["_id"]
            db_product = products.get(prod_id)

            self.assertIsNotNone(db_product, f"ProdID: {products}")

            for key, value in product.items():
                if key == "_id":
                    continue

                self.assertEqual(value, db_product[key])

        Database.MongoDBConnection = hold_connection
        Database.HPNorton = hold_hp

    def test_show_rentals(self):
        """
        Validates that show_rentals returns the expected dictionary
        """
        hold_connection = Database.MongoDBConnection
        hold_hp = Database.HPNorton

        Database.MongoDBConnection = MockMongoDBConnection
        Database.HPNorton = MockHpNorton

        rentals = Database.show_rentals("1")
        self.assertEqual(len(rentals), 1)

        customer = MockMongoDBConnection.MockCustomers().customer
        rental_cust = rentals.get(customer["_id"])
        self.assertIsNotNone(rental_cust)

        for key, value in customer.items():
            if key == "_id":
                continue

            self.assertEqual(value, rental_cust[key])

        Database.MongoDBConnection = hold_connection
        Database.HPNorton = hold_hp
