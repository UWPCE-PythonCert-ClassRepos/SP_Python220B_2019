'''
Test suite for inventory.py module
'''

import os
import csv
from unittest import TestCase
from inventory import add_furniture, single_customer

class InventoryTests(TestCase):
    '''
    Test suite for inventory module
    '''
    @classmethod
    def setUpClass(cls):
        cls.test_add_furnture_file = 'test_furniture.csv'
        cls.test_single_customer_read_file = 'test_items.csv'
        cls.test_single_customer_write_file = 'rented_items.csv'
        cls.furniture_lines = [['Elisa Miles','LR04','Leather Sofa',25],
                                ['Edward Data','KT78','Kitchen Table',10],
                                ['Alex Gonzales','BR02','Queen Mattress',17]]
        cls.single_customer_lines = [['Susan Wong','LR04','Leather Sofa',25],
                                     ['Susan Wong','KT78','Kitchen Table',10],
                                     ['Susan Wong','BR02','Queen Mattress',17]]
        with open(cls.test_single_customer_read_file,'w') as test_csv:
            test_csv.write('LR04,Leather Sofa,25.00\n')
            test_csv.write('KT78,Kitchen Table,10.00\n')
            test_csv.write('BR02,Queen Mattress,17.00')

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_add_furnture_file)
        os.remove(cls.test_single_customer_read_file)
        os.remove(cls.test_single_customer_write_file)

    def test_add_furniture(self):
        for item in self.furniture_lines:
            add_furniture(self.test_add_furnture_file, *item)
        # Read csv file to confirm correct write
        with open(self.test_add_furnture_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for i,row in enumerate(csv_reader):
                # Convert final column (price) to int
                row[-1] = int(float(row[-1]))
                # Ensure row is equal to input data
                self.assertEqual(self.furniture_lines[i], row)

    def test_single_customer(self):
        create_invoice = single_customer("Susan Wong", self.test_single_customer_write_file)
        create_invoice(self.test_single_customer_read_file)
        # Read csv file to confirm correct write
        with open(self.test_single_customer_write_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for i,row in enumerate(csv_reader):
                # Convert final column (price) to int
                row[-1] = int(float(row[-1]))
                # Ensure row is equal to input data
                self.assertEqual(self.single_customer_lines[i], row)
