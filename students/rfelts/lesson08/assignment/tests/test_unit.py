#!/usr/bin/env python3

# Russell Felts
# Assignment 8 - Unit Tests

""" Unit tests """

from unittest import TestCase
import csv
import inventory


class InventoryUnitTest(TestCase):
    """ Unit tests for the database class """

    def test_add_furniture(self):
        """ Unit test for the add_furniture function """

        inventory_list = [["Elisa Miles", "LR04", "Leather Sofa", "25"],
                          ["Edward Data", "KT78", "Kitchen Table", "10"],
                          ["Alex Gonzales", "BR02", "Queen Mattress", "17"]]
        for item in inventory_list:
            inventory.add_furniture("data/rental_data.csv", item[0], item[1], item[2], item[3])

        with open("data/rental_data.csv", 'r') as rental_file:
            reader = csv.reader(rental_file)
            self.assertListEqual(list(reader), inventory_list)

    def test_single_customer(self):
        """ Unit test for the single_customer function """

        create_invoice = inventory.single_customer("Bruce Wayne", "data/rental_data.csv")
        create_invoice("data/test_items.csv")

        with open("data/rental_data.csv", 'r') as rental_file:
            reader = csv.reader(rental_file)
            self.assertIn(["Bruce Wayne", "BM500", "Batmobile Remote Control", "1000"],
                          list(reader))
