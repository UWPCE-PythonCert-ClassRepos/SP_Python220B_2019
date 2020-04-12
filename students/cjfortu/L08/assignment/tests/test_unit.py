#!/usr/bin/env python
"""
Unit tests.
"""

from unittest import TestCase
from unittest.mock import patch
from io import StringIO
import os
import sys

os.chdir('..')
sys.path.append(os.getcwd())

from inventory import *


class FunctionTests(TestCase):
    """
    Test the functions in the module.
    """
    # test_rental_items_path = os.getcwd() + '/tests/' + 'test_rental_items.csv'

    def setUp(self):
        self.test_invoice_file_path = os.getcwd() + '/' + 'test_invoice_file.csv'
        # self.test_rental_items_path = os.getcwd() + '/tests/' + 'test_rental_items.csv'
        # self.test_rental_items_path = r'/Users/fortucj/Documents/skoo/Python/220/SP_Python220B_2019/students/cjfortu/L08/assignment/tests/test_rental_items.csv'

    def tearDown(self):
        os.remove(self.test_invoice_file_path)

    def test_add_furniture(self):
        """
        Test all elements of add_furniture.
        """
        add_furniture('test_invoice_file.csv', 'test Edward Data', 'test KT78',
                      'test Kitchen Table', 10.009)
        self.assertTrue(os.path.exists(self.test_invoice_file_path))
        with open(self.test_invoice_file_path, 'r', encoding='utf-8-sig') as read_file:
                csv_reader = csv.reader(read_file)
                for i, row in enumerate(csv_reader):
                    self.assertEqual(row, ['test Edward Data', 'test KT78',
                                     'test Kitchen Table', '10.01'])
                self.assertEqual(i, 0)

    def test_single_customer(self):
        """
        Test all elements of single_customer.
        """
        amend_Edward = single_customer('test Edward Data', 'test_invoice_file.csv')
        # test_rental_items_path = os.getcwd() + '/tests/' + 'test_rental_items.csv'
        # test_rental_items_path = r'/Users/fortucj/Documents/skoo/Python/220/SP_Python220B_2019/students/cjfortu/L08/assignment/tests/test_rental_items.csv'
        amend_Edward('test_rental_items.csv')
        # single_customer('test Edward Data', 'test_invoice_file.csv')(self.test_rental_items_path)
        self.assertTrue(os.path.exists(self.test_invoice_file_path))
        with open(self.test_invoice_file_path, 'r', encoding='utf-8-sig') as read_file:
                csv_reader = csv.reader(read_file)
                for i, row in enumerate(csv_reader):
                    if i == 0:
                        self.assertEqual(row, ['test Edward Data', 'LR04', 'Leather Sofa',
                                         '25.00'])
                    if i == 1:
                        self.assertEqual(row, ['test Edward Data', 'KT78', 'Kitchen Table',
                                         '10.00'])
                    if i == 2:
                        self.assertEqual(row, ['test Edward Data', 'BR02', 'Queen Mattress',
                                         '17.00'])