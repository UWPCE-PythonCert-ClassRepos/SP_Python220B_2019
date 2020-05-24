#!/usr/bin/env python3
"""Unit test for the HP Norton Furniture Consume APIs with NoSQL Assignment."""
# Created by Niels Skvarch

import unittest
import os
from parallel import import_data, clear_db


class TestCaseOne(unittest.TestCase):
    """Test the Import Data function from the database file."""
    def test_import_data(self):
        """Tests importing of data from csv files"""
        current_dir = os.getcwd()
        path = current_dir + r"\data_files"
        clear_db()
        import_test = import_data(path, "customer_data.csv", "product_data.csv")
        self.assertEqual((import_test[0][:3], import_test[1][:3]), ((1000, 0, 1000), (1000, 0, 1000)))


# main program name-space
if __name__ == "__main__":
    unittest.main()
