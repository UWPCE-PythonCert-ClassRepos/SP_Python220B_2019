"""
This file will test the methods in database.py for reading and writing to a mongoDB database
"""

import csv
import os
import logging
import unittest
import sys
import database
from database import MongoDBConnection

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'test.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class TestDatabase(unittest.TestCase):
    """This class will contain all the tests for database.py"""

    def test_import(self):
        """This method will test import of .csv files to the database"""

        database.delete_database()

        #Fully successful import
        actual_tuples1 = database.import_data('csvs', 'product_data.csv', 'customer_data.csv',
                                           'rentals_data.csv')
        expected_tuples1 = ((1, 1, 1), (0, 0, 0))
        self.assertEqual(actual_tuples1, expected_tuples1)
        database.delete_database()

        #Partially successful import with failed product_data
        actual_tuples2 = database.import_data('csvs', 'produc_data.csv', 'customer_data.csv',
                                           'rentals_data.csv')
        expected_tuples2 = ((0, 1, 1), (1, 0, 0))
        self.assertEqual(actual_tuples2, expected_tuples2)
        database.delete_database()

        #Partially successful import with failed customer_data
        actual_tuples3 = database.import_data('csvs', 'product_data.csv', 'custome_data.csv',
                                           'rentals_data.csv')
        expected_tuples3 = ((1, 0, 1), (0, 1, 0))
        self.assertEqual(actual_tuples3, expected_tuples3)
        database.delete_database()

        #Partially successful import with failed rentals_data
        actual_tuples4 = database.import_data('csvs', 'product_data.csv', 'customer_data.csv',
                                           'rental_data.csv')
        expected_tuples4 = ((1, 1, 0), (0, 0, 1))
        self.assertEqual(actual_tuples4, expected_tuples4)
        database.delete_database()

    def test_show_available(self):
        """This method tests that all and only available products are displayed"""
        database.import_data('csvs', 'product_data.csv', 'customer_data.csv', 'rentals_data.csv')
        actual_available = database.show_available_products()
        expected_available = {'prd001': {'description': 'TV', 'product_type': 'livingroom',
                              'quantity_available': '3'},
                             'prd002': {'description': 'Couch', 'product_type': 'livingroom',
                              'quantity_available': '1'}}
        self.assertEqual(actual_available, expected_available)
        database.delete_database()

        database.import_data('csvs', 'produc_data.csv', 'customer_data.csv', 'rentals_data.csv')
        database.delete_database()

    def test_show_rentals(self):
        """This method tests that the correct customers are displayed for the product_id"""
        database.import_data('csvs', 'product_data.csv', 'customer_data.csv', 'rentals_data.csv')
        actual_customers1 = database.show_rentals('prd002')
        expected_customers1 = {'cst001': {'name': 'Charlie', 'address': '123 Fleet Street',
                                         'phone_number': '1231234123'},
                              'cst002': {'name': 'Andrey', 'address': '123 Jordan Street',
                                         'phone_number': '4564564567'}}
        actual_customers2 = database.show_rentals('prd009')
        expected_customers2 = {}
        self.assertEqual(actual_customers1, expected_customers1)
        self.assertEqual(actual_customers2, expected_customers2)

#This method is only to be used for the creation of .csv files if there are none
'''def write_csv():
    """This method writes the csv files to import for testing"""

    try:  
        os.mkdir('csvs')
    except OSError:  
        print ("Could not create directory")
    else:  
        print ("Successfully created the directory")

    LOGGER.debug("Establishing dictionaries for csv")
    product_data = {'prd001': {'description': 'TV', 'product_type': 'livingroom',
                               'quantity_available': 3},
                    'prd002': {'description': 'Couch', 'product_type': 'livingroom',
                               'quantity_available': 1},
                    'prd003': {'description': 'Chair', 'product_type': 'livingroom',
                               'quantity_available': 0}}

    customer_data = {'cst001': {'name': 'Charlie', 'address': '123 Fleet Street',
                                'phone_number': '1231234123'},
                     'cst002': {'name': 'Andrey', 'address': '123 Jordan Street',
                                'phone_number': '4564564567'},
                     'cst003': {'name': 'Vijay', 'address': '123 Lake Street',
                                'phone_number': '7987897891'}}

    rentals_data = {'cst001': {'name': 'Charlie', 'rentals': ['prd001', 'prd002']},
                    'cst002': {'name': 'Andrey', 'rentals': ['prd002', 'prd003']},
                    'cst003': {'name': 'Vijay', 'rentals': ['prd001', 'prd003']}}

    LOGGER.debug("Writing to .csv files")
    with open('csvs/product_data.csv', 'w') as products:
        product_fields = ['id', 'description', 'product_type', 'quantity_available']
        product_writer = csv.DictWriter(products, delimiter=',', lineterminator='\n', fieldnames=product_fields)
        product_writer.writeheader()
        for key, value in product_data.items():
            product_row = {'id': key}
            product_row.update(value)
            product_writer.writerow(product_row)

    with open('csvs/customer_data.csv', 'w') as customers:
        customer_fields = ['id', 'name', 'address', 'phone_number']
        customer_writer = csv.DictWriter(customers, delimiter=',', lineterminator='\n', fieldnames=customer_fields)
        customer_writer.writeheader()
        for key, value in customer_data.items():
            customer_row = {'id': key}
            customer_row.update(value)
            customer_writer.writerow(customer_row)

    with open('csvs/rentals_data.csv', 'w') as rentals:
        rentals_fields = ['id', 'name', 'rentals']
        rentals_writer = csv.DictWriter(rentals, delimiter=',', lineterminator='\n', fieldnames=rentals_fields)
        rentals_writer.writeheader()
        for key, value in rentals_data.items():
            rentals_row = {'id': key}
            value['rentals'] = ' '.join(value['rentals']) 
            rentals_row.update(value)
            rentals_writer.writerow(rentals_row)

    LOGGER.debug("Writing complete")'''

if __name__ == '__main__':
#    write_csv()
    unittest.main()
