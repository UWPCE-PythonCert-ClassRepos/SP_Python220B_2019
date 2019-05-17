# -*- coding: utf-8 -*-
"""
Created on Mon May 13 20:09:02 2019

@author: Laura.Fiorentino
"""

from unittest import TestCase
import csv
from inventory import add_furniture, single_customer


class TestInventory(TestCase):
    """ test inventory.py"""

    def test_add_furniture(self):
        """tests add_furniture"""
        add_furniture('test_invoice.csv', 'Dorothy Zbornak', 'C100', 'couch',
                      25)
        add_furniture('test_invoice.csv', 'Rose Nylund', 'DT100',
                      'dining table', 20)
        add_furniture('test_invoice.csv', 'Blanche Devereaux',
                      'AC100', 'arm chair', 20)
        add_furniture('test_invoice.csv', 'Sophia Petrillo', 'R100',
                      'recliner', 30)

        with open('test_invoice.csv', 'r') as test_invoice:
            test_csv_reader = csv.reader(test_invoice)
            test_row = next(test_csv_reader)
        self.assertEqual(test_row, ['Dorothy Zbornak', 'C100', 'couch', '25'])

    def test_single_customer(self):
        """tests single_customer"""
        with open('Dorothy_Zbornak.csv', 'a', newline='') as invoice:
            invoice_write = csv.writer(invoice, delimiter=',')
            invoice_write.writerow(['T100', 'television', 50])
            invoice_write.writerow(['CT100', 'coffee table', 10])
            invoice_write.writerow(['QB100', 'queen bed', 40])

        dorothy = single_customer('Dorothy Zbornak', 'test_invoice.csv')
        dorothy('Dorothy_Zbornak.csv')
        with open('test_invoice.csv', 'r') as test_invoice:
            test_csv_reader = csv.reader(test_invoice)
            test_row = next(test_csv_reader)
        self.assertEqual(test_row, ['Dorothy Zbornak', 'C100', 'couch', '25'])
        with open('test_invoice.csv', 'r') as test_invoice:
            test_csv_reader = csv.reader(test_invoice)
            test_row = (next(reversed(list(test_csv_reader))))
        self.assertEqual(test_row, ['Dorothy Zbornak', 'QB100', 'queen bed',
                                    '40'])
