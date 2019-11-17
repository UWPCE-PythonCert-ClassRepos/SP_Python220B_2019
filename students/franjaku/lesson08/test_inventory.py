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
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row)
                print(row)

        test_list = [{'customer_name': 'John Adams',
                      'item_code': 'LK25',
                      'item_description': 'Leather Chair',
                      'item_monthly_price': 25},
                     {'customer_name': 'Ivan Ramen',
                      'item_code': 'ST68',
                      'item_description': 'Bar Stool',
                      'item_monthly_price': 15},
                     {'customer_name': 'Irene Jules',
                      'item_code': 'SF22',
                      'item_description': 'Sofa',
                      'item_monthly_price': 150}
                     ]

        self.assertEqual(test_list, data)

    def test_single_customer(self):
        """Test single_customer()"""
        pass
