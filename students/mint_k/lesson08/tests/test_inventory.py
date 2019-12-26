"""testing"""

import csv
from unittest import TestCase
from codes import inventory

class InventoryTests(TestCase):
    """This is to test the inventory.py"""

    def test_add_furniture(self):
        """This is to test add_furniture function in inventory.py"""

        #adding sample variables
        invoice_file = 'codes/invoice_file.csv'
        customer_name = 'Mike Thompson'
        item_code = 31
        item_description = 'Wireless Headphone'
        item_monthly_price = 60.32
        inventory.add_furniture(invoice_file, customer_name, item_code, item_description,
                                item_monthly_price)
        with open(invoice_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            my_list = []
            for row in csv_reader:
                my_list.append(row[:])
        self.assertEqual(my_list[0][0], 'Mike Thompson')

    def test_single_customer(self):
        """This is to test single customer function in inventory.py"""
        create_invoice = inventory.single_customer("Susan Wong", 'codes/invoice_file.csv')
        create_invoice("codes/test_items.csv")
        with open('codes/invoice_file.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            my_list = []
            for row in csv_reader:
                my_list.append(row[:])
        self.assertEqual(my_list[3][1], 'BR02')
