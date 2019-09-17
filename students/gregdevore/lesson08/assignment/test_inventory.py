'''
Test suite for inventory.py module
'''

import os
import csv
from unittest import TestCase
from inventory import add_furniture

class InventoryTests(TestCase):
    '''
    Test suite for inventory module
    '''
    @classmethod
    def setUpClass(cls):
        cls.test_file = 'test_furniture.csv'

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_file)

    def test_add_furniture(self):
        to_add = [['Elisa Miles','LR04','Leather Sofa',25],
                  ['Edward Data','KT78','Kitchen Table',10],
                  ['Alex Gonzales','BR02','Queen Mattress',17]]
        for item in to_add:
            add_furniture(self.test_file, *item)
        # Read csv file to confirm correct write
        with open(self.test_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for i,row in enumerate(csv_reader):
                # Convert final column (price) to int
                row[-1] = int(float(row[-1]))
                # Ensure row is equal to input data
                self.assertEqual(to_add[i], row)
