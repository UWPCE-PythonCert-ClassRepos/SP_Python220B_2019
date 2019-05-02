"""
This file will test all thr cunctions in inventory.py
"""

import logging
import unittest
import os
import csv
from src import inventory

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = os.path.join(os.path.dirname(__file__), 'test_inventory.log')
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class TestInventory(unittest.TestCase):
    """This class will contain all the tests for inventory.py"""

    def test_add_furniture(self):
        """This method will test the add_furniture function in inventory.py"""
        file_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'test_add_furniture.csv')
        try:
            os.remove(file_path)
        except FileNotFoundError:
            LOGGER.debug("No leftover files found")

        actual_items1 = []

        inventory.add_furniture("test_add_furniture.csv", "Elisa Miles",
                                "LR04", "Leather Sofa", 25)
        inventory.add_furniture("test_add_furniture.csv", "Edward Data",
                                "KT78", "Kitchen Table", 10)
        inventory.add_furniture("test_add_furniture.csv", "Alex Gonzales",
                                "QM15", "Queen Mattress", 17)

        with open(file_path) as test:
            test_reader = csv.reader(test, delimiter=',', quotechar='"')
            for row in test_reader:
                actual_items1.append(row)
        expected_items1 = [["Elisa Miles", "LR04", "Leather Sofa", '25'],
                           ["Edward Data", "KT78", "Kitchen Table", '10'],
                           ["Alex Gonzales", "QM15", "Queen Mattress", '17']]
        self.assertEqual(actual_items1, expected_items1)
        os.remove(file_path)

    def test_single_customer(self):
        """This method will test the single_customer function in inventory.py"""
        file_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'test_single_customer.csv')
        try:
            os.remove(file_path)
        except FileNotFoundError:
            LOGGER.debug("No leftover files found")

        actual_items2 = []

        create_invoice = inventory.single_customer("Susan Wong", "test_single_customer.csv")
        create_invoice("test_items.csv")

        with open(file_path) as test:
            test_reader = csv.reader(test, delimiter=',', quotechar='"')
            for row in test_reader:
                actual_items2.append(row)
        expected_items2 = [['Susan Wong', 'LR04', 'Leather Sofa', '25.00'],
                           ['Susan Wong', 'KT78', 'Kitchen Table', '10.00'],
                           ['Susan Wong', 'BR02', 'Queen Mattress', '17.00']]
        self.assertEqual(actual_items2, expected_items2)
        os.remove(file_path)
