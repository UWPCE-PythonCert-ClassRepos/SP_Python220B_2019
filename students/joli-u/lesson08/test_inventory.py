"""
test_inventory.py
Assignment 8
Joli Umetsu
PY220
"""

from unittest import TestCase
import csv
from inventory import add_furniture, single_customer


class TestInventory(TestCase):
    """ Unit tests for inventory functions """

    def test_add_furniture(self):
        """ Tests function to add rental data to csv file """
        rental_data = [['Elisa Miles', 'LC04', 'Leather Chair', '12.0'],
                       ['Edward Data', 'CT78', 'Coffee Table', '10.0'],
                       ['Alex Gonzales', 'BR01', 'Bed Frame', '80.0']]
        invoice_file = "rental_data.csv"
        for record in rental_data:
            add_furniture(invoice_file, record[0], record[1], record[2], record[3])

        with open(invoice_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        self.assertEqual(data, rental_data)


    def test_single_customer(self):
        """ Tests function to add multiple rental data for a single customer """
        name = "Susan Wong"
        items = [['LR04', 'Leather Sofa', '25'],
                 ['KT78', 'Kitchen Table', '15'],
                 ['BR02', 'Queen Mattress', '17']]
        for item in items:
            item.insert(0, name)

        invoice_file = "rental_data.csv"

        create_invoice = single_customer(name, invoice_file)
        create_invoice("test_items.csv")

        with open(invoice_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data_list = list(reader)

        del data_list[:3]

        self.assertEqual(data_list, items)
