"""
Module for testing inventory module.
"""

from unittest import TestCase
import inventory
import csv


class InventoryTest(TestCase):
    """Class for testing inventory module."""

    def setUp(self):
        """Establish class data structures."""
        self.test_invoice_file = 'test_invoice.csv'
        self.test_furniture_list = [["Elisa Miles", "LR04", "Leather Sofa", 25],
                                    ["Edward Data", "KT78", "Kitchen Table", 10]]
        self.test_single_list = [["Susan Wong", "LR04", "Leather Sofa", 25],
                                 ["Susan Wong", "KT78", "Kitchen Table", 10],
                                 ["Susan Wong", "BR02", "Queen Mattress", 17]]

    def test_add_furniture(self):
        """Test add_furniture function."""
        open(self.test_invoice_file, 'w').close()
        inventory.add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
        inventory.add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
        with open(self.test_invoice_file) as f:
            contents = csv.reader(f)
            for j,k in zip(contents, self.test_furniture_list):
                self.assertEqual(j,k)

    def test_single_customer(self):
        """Test single_customer function."""
        open(self.test_invoice_file, 'w').close()
        create_invoice = inventory.single_customer("Susan Wong", "rented_items.csv")
        create_invoice("test_items.csv")
        with open(self.test_invoice_file) as f:
            contents = csv.reader(f)
            for j, k in zip(contents, self.test_single_list):
                self.assertEqual(j, k)


