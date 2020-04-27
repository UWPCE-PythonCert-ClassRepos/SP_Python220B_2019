#!/usr/bin/env python
"""
Unit tests.
"""

import os
import sys

os.chdir('..')
sys.path.append(os.getcwd())
src_dir = os.getcwd() + '/src_data/'

from unittest import TestCase
from unittest.mock import patch
from io import StringIO
from database import *
from pymongo import MongoClient

key_seq = ['1', '2', '', '', '', '', '3', '4', '5', 'PID9997', '6', '3', '9998', '998', '98']


class FunctionTests(TestCase):
    """
    Test the main menu and UI.
    """
    # db_instantiation = DBFunctions()
    attrs_dict = {'print_database': print_database, 'import_data': import_data,
                       'clear_data': clear_data, 'show_available_products': show_available_products,
                       'show_rentals': show_rentals}
    DBFunctions = type('DBFunctions', (object,), attrs_dict)

    def setUp(self):
        mongo_client = MongoClient('mongodb://localhost:27017')
        mongo_client.drop_database('products_database')
        self.maxDiff = None

    @patch('sys.stdout', new_callable=StringIO)
    def test_write_data(self, mock_stdout):
        """
        Confirm behavior for multiprocessing process
        """
        self.DBFunctions.import_data(self, src_dir, 'product_file_old.csv', 'customer_file_old.csv', 'rental_file_old.csv', call_inner=True)#(src_dir + 'product_file_old.csv', [], [], [], 0)
        with patch('builtins.input'):
            self.DBFunctions.print_database(self)
            self.assertEqual(mock_stdout.getvalue(), """Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'products_database'), 'products')
{'product_id': 'LR001', 'description': '55in TV', 'product_type': 'Living Room', 'quantity_available': '15', 'daily_rate': '3'}
{'product_id': 'LR002', 'description': '65in TV', 'product_type': 'Living Room', 'quantity_available': '0', 'daily_rate': '4'}
{'product_id': 'BD002', 'description': 'Queen Bed', 'product_type': 'Bedroom', 'quantity_available': '12', 'daily_rate': '2'}
{'product_id': 'BD001', 'description': 'Full Bed', 'product_type': 'Bedroom', 'quantity_available': '40', 'daily_rate': '1'}
{'product_id': 'OF001', 'description': 'Desk + Chair', 'product_type': 'Office', 'quantity_available': '26', 'daily_rate': '1'}
{'product_id': 'DN002', 'description': 'Dining Table + 6 Chair', 'product_type': 'Dining Room', 'quantity_available': '8', 'daily_rate': '3'}
{'product_id': 'DN001', 'description': 'Dining Table + 4 Chair', 'product_type': 'Dining Room', 'quantity_available': '0', 'daily_rate': '2'}
{'product_id': 'LR003', 'description': 'Sofa', 'product_type': 'Living Room', 'quantity_available': '17', 'daily_rate': '2'}
Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'products_database'), 'customers')
Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'products_database'), 'rentals')
""")

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_1(self, mock_stdout):
        """
        Confirm behavior for main menu handling of option 1.
        """
        # DBFunctions = type('DBFunctions', (object,), self.attrs_dict)
        with patch('builtins.input', side_effect=key_seq[0:1]):
            main_menu(self.attrs_dict)
            self.assertEqual(mock_stdout.getvalue(), """Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
              '6' - Timing run
              'q' - Quit
Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'products_database'), 'products')
Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'products_database'), 'customers')
Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'products_database'), 'rentals')
""")

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_2(self, mock_stdout):
        """
        Confirm behavior for main menu handling of option 1.
        """
        with patch('builtins.input', side_effect=key_seq[1:6]):
            main_menu(self.attrs_dict)
            self.assertEqual(mock_stdout.getvalue(), """Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
              '6' - Timing run
              'q' - Quit
total rows/documents = (9999, 9999, 9999)   invalid rows/documents(blank entries aside from end_date) = (1, 0, 1)
""")

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_3(self, mock_stdout):
        """
        Confirm behavior for main menu handling of option 1.
        """
        with patch('builtins.input', side_effect=key_seq[6:7]):
            main_menu(self.attrs_dict)
            self.assertEqual(mock_stdout.getvalue(), """Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
              '6' - Timing run
              'q' - Quit
products_database dropped
""")

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_4(self, mock_stdout):
        """
        Confirm behavior for main menu handling of option 1.
        """
        self.DBFunctions.import_data(self, src_dir, 'product_file_old.csv', 'customer_file_old.csv', 'rental_file_old.csv')
        with patch('builtins.input', side_effect=key_seq[7:8]):
            main_menu(self.attrs_dict)
            self.assertEqual(mock_stdout.getvalue(), """total rows/documents = (8, 5, 15)   invalid rows/documents(blank entries aside from end_date) = (1, 0, 1)
Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
              '6' - Timing run
              'q' - Quit
  P_ID  |         DESCRIPTION          |   PRODUCT TYPE   | QTY |RATE
---------------------------------------------------------------------
  LR001 |           55in TV            |   Living Room    | 15  | 3  
  BD002 |          Queen Bed           |     Bedroom      | 12  | 2  
  BD001 |           Full Bed           |     Bedroom      | 40  | 1  
  OF001 |         Desk + Chair         |      Office      | 26  | 1  
  DN002 |    Dining Table + 6 Chair    |   Dining Room    |  8  | 3  
  LR003 |             Sofa             |   Living Room    | 17  | 2  
""")

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_5(self, mock_stdout):
        """
        Confirm behavior for main menu handling of option 1.
        """
        self.DBFunctions.import_data(self, src_dir, 'product_file.csv', 'customer_file.csv', 'rental_file.csv')
        with patch('builtins.input', side_effect=key_seq[8:10]):
            main_menu(self.attrs_dict)
            self.assertEqual(mock_stdout.getvalue(), """total rows/documents = (9999, 9999, 9999)   invalid rows/documents(blank entries aside from end_date) = (1, 0, 1)
Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
              '6' - Timing run
              'q' - Quit
  usrID |             NAME             |                     ADDRESS                      |   PHONE    |          EMAIL          
---------------------------------------------------------------------------------------------------------------------------------
 CID0907|      last907, first907       |                   address0907                    | 5553332018 |     email0907@xx.xx     
 CID0646|      last646, first646       |                   address0646                    | 5553331757 |     email0646@xx.xx     
 CID1530|     last1530, first1530      |                   address1530                    | 5553332641 |     email1530@xx.xx     
""")

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_6(self, mock_stdout):
        """
        Confirm behavior for main menu handling of option 1.
        """
        with patch('builtins.input', side_effect=key_seq[10:15]):
            main_menu(self.attrs_dict)
            self.assertEqual(mock_stdout.getvalue(), """Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
              '6' - Timing run
              'q' - Quit
products_database dropped
total rows/documents = (9998, 9998, 9998)   invalid rows/documents(blank entries aside from end_date) = (0, 0, 0)
products_database dropped
total rows/documents = (998, 998, 998)   invalid rows/documents(blank entries aside from end_date) = (0, 0, 0)
products_database dropped
total rows/documents = (98, 98, 98)   invalid rows/documents(blank entries aside from end_date) = (0, 0, 0)
""")