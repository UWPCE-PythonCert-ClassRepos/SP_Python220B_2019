"""
Test the inventory module
"""

from unittest import TestCase
import inventory
import os
import csv

class InventoryTests(TestCase):
    """Test the add_furniture and single_customer funcs"""

    def setUp(self):
        """Set up .csv test file"""
        if os.path.exists('test_rented_items.csv'):
            os.remove('test_rented_items.csv')

    def tearDown(self):
        pass

    def test_add_furniture(self):
        """Test add_furniture()"""

        # Test creating new file and adding 1 item
        inventory.add_furniture('test_rented_items.csv', 'John Adams', 'LK25', 'Leather Chair', 25)

        # Test adding multiple items into existing file
        inventory.add_furniture('test_rented_items.csv', 'Ivan Ramen', 'ST68', 'Bar Stool', 15)
        inventory.add_furniture('test_rented_items.csv', 'Irene Jules', 'SF22', 'Sofa', 150)

        # Check for added items
        with open('test_rented_items.csv', 'r') as file:
            reader = csv.reader(file)
            data = []
            for row in reader:
                data.append(row)

        test_list = [['customer_name', 'item_code', 'item_description', 'item_monthly_price'],
                     ['John Adams', 'LK25', 'Leather Chair', '25'],
                     ['Ivan Ramen', 'ST68', 'Bar Stool', '15'],
                     ['Irene Jules', 'SF22', 'Sofa', '150']]

        self.assertEqual(test_list, data)

    def test_single_customer(self):
        """Test single_customer()"""
        # Test creating new file and adding 1 item
        inventory.add_furniture('test_rented_items.csv', 'John Adams', 'LK25', 'Leather Chair', 25)

        # Test adding multiple items into existing file
        inventory.add_furniture('test_rented_items.csv', 'Ivan Ramen', 'ST68', 'Bar Stool', 15)
        inventory.add_furniture('test_rented_items.csv', 'Irene Jules', 'SF22', 'Sofa', 150)

        # Test adding multiple items with single_customer
        bulk_add = inventory.single_customer('Susan', 'test_rented_items.csv')

        bulk_add('all_rentals.csv')

        # Check for added items
        with open('test_rented_items.csv', 'r') as file:
            reader = csv.reader(file)
            data = []
            for row in reader:
                data.append(row)

        test_list = [['customer_name', 'item_code', 'item_description', 'item_monthly_price'],
                     ['John Adams', 'LK25', 'Leather Chair', '25'],
                     ['Ivan Ramen', 'ST68', 'Bar Stool', '15'],
                     ['Irene Jules', 'SF22', 'Sofa', '150'],
                     ['Susan', 'HM25', 'Mattress', '150'],
                     ['Susan', 'JK10', 'Grill', '20'],
                     ['Susan', 'YG36', 'Rug', '300']]

        self.assertEqual(test_list, data)
