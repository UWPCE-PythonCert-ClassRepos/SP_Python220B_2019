""" Unit tests for inventory.py """

# pylint: disable=invalid-name

import os
from pathlib import Path
from unittest import TestCase
from src.inventory import add_furniture, single_customer



class InventoryTest(TestCase):
    """ Inventory tests"""

    def setUp(self):
        try:
            os.remove("./invoices/rented_items.csv")
        except FileExistsError:
            print("./invoices/rented_items.csv does not exist")

    def tearDown(self):
        pass

    def test_add_furniture_should_create_invoice(self):
        """ Create invoice, verify CSV created"""
        # Given
        expected_filename = "rented_items.csv"
        expected_directory = "./invoices"
        file_path = Path(expected_directory) / expected_filename

        # When
        add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)

        # Then
        self.assertTrue(os.path.isfile(file_path))
        # os.remove("./inventories/rental_items.csv")

    def test_add_furniture_should_add_line_to_blank_file(self):
        """ Create invoice, add line to it"""
        # Given
        filename = "rented_items.csv"
        directory = "./invoices"
        file_path = Path(directory) / filename
        name = "Elisa Miles"
        prod_id = "LR04"
        description = "Leather Sofa"
        price = 25

        expected_line = ",".join([name, prod_id, description, str(price)])
        expected_line += "\n"

        # When
        add_furniture(filename, name, prod_id, description, price)

        # Then
        with open(file_path, "r") as f:
            read_line = f.readline()

        self.assertEqual(expected_line, read_line)
        # os.remove("./inventories/rental_items.csv")

    def test_add_furniture_should_be_able_to_add_multiple_lines(self):
        """ Create invoice, add many entries """
        # Given
        expected_lines = [
            "Elisa Miles,LR04,Leather Sofa,25\n",
            "Edward Data,KT78,Kitchen Table,10\n",
            "Alex Gonzales,BR02,Queen Mattress,17\n",
        ]
        # When
        add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
        add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
        add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)

        actual_lines = []
        with open("./invoices/rented_items.csv", "r") as f:
            for line in f:
                actual_lines.append(line)
        # Then
        self.assertListEqual(expected_lines, actual_lines)
        # os.remove("./inventories/rental_items.csv")

    def test_create_invoice_for_single_customer_should_create_invoice(self):
        """ Test create_invoice to see if file is generated correctly """
        # Given
        expected_contents = [
            "Elisa Miles,LR04,Leather Sofa,25\n",
            "Edward Data,KT78,Kitchen Table,10\n",
            "Alex Gonzales,BR02,Queen Mattress,17\n",
            "Susan Wong,LR04,Leather Sofa,25.00\n",
            "Susan Wong,KT78,Kitchen Table,10.00\n",
            "Susan Wong,BR02,Queen Mattress,17.00\n",
        ]

        # Whenadd_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
        add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
        add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
        add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)

        create_invoice = single_customer("Susan Wong", "rented_items.csv")
        self.assertTrue(callable(create_invoice))
        create_invoice("test_items.csv")

        # Then
        actual_lines = []
        with open("./invoices/rented_items.csv", "r") as f:
            for line in f:
                actual_lines.append(line)

        self.assertListEqual(expected_contents, actual_lines)
