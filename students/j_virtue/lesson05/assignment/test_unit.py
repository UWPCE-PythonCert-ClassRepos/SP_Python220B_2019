"""Module for Unit tests"""

# Advanced Programming in Python -- Lesson 5 Assignment 1
# Jason Virtue
# Start Date 2/20/2020

#Supress pylint warnings here
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name,too-few-public-methods,wrong-import-order,singleton-comparison,too-many-arguments,logging-format-interpolation

import sys
from unittest import TestCase
import logging
import os
from database import *

# Set up log file
logging.basicConfig(filename="db.log", format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M %p', level=logging.INFO)

class TestDatabaseSetup(TestCase):
    """Unit Test Cases"""
    def test_import_data(self):
        """Test importing three csv files"""
        drop_collection()
        
        test_file_errors = import_data('products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(test_file_errors[0], (0, 0, 0))

    def test_insert_collection_many(self):
        """Test loading dictionaries into mongodb collections"""
        drop_collection()

        total_insert_errors = import_data('products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(total_insert_errors[1], (0, 0, 0))

    def test_show_available_products(self):
        drop_collection()
        
        import_data('products.csv', 'customers.csv', 'rentals.csv')

        """Test results are all available products"""
        Actual_results = {
                            'prod001': {
                                'description': 'Big Sofa',
                                'product_type': 'Livingroom',
                                'quantity_available': '5'
                            },
                            'prod002': {
                                'description': 'TV Stand',
                                'product_type': 'Livingroom',
                                'quantity_available': '5'
                            },
                            'prod003': {
                                'description': 'TV',
                                'product_type': 'Livingroom',
                                'quantity_available': '3'
                            },
                            'prod004': {
                                'description': 'Table',
                                'product_type': 'Livingroom',
                                'quantity_available': '2'
                            }
                        }

        return_dict = show_available_products()
        self.assertEqual(Actual_results, return_dict)

    def test_show_rentals(self):
        """Test results are showing rentals with specified product id"""
        drop_collection()
        
        import_data('products.csv', 'customers.csv', 'rentals.csv')
        
        """Test results are for all available products"""
        Actual_results = {
                            'user001': {
                                'name': 'Fred Flintstone',
                                'address': '123 Bedrock St',
                                'phone_number': '305-555-1212',
                                'email_address': 'fflint@aol.com'
                            },
                            'user004': {
                                'name': 'Bamm-Bamm Rubble',
                                'address': '456 Bedrock St',
                                'phone_number': '305-555-3434',
                                'email_address': 'bam@yahoo.com'
                            }
                        }

        return_dict = show_rentals('prod001')
        self.assertEqual(Actual_results, return_dict)
        drop_collection()    