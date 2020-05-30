"""
Tests Inventory module and functionality.
"""

# pylint:disable=wildcard-import
# pylint:disable=unused-wildcard-import

from unittest import TestCase
from inventory import *

class TestIventory(TestCase):
    """Class to test inventory module."""

    def test_add_furniture(self):
        """Function to test add furniture functionality."""

        add_furniture('invoice.csv', 'Elisa Miles', 'LR04', 'Leather Sofa', 25)
        add_furniture('invoice.csv', 'Edward Data', 'KT78', 'Kitchen Table', 10)
        add_furniture('invoice.csv', 'Alex Gonzales', 'BR02', 'Queen Mattress', 17)

        # Generate list of rentals
        with open('invoice.csv', 'r') as csvfile:
            rentals = []
            for row in csvfile:
                rentals.append(row)

        print(rentals)

        # Assert statements
        self.assertEqual(rentals[0], ('Elisa Miles,LR04,Leather Sofa,25\n'))
        self.assertEqual(rentals[1], ('Edward Data,KT78,Kitchen Table,10\n'))
        self.assertEqual(rentals[2], ('Alex Gonzales,BR02,Queen Mattress,17\n'))

    def test_single_customer(self):
        """Tests single customer functionality."""

        create_invoice = single_customer("Susan Wong", "invoice.csv")
        create_invoice("test_items.csv")

        # Generate list of rentals
        with open('invoice.csv', 'r') as csvfile:
            rentals = []
            for row in csvfile:
                rentals.append(row)

        print(rentals)

        # Assert statements
        self.assertEqual(rentals[3], ('Susan Wong,AT92,Office Chair,13\n'))
        self.assertEqual(rentals[4], ('Susan Wong,KE25,Espresso Machine,30\n'))
