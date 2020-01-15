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

CUSTOMERS = os.path.join(DATA_DIR, 'customers.csv')
PRODUCTS = os.path.join(DATA_DIR, 'products.csv')
RENTALS = os.path.join(DATA_DIR, 'rentals.csv')


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
        self.customer_data = database.read_csv(CUSTOMERS)
        self.product_data = database.read_csv(PRODUCTS)
        self.rental_data = database.read_csv(RENTALS)



