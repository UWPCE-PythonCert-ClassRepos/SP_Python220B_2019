import sys
sys.path.append('../')
from unittest import TestCase
import inventory
import os
import csv


RENTED_ITEMS_FILE = 'rented_items.csv'

EXPECTED_DATA = [['Elisa Miles', 'LR04', 'Leather Sofa', '25.0'],
                 ['Edward Data', 'KT78', 'Kitchen Table', '10.0'],
                 ['Alex Gonzales', 'BR02', 'Queen Mattress', '17.0'],
                 ['Susan Wong', 'LR04', 'Leather Sofa', '25.00'],
                 ['Susan Wong', 'KT78', 'Kitchen Table', '10.00'],
                 ['Susan Wong', 'BR02', 'Queen Mattress', '17.00']]

class InventoryTest(TestCase):

    def tearDown(self):
        if os.path.exists(RENTED_ITEMS_FILE):
            os.remove(RENTED_ITEMS_FILE)

    def test_add_furntiure(self):
        inventory.add_furniture(RENTED_ITEMS_FILE, 'Elisa Miles', 'LR04', 'Leather Sofa', 25.00)
        inventory.add_furniture(RENTED_ITEMS_FILE, 'Edward Data', 'KT78', 'Kitchen Table', 10.00)
        inventory.add_furniture(RENTED_ITEMS_FILE, 'Alex Gonzales', 'BR02', 'Queen Mattress', 17.00)
        create_invoice = inventory.single_customer("Susan Wong", RENTED_ITEMS_FILE)
        create_invoice("test_items.csv")

        with open(RENTED_ITEMS_FILE, newline='') as input_file:
            field_names = ['customer_name', 'item_code', 'item_description', 'item_monthly_price']
            reader = csv.DictReader(input_file, field_names)
            for index, row in enumerate(reader):
                expected_row = EXPECTED_DATA[index]
                for i in range(4):
                    self.assertEqual(expected_row[i], row[field_names[i]])

