"""unit tests for inventory.py"""

import os
from unittest import TestCase
from inventory import add_furniture, single_customer


def scrub_test_file(file_name):
    """remove the test file"""
    try:
        os.remove(file_name)
    except OSError:
        pass


class TestBasicOps(TestCase):
    """Class for housing the tests"""

    def test_add_furniture(self):
        """imports a csv from a file path and makes a json"""
        scrub_test_file("rented_items.csv")
        add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
        add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
        add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)
        test_list = []
        with open("rented_items.csv", newline="") as file:
            for row in file:
                test_list.append(row)
        self.assertEqual(test_list[0], ('Elisa Miles,LR04,Leather Sofa,25.0\r\n'))
        self.assertEqual(test_list[1], ('Edward Data,KT78,Kitchen Table,10.0\r\n'))
        self.assertEqual(test_list[2], ('Alex Gonzales,BR02,Queen Mattress,17.0\r\n'))


    def test_single_customer(self):
        """test adding in a single customer"""
        scrub_test_file("rented_items.csv")
        new_invoice = single_customer("rented_items.csv", "Susan Wong")
        new_invoice("data.csv")
        test_list = []
        with open("rented_items.csv", newline="") as file:
            for row in file:
                test_list.append(row)
        self.assertEqual(test_list[0], ('Susan Wong,LR04,Leather Sofa,25.0\r\n'))
        self.assertEqual(test_list[1], ('Susan Wong,KT78,Kitchen Table,10.0\r\n'))
        self.assertEqual(test_list[2], ('Susan Wong,BR02,Queen Mattress,17.0\r\n'))
