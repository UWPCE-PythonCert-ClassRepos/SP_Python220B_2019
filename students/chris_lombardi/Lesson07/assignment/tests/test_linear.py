import sys
sys.path.append('C:\\Users\\chris\\documents\\PY220_Git\\SP_Python220B_2019\\students\\'
                'chris_lombardi\\Lesson07\\assignment')
import os
import unittest
import csv
import linear
import logging
import sample_data_expand as expander
from pymongo import errors as pyerror


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
PATH = ('C:\\users\\chris\\documents\\PY220_Git\\SP_Python220B_2019\\students\\'
        'chris_lombardi\\Lesson07\\assignment\\data')
AVAIL_PRODS = {}

class test_database(unittest.TestCase):

    def setup(self):
        # Generate test products file with 10 entries.
        print('Running setup...')
        expander.expand_products('test_prod.csv', 10)

        # Read the file into a list and get the entries that have availability.
        file_path = os.path.join(PATH, 'test_prod.csv')
        entries=[]
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                entries.append(row)

        for entry in entries:
            if int(entry[3]) > 0:
                prod_info = {'description': entry[1],
                             'product_type': entry[2],
                             'quantity_available': entry[3]}
                AVAIL_PRODS[entry[0]] = prod_info

    def test_import_data(self):
        """Test importing data into the database"""
        # Clear the database
        linear.drop_all()

        # Test that file not found error works for all three conditions.
        test_one, one_errors = linear.import_products(PATH, 'empty_prod.csv')
        test_two, two_errors = linear.import_customers(PATH, 'empty_cust.csv')
        test_three, three_errors = linear.import_rentals(PATH, 'empty_rent.csv')
        self.assertEqual(one_errors, 1)
        self.assertEqual(two_errors, 1)
        self.assertEqual(three_errors, 1)

        # Test that records are successfully added to the database with no errors.
        test_one, one_errors = linear.import_products(PATH, 'products.csv')
        test_two, two_errors = linear.import_customers(PATH, 'customers.csv')
        test_three, three_errors = linear.import_rentals(PATH, 'rentals.csv')
        self.assertEqual(test_one[0], 1000)
        self.assertEqual(test_one[1], 0)
        self.assertEqual(one_errors, 0)
        self.assertEqual(test_two[0], 1000)
        self.assertEqual(test_two[1], 0)
        self.assertEqual(two_errors, 0)
        self.assertEqual(test_three[0], 10)
        self.assertEqual(test_three[1], 0)
        self.assertEqual(three_errors, 0)

        # Test DuplicateKeyError raised when importing documents again.
        tup1, tup1_errors = linear.import_products(PATH, 'products.csv')
        tup2, tup2_errors = linear.import_customers(PATH, 'customers.csv')
        tup3, tup3_errors = linear.import_rentals(PATH, 'rentals.csv')
        self.assertEqual(tup1_errors, 1000)
        self.assertEqual(tup2_errors, 1000)
        self.assertEqual(tup3_errors, 10)
        linear.drop_all()

    def test_show_available_products(self):
        """Test show_available_products function"""
        # Clear the database
        linear.drop_all()
        self.setup()
        linear.import_products(PATH, 'test_prod.csv')
        return_dict = linear.show_available_products()
        self.assertEqual(AVAIL_PRODS, return_dict)
        linear.drop_all()

    def test_show_rentals(self):
        """Test show_rentals function"""
        # Clear the database
        linear.drop_all()
        expected_data = {'cust0003': {'name': 'George Garfield', 'address': '1078 106th Cir.',
                        'phone_number': '9660121107', 'email': 'George3@yahoo.com'},
                         'cust0008': {'name': 'Tom Miller', 'address': '3999 30th Dr.',
                         'phone_number': '1100632224', 'email': 'Tom1@msn.com'}}
        linear.import_products(PATH, 'products.csv')
        linear.import_customers(PATH, 'customers.csv')
        linear.import_rentals(PATH, 'rentals.csv')
        return_dict = linear.show_rentals('prd0001')
        self.assertEqual(expected_data, return_dict)
        linear.drop_all()

if __name__ == '__main__':
    test_database.setup()