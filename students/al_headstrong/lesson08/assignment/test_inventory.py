"""
Module for testing inventory module.
"""

from unittest import TestCase
import csv
import inventory


class InventoryTest(TestCase):
    """Class for testing inventory module."""

    def setUp(self):
        """Establish class data structures."""
        self.test_invoice_file = 'test_invoice.csv'
        self.test_furniture_list = ["Elisa Miles", "LR04", "Leather Sofa", "25"]
        self.test_single_list = ["Susan Wong", "LR04", "Leather Sofa", "25"]

    def test_add_furniture(self):
        """Test add_furniture function."""
        open(self.test_invoice_file, 'w').close()
        inventory.add_furniture(self.test_invoice_file, "Elisa Miles", "LR04", "Leather Sofa", 25)
        inventory.add_furniture(self.test_invoice_file, "Edward Data", "KT78", "Kitchen Table", 10)
        with open(self.test_invoice_file, 'r') as file:
            contents = csv.reader(file)
            check_row = next(contents)
        self.assertEqual(self.test_furniture_list, check_row)

    def test_single_customer(self):
        """Test single_customer function."""
        open(self.test_invoice_file, 'w').close()
        create_invoice = inventory.single_customer("Susan Wong", self.test_invoice_file)
        create_invoice("test_items.csv")
        with open(self.test_invoice_file, 'r') as file:
            contents = csv.reader(file)
            check_row = next(contents)
        self.assertEqual(self.test_single_list, check_row)
