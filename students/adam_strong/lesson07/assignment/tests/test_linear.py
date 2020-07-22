#!/usr/bin/env python

"""
    Tests for the database instantiator, customer_models and basic operations

"""
from unittest import TestCase
import sys
sys.path.append('..')
from linear import *

AVAILABLE = {'PD5X': {'Product Code': 'PD5X', 'Quantity Available': '12',
                      'Description': 'Power Drill 5Xt', 'Product Type': 'Tools'},
             'SLD2': {'Product Code': 'SLD2', 'Quantity Available': '20',
                      'Description': 'Solar Lamp D2', 'Product Type': 'Electric'}, 
             'SLEDX': {'Product Code': 'SLEDX', 'Quantity Available': '8',
                       'Description': 'Solar LED X50', 'Product Type': 'Electric'},
             'COU': {'Product Code': 'COU', 'Quantity Available': '2',
                     'Description': 'Blue Couch', 'Product Type': 'Furniture'},
             'SCRS': {'Product Code': 'SCRS', 'Quantity Available': '12',
                      'Description': 'Screwdriver Set', 'Product Type': 'Tools'},
             'CWD5': {'Product Code': 'CWD5', 'Quantity Available': '1',
                      'Description': 'Cleanswell Drier', 'Product Type': 'Electric'},
             'CWW1': {'Product Code': 'CWW1', 'Quantity Available': '3',
                      'Description': 'Cleanswell Washer', 'Product Type': 'Electric'}}

ALL = {'PD5X': {'Product Code': 'PD5X', 'Quantity Available': '12',
                'Description': 'Power Drill 5Xt', 'Product Type': 'Tools'},
       'SLD2': {'Product Code': 'SLD2', 'Quantity Available': '20',
                'Description': 'Solar Lamp D2', 'Product Type': 'Electric'},
       'SLEDX': {'Product Code': 'SLEDX', 'Quantity Available': '8',
                 'Description': 'Solar LED X50', 'Product Type': 'Electric'},
       'COU': {'Product Code': 'COU', 'Quantity Available': '2',
               'Description': 'Blue Couch', 'Product Type': 'Furniture'},
       'SCRS': {'Product Code': 'SCRS', 'Quantity Available': '12',
                'Description': 'Screwdriver Set', 'Product Type': 'Tools'},
       'CWD5': {'Product Code': 'CWD5', 'Quantity Available': '1',
                'Description': 'Cleanswell Drier', 'Product Type': 'Electric'},
       'CWW1': {'Product Code': 'CWW1', 'Quantity Available': '3',
                'Description': 'Cleanswell Washer', 'Product Type': 'Electric'},
       'CW8000': {'Product Code': 'CW8000', 'Quantity Available': '0',
                  'Description': 'Cleanswell 8000', 'Product Type': 'Electric'}}

SHOW_2USERS = {'user008': {'User ID': 'user008', 'Name': 'Carrie Baker', 'Address': '981 Main St.',
                           'Phone': '425-444-4444', 'Email': 'cbaker23@fakemail.com'},
               'user001': {'User ID': 'user001', 'Name': 'John Jacboson', 'Address': '123 Fake Street',
                           'Phone': '206-848-8987', 'Email': 'johnjohn@hotmail.com'}}

SHOW_1USER = {'user008': {'User ID': 'user008', 'Name': 'Carrie Baker', 'Address': '981 Main St.',
                          'Phone': '425-444-4444', 'Email': 'cbaker23@fakemail.com'}}

class DataTransfer(TestCase):
    '''Testing that the data is imported from csvs and placed in a mongo db'''

    def test_importing(self):
        '''Ensures that two tuples are returned with predetermined values and that the 
        final value in each tuple is a float (from the time.time() calculation'''
        import_report = import_data(DIRECTORY_NAME, PRODUCT_FILE, CUSTOMER_FILE, RENTALS_FILE)
        assert import_report[0][0] == 0
        assert import_report[0][1] == 10
        assert import_report[0][2] == 10
        assert type(import_report[0][3]) is float
        assert import_report[1][0] == 0
        assert import_report[1][1] == 8
        assert import_report[1][2] == 8
        assert type(import_report[1][3]) is float

class DatabaseQueries(TestCase):
    '''Testing that a database is created'''

    def setUp(self):
        '''Get the database instantiated with imported csv'''
        import_data(DIRECTORY_NAME, PRODUCT_FILE, CUSTOMER_FILE, RENTALS_FILE)

    def test_available_products(self):
        '''Tests the instantiation of the database'''
        available_products = show_available_products()
        assert available_products == AVAILABLE

    def test_all_products(self):
        '''Tests the show_all_products function'''
        all_products = show_all_products()
        assert all_products == ALL

    def test_show_rentals_2USERS(self):
        '''Tests show_rentals() with 2 match'''
        history = show_rentals('SLD2')
        assert history == SHOW_2USERS

    def test_show_rentals_1USER(self):
        '''Tests show_rentals() with 1 match'''
        history = show_rentals('SLEDX')
        assert history == SHOW_1USER

    def tearDown(self):
        '''Delete the data from the mongoDB'''
        delete_db()