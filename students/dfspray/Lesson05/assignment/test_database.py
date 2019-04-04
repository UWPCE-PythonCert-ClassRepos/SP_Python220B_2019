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

        #Fully successful import
        actual_tuples1 = database.import_data('csvs', 'product_data.csv', 'customer_data.csv',
                                           'rentals_data.csv')
        expected_tuples1 = [(3, 3, 3), (0)]
        self.assertEqual(actual_tuples1, expected_tuples1)
        delete_database()

        #Partially successful import with failed product_data
        actual_tuples2 = database.import_data('csvs', 'produc_data.csv', 'customer_data.csv',
                                           'rentals_data.csv')
        expected_tuples2 = [(0, 3, 3), (1)]
        self.assertEqual(actual_tuples2, expected_tuples2)
        delete_database()

        #Partially successful import with failed customer_data
        actual_tuples3 = database.import_data('csvs', 'product_data.csv', 'custome_data.csv',
                                           'rentals_data.csv')
        expected_tuples3 = [(3, 0, 3), (1)]
        self.assertEqual(actual_tuples3, expected_tuples3)
        delete_database()

        #Partially successful import with failed rentals_data
        actual_tuples4 = database.import_data('csvs', 'product_data.csv', 'customer_data.csv',
                                           'rental_data.csv')
        expected_tuples4 = [(3, 3, 0), (1)]
        self.assertEqual(actual_tuples4, expected_tuples4)
        delete_database()

    def test_show_available(self):
        """This method tests that all and only available products are displayed"""
        database.import_data('csvs', 'product_data.csv', 'customer_data.csv', 'rentals_data.csv')
        actual_available = database.show_available_products()
        expected_available = {'prd001': {'description': 'TV', 'product_type': 'livingroom',
                              'quantity_available': 3},
                             'prd002': {'description': 'Couch', 'product_type': 'livingroom',
                              'quantity_available': 1}}
        self.assertEqual(actual_available, expected_available)
        delete_database()

        database.import_data('csvs', 'produc_data.csv', 'customer_data.csv', 'rentals_data.csv')
        with self.assertRaises(ValueError):
            database.show_available_products()

#    def test_show_rentals(

def delete_database():
    """This method deletes the database to reset for other tests"""
    mongo = MongoDBConnection
    with mongo:
        db = mongo.connection.rental_company
        db.dropDatabase()
    LOGGER.debug("Deleted database")

def write_csv():
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

    rentals_data = {'usr001': {'name': 'Charlie', 'address': '123 Fleet Street',
                               'phone_number': '1231234123', 'email': 'charlie@gmail.com'},
                    'usr002': {'name': 'Andrey', 'address': '123 Jordan Street',
                               'phone_number': '4564564567', 'email': 'andrey@gmail.com'},
                    'usr003': {'name': 'Vijay', 'address': '123 Lake Street',
                               'phone_number': '7987897891', 'email': 'vijay@gmail.com'}}

    LOGGER.debug("Writing to .csv files")
    with open('csvs/product_data.csv', 'w') as products:
        product_writer = csv.writer(products)
        for key, value in product_data.items():
            product_writer.writerow([key, dict(value)])

    with open('csvs/customer_data.csv', 'w') as customers:
        customer_writer = csv.writer(customers)
        for key, value in customer_data.items():
            customer_writer.writerow([key, dict(value)])

    with open('csvs/rentals_data.csv', 'w') as rentals:
        rentals_writer = csv.writer(rentals)
        for key, value in rentals_data.items():
            rentals_writer.writerow([key, dict(value)])

    LOGGER.debug("Writing complete")

if __name__ == '__main__':
    write_csv()
    unittest.main()