# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 11:40:35 2019

@author: Humberto
"""
# pylint: disable = invalid-name

from unittest import TestCase
from assignment import database as main

class TestDatabase(TestCase):
    """Tests the functionality of the Mongo Database
    """

    def setUp(self):
        """Setting up the database for the tests"""

        mongo = main.MongoDBConnection()
        with mongo:
            db = mongo.connection.storeDB
            #clearing the databases for testing purposes
            db["customers"].drop()
            db["products"].drop()
            db["rentals"].drop()

    def tearDown(self):
        """Tearing down anything created or used for testing purposes"""

        mongo = main.MongoDBConnection()
        with mongo:
            db = mongo.connection.storeDB
            #clearing the databases for testing purposes
            db["customers"].drop()
            db["products"].drop()
            db["rentals"].drop()

    def test_import_data(self):
        """Testing the import_data funtion"""
        directory_name = "./csv_files"
        product_file = "products.csv"
        customer_file = "customers.csv"
        rentals_file = "rentals.csv"

        results = main.import_data(directory_name, product_file,
                                   customer_file, rentals_file)

        compare = ((4, 6, 4),
                   (0, 0, 0))

        self.assertEqual(results, compare)

    def test_show_available_products(self):
        """Testing functionality of showing all available products in the database"""

        directory_name = "./csv_files"
        product_file = "products.csv"
        customer_file = "customers.csv"
        rentals_file = "rentals.csv"

        main.import_data(directory_name, product_file,
                         customer_file, rentals_file)

        results = main.show_available_products()

        compare = {"prd001":{"description":"65-Inch TV",
                             "product_type":"livingroom",
                             "quantity_available":"5"},
                   "prd003":{"description":"Queen Bed",
                             "product_type":"bedroom",
                             "quantity_available":"4"},
                   "prd005":{"description":"Dish Washer",
                             "product_type":"kitchen",
                             "quantity_available":"3"}}

        self.assertEqual(results, compare)

    def test_show_rentals(self):
        """Testing the functionality of showing all users who rented a given product"""

        directory_name = "./csv_files"
        product_file = "products.csv"
        customer_file = "customers.csv"
        rentals_file = "rentals.csv"

        main.import_data(directory_name, product_file,
                         customer_file, rentals_file)

        results = main.show_rentals("prd002")

        compare = {'user004': {'user_id': 'user004',
                               'name': 'Luke Organa',
                               'address': '1235 Aldern Lane',
                               'phone_number': '4796268775',
                               'email': 'sw@storm.net'},
                   'user002': {'user_id': 'user002',
                               'name': 'Anna Light',
                               'address': '568 Elder Road',
                               'phone_number': '5612378451',
                               'email': 'anna@yahoo.com'}}

        self.assertEqual(results, compare)
