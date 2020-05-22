#!/usr/bin/env python3
"""Unit test for the HP Norton Furniture Consume APIs with NoSQL Assignment."""
# Created by Niels Skvarch

import unittest
import os
from database import import_data, show_available_products, show_rentals, clear_db


class TestCaseOne(unittest.TestCase):
    """Test the Import Data function from the database file."""
    def test_import_data(self):
        """Tests importing of data from csv files"""
        current_dir = os.getcwd()
        path = current_dir + r"\data_files"
        clear_db()
        import_test = import_data(path, "customer_data.csv", "product_data.csv", "rental_data.csv")
        self.assertEqual(list(import_test), [(8, 5, 11), (0, 0, 0)])

    def test_import_bad_data(self):
        """Test the import of bad or incomplete data."""
        current_dir = os.getcwd()
        path = current_dir + r"\data_files"
        clear_db()
        import_data(path, "bad_cust_data.csv", "bad_prod_data.csv", "bad_rent_data.csv")
        self.assertRaises(NameError)

    def test_import_no_files(self):
        """Test the import when files are not found."""
        current_dir = os.getcwd()
        path = current_dir + r"\data_files"
        clear_db()
        import_data(path, "cust_data.csv", "prod_data.csv", "rent_data.csv")
        self.assertRaises(FileNotFoundError)


class TestCaseTwo(unittest.TestCase):
    """Test the Show Available Products function from the database file"""
    def test_show_available_products(self):
        """Tests a database query to return a dictionary of products that
        have a quantity listed as greater than zero"""
        current_dir = os.getcwd()
        path = current_dir + r"\data_files"
        clear_db()
        import_data(path, "customer_data.csv", "product_data.csv", "rental_data.csv")

        expected_dict1 = {"2001": {"description": "stereo", "number_available": "6",
                                   "type": "electronics"},
                          "2002": {"description": "television", "number_available": "4",
                                   "type": "electronics"},
                          "2003": {"description": "microwave", "number_available": "2",
                                   "type": "appliance"},
                          "2004": {"description": "painting", "number_available": "11",
                                   "type": "decoration"},
                          "2005": {"description": "table_lamp", "number_available": "7",
                                   "type": "electronics"},
                          "2006": {"description": "end_table", "number_available": "3",
                                   "type": "furniture"},
                          "2007": {"description": "couch", "number_available": "1",
                                   "type": "furniture"}}

        available_test = show_available_products()
        self.assertEqual(available_test, expected_dict1)


class TestCaseThree(unittest.TestCase):
    """Test the Show Rentals function from the database file."""
    def test_show_rentals(self):
        """Tests a database query to return a dictionary of customers
         who have rented a certain product"""
        current_dir = os.getcwd()
        path = current_dir + r"\data_files"
        clear_db()
        import_data(path, "customer_data.csv", "product_data.csv", "rental_data.csv")

        expected_dict2 = {"1001": {"address": "35 Kentucky Rd",
                                   "email_address": "jim@beam.com",
                                   "name": "Jim Beam",
                                   "phone_number": "111-222-3333"},
                          "1004": {"address": "66934 Redmond Way",
                                   "email_address": "sasquatch@email.com",
                                   "name": "Harry Henderson",
                                   "phone_number": "444-555-6666"}}

        renters_test = show_rentals("2002")
        self.assertEqual(renters_test, expected_dict2)


# main program name-space
if __name__ == "__main__":
    unittest.main()
