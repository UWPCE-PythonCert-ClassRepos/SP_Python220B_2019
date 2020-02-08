# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 10:36:31 2020

@author: uz367d
"""

import os
import csv
from unittest import TestCase
import filecmp
from assignment.inventory import add_furniture
from assignment.inventory import single_customer


class TestInventory(TestCase):
    """Tests the inventory functionalities"""

    def setUp(self):
        """Sets up the environment for testing"""
        filename = "rented_items.csv"
        file = open(filename, "a")
        file.close()

        with open("test_items.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["LR04", "Leather Sofa", 25.00])
            writer.writerow(["KT78", "Kitchen Tablee", 10.00])
            writer.writerow(["BR02", "Queen Mattress", 17.00])
            file.close()

        with open("comparison.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Susan Wong", "LR04", "Leather Sofa", 25.00])
            writer.writerow(["Susan Wong", "KT78", "Kitchen Tablee", 10.00])
            writer.writerow(["Susan Wong", "BR02", "Queen Mattress", 17.00])
            file.close()

    def tearDown(self):
        """Tears down all creations for testing"""
        os.remove("rented_items.csv")
        os.remove("test_items.csv")
        os.remove("comparison.csv")

    def test_add_furniture(self):
        """test to make sure an entry is added to the file"""
        invoice_file = "rented_items.csv"
        customer_name = "Ashley Miles"
        item_code = "N64"
        item_description = "Videogame Console"
        item_monthly_price = "25.0"

        add_furniture(invoice_file, customer_name, item_code,
                      item_description, item_monthly_price)

        with open(invoice_file, "r") as cfile:
            reader = csv.reader(cfile)
            for row in reader:
                self.assertEqual(customer_name, row[0])
                self.assertEqual(item_code, row[1])
                self.assertEqual(item_description, row[2])
                self.assertEqual(item_monthly_price, row[3])

    def test_single_customer(self):
        """tests to make sure single_customer functions properly"""
        create_invoice = single_customer("rented_items.csv", "Susan Wong")
        create_invoice("test_items.csv")

        self.assertTrue(filecmp.cmp("rented_items.csv", "comparison.csv", shallow=False))
