"""
Tests the database module
"""
#pylint: disable=invalid-name
from unittest import TestCase
import os
import csv
import inventory

class InventoryTests(TestCase):
    """
    Tests for the database module
    """
    def setUp(self):
        '''Set up for the tests'''
        if os.path.exists('rented_items.csv'):
            os.remove('rented_items.csv')

    def test_add_furniture(self):
        '''Tests add furniture class'''
        inventory.add_furniture("rented_items.csv", "Elisa Miles",
                                "LR04", "Leather Sofa", 25)
        self.assertTrue(os.path.exists('rented_items.csv'))
        inventory.add_furniture("rented_items.csv", "Edward Data",
                                "KT78", "Kitchen Table", 10)
        with open('rented_items.csv', 'r') as file:
            data_reader = csv.reader(file, delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
            new_list = []
            for row in data_reader:
                new_list.append(row)
        final_list = [["Elisa Miles", "LR04", "Leather Sofa", '25'],
                      ["Edward Data", "KT78", "Kitchen Table", '10']]
        self.assertEqual(new_list, final_list)

    def test_single_customer(self):
        '''Tests single customer class'''
        inventory.add_furniture("rented_items.csv", "Elisa Miles",
                                "LR04", "Leather Sofa", 25)
        create_invoice = inventory.single_customer("Susan Wong", "rented_items.csv")
        create_invoice("test_items.csv")
        with open('rented_items.csv', 'r') as file:
            data_reader = csv.reader(file, delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
            new_list = []
            for row in data_reader:
                new_list.append(row)
        final_list = [["Elisa Miles", "LR04", "Leather Sofa", '25'],
                      ["Susan Wong", "LR04", "Leather Sofa", '25'],
                      ["Susan Wong", "KT78", "Kitchen Table", '10'],
                      ["Susan Wong", "BR02", "Queen Mattress", '17']]
        self.assertEqual(new_list, final_list)
