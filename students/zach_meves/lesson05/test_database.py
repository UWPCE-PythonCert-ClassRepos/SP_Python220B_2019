"""
Tests for database.py.
"""

import unittest
import pymongo
import os
import csv
import database

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(TEST_DIR, 'data')

# Test CSV files
CUSTOMERS = os.path.join(DATA_DIR, 'customers.csv')
PRODUCTS = os.path.join(DATA_DIR, 'products.csv')
RENTALS = os.path.join(DATA_DIR, 'rentals.csv')

# Test CSV field names
USER_ID, USER_NAME = "user_id", "name"
USER_ADDRESS, USER_EMAIL = "address", "email"
USER_PHONE = "phone_number"

PROD_ID, PROD_DESC = "product_id", "description"
PROD_TYPE, PROD_QTY = "product_type", "quantity"

RENT_QTY = "quantity_rented"


class TestCsvIO(unittest.TestCase):
    """Test reading/writing of CSV files"""

    def setUp(self) -> None:
        """Set up test case"""

        self.header = ('A', 'b', 'Cd')
        self.entries = ((1, 'a', 'd'),
                        (2, 'b', 'e'),
                        (3, 'c', 'f'))

        self.data_list = [dict(zip(self.header, entry)) for entry in self.entries]
        self.data_dict = dict(zip((entry[0] for entry in self.entries), self.data_list))

        self.filename = "test_file.csv"

        # Export CSV
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.header)
            writer.writerows(self.entries)

    def test_read_list(self):
        """Test reading CSV with list output"""

        # Read the file and assert that the dictionary output
        # matches self.data_list
        data = database.read_csv(self.filename)

        self.assertEqual(self.data_list, data)

    def test_read_dict(self):
        """Test reading CSV with dict output"""

        # Read the file and assert that the dictionary output
        # matches self.data_dict
        data = database.read_csv(self.filename, keyed=True)

        self.assertEqual(self.data_dict, data)

    def tearDown(self) -> None:
        """Remove test file"""

        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass


class TestDatabase(unittest.TestCase):
    """Test cases for database"""

    def setUp(self) -> None:
        """Set up test case"""

        # The read_csv method is tested above
        self.customer_data = database.read_csv(CUSTOMERS, keyed=True)
        self.product_data = database.read_csv(PRODUCTS, keyed=True)
        self.rental_data = database.read_csv(RENTALS, keyed=False)

        self.customer_keys = list(self.customer_data.keys())
        self.product_keys = list(self.product_data.keys())

        self.products_remaining = dict(zip(self.product_keys,
                                           (self.product_data[k][PROD_QTY] for
                                            k in self.product_keys)))

        for rental in self.rental_data:  # Subtract rented quantities from stock
            prod, qty = rental[PROD_ID], rental[RENT_QTY]
            self.products_remaining[prod] = self.products_remaining[prod] - qty

        self.client = pymongo.MongoClient()

    def test_import_data(self):
        """Test database.import_data"""

        pass

    def test_show_available_products(self):
        """Test database.show_available_products"""

        pass

    def test_show_rentals(self):
        """Test database.show_rentals"""

    pass
