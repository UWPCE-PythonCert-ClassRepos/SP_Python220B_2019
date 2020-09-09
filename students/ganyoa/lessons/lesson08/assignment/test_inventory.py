"""
Unittest for Inventory module.
"""

import unittest
import os
from inventory import *


class TestIventory(unittest.TestCase):
    """Class to test inventory module."""

    #delete csv test file if present
    try:
        os.remove("rented_items_test.csv")
    except FileNotFoundError:
        pass


    def test_add_furniture(self):
        """test add furniture"""

        add_furniture("rented_items_test.csv", "Test Miles", "LR04", "Leather Sofa", 25)
        add_furniture("rented_items_test.csv", "Test Data", "KT78", "Kitchen Table", 10)
        add_furniture("rented_items_test.csv", "Test Gonzales", "BR02", "Queen Mattress", 17)

        with open("rented_items_test.csv", 'r') as inv_file:
            csv_data = [row for row in csv.reader(inv_file.read().splitlines())]

        self.assertEqual(csv_data[0][0], 'Test Miles')
        self.assertEqual(csv_data[2][1], 'BR02')


    def test_single_customer(self):
        """test coverage in single_customer"""

        create_inv_test = single_customer("Test Wong", "rented_items_test.csv")
        create_inv_test("test_items.csv")

        with open("rented_items_test.csv", 'r') as inv_file:
            csv_data = [row for row in csv.reader(inv_file.read().splitlines())]

        self.assertEqual(csv_data[3][0], 'Test Wong')
        self.assertEqual(csv_data[4][2], 'Kitchen Table')

