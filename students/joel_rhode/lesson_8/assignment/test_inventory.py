"""Test module for inventory module."""

from unittest import TestCase
from csv import reader
from inventory import add_furniture, single_customer


class InventoryUnitTesting(TestCase):
    """Unit tests for the inventory functions."""

    def test_add_furniture_unit(self):
        """Unit test of the add_furniture function."""
        test_file = 'add_furniture_test.csv'
        add_furniture(test_file, 'Bob Bobbo', 'LT02', 'Cloth Couch', 17.00)
        add_furniture(test_file, 'Jane Jano', 'TT339', 'Dining Room Table', 25.32)

        test_result = []
        with open(test_file, 'r') as read_file:
            for line in reader(read_file):
                test_result.append(line)

        self.assertListEqual(test_result[-2], ['Bob Bobbo', 'LT02', 'Cloth Couch', '17.0'])
        self.assertListEqual(test_result[-1], ['Jane Jano', 'TT339', 'Dining Room Table', '25.32'])


    def test_single_customer(self):
        """Unit test of the single_customer function"""
        test_file = 'single_customer_test.csv'
        test_items = []
        with open('test_items.csv', newline='') as test_items_file:
            for line in reader(test_items_file):
                test_items.append(line)
        test_cust_add = single_customer('Bob Bobbo', test_file)
        test_cust_add(test_items)

        test_result = []
        with open(test_file, 'r') as read_file:
            for line in reader(read_file):
                test_result.append(line)

        for item in test_items:
            item.insert(0, 'Bob Bobbo')
        self.assertListEqual(test_result[-len(test_items):], test_items)
