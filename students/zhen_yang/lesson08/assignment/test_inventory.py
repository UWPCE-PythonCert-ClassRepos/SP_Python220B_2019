# test_linear_parallel.py
""" This module defines all the test functions for inventory.py """
import os
from unittest import TestCase
import inventory as inv

class inventory_Tests(TestCase):
    """ This class defines unit test fuctions for invetory.py """
    def test_add_furniture(self):
        """ Test add_furniture function """
        inv.LOGGER.info('--- Start Test add_furniture() ---')
        # remove the existing 'rented_items.csv' file
        if os.path.exists('rented_items.csv'):
            os.remove('rented_items.csv')
        inv.add_furniture('rented_items.csv', 'Elisa Miles', 'LR04',
                          'Leather Sofa', 25.00)
        inv.add_furniture('rented_items.csv', 'Edward Data', 'KT78',
                          'Kitchen Table', 10.00)
        inv.add_furniture('rented_items.csv', 'Alex Gonzales', 'QM22',
                          'Queen Matress', 17.00)
        self.assertEqual(os.path.exists('rented_items.csv'), True)
        inv.LOGGER.info('--- End Test add_furniture() ---')

    def test_single_customer(self):
        """ Test single_customer function """
        inv.LOGGER.info('--- Start Test single_customer() ---')
        create_invoice = inv.single_customer('Susan Wong', 'rented_items.csv')
        create_invoice('test_items.csv')
        with open('rented_items.csv', 'r') as infile:
            lines = infile.readlines()
            self.assertEqual(len(lines), 6)
            self.assertEqual(lines[3], 'Susan Wong,MO04,Microwave Oven,35.0\n')
            self.assertEqual(lines[4], 'Susan Wong,KT88,Kitchen Chair,5.0\n')
            self.assertEqual(lines[5], 'Susan Wong,KM52,King Matress,27.0\n')
        inv.LOGGER.info('--- End Test single_customer() ---')
