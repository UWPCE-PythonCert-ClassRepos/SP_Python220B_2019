""" This module tests the inventory module """
import csv
import os
from unittest import TestCase
from functools import partial
from inventory import *

class InventoryTests(TestCase):
    """ This class tests inventory functions """

    def test_add_furniture(self, invoice_file='invoice_test.csv'):
        """ Test inventory function """
        #Start with fresh file
        os.remove(invoice_file)
        add_furniture(invoice_file, "Elisa Miles", "LR04", "Leather Sofa", 25)
        add_furniture(invoice_file, "Edward Data", "KT78", "Kitchen Table", 10)
        add_furniture(invoice_file, "Alex Gonzales", "BR02", "Queen Mattress", 17)

        expected = [['Elisa Miles', 'LR04', 'Leather Sofa', '25'],
                    ['Edward Data', 'KT78', 'Kitchen Table', '10'],
                    ['Alex Gonzales', 'BR02', 'Queen Mattress', '17']]

        with open(invoice_file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for i, row in enumerate(reader):
                self.assertEqual(row, expected[i])

    def test_single_customer(self, invoice_file='invoice_test.csv'):
        """ This module tests single_customer function """
        os.remove(invoice_file)
        add_karl = partial(single_customer, customer_name='Karl', invoice_file=invoice_file)
        #### Why is there error here ?s
        test1 = add_karl()
        test1('rental_items.csv')

        expected = [['Karl', 'LR04', 'Leather Sofa', '25'],
                    ['Karl', 'KT78', 'Kitchen Table', '10'],
                    ['Karl', 'BR02', 'Queen Mattress', '17']]
        with open(invoice_file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for i, row in enumerate(reader):
                self.assertEqual(expected[i], row)
