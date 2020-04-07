#!/usr/bin/env python
"""
Unit tests.
"""
from unittest import TestCase
from unittest.mock import patch
from io import StringIO
import os
import sys

os.chdir('..')
sys.path.append(os.getcwd())
src_dir = os.getcwd() + '/src_data/'

from linear import *
from pymongo import MongoClient

key_seq = ['1', '2', '', '', '', '', '3', '4', '5', 'PID9997']

class FunctionTests(TestCase):#, MongoDBConnection):
    """
    Test the main menu and UI.
    """
    def setUp(self):
        mongo_client = MongoClient('mongodb://localhost:27017')
        mongo_client.drop_database('products_database')
        self.maxDiff = None

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_database(self, mock_stdout):
        """
        Confirm database creation by verifying print output.
        """
        import_data(src_dir, 'product_file_old.csv', 'customer_file_old.csv', 'rental_file_old.csv')
        with patch('builtins.input'):
            print_database()
            self.assertEqual(mock_stdout.getvalue(), """total rows/documents = (8, 5, 15)   invalid rows/documents(blank entries aside from end_date) = (1, 0, 1)
Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'products_database'), 'products')
{'product_id': 'LR001', 'description': '55in TV', 'product_type': 'Living Room', 'quantity_available': '15', 'daily_rate': '3'}
{'product_id': 'LR002', 'description': '65in TV', 'product_type': 'Living Room', 'quantity_available': '0', 'daily_rate': '4'}
{'product_id': 'BD002', 'description': 'Queen Bed', 'product_type': 'Bedroom', 'quantity_available': '12', 'daily_rate': '2'}
{'product_id': 'BD001', 'description': 'Full Bed', 'product_type': 'Bedroom', 'quantity_available': '40', 'daily_rate': '1'}
{'product_id': 'OF001', 'description': 'Desk + Chair', 'product_type': 'Office', 'quantity_available': '26', 'daily_rate': '1'}
{'product_id': 'DN002', 'description': 'Dining Table + 6 Chair', 'product_type': 'Dining Room', 'quantity_available': '8', 'daily_rate': '3'}
{'product_id': 'DN001', 'description': 'Dining Table + 4 Chair', 'product_type': 'Dining Room', 'quantity_available': '0', 'daily_rate': '2'}
{'product_id': 'LR003', 'description': 'Sofa', 'product_type': 'Living Room', 'quantity_available': '17', 'daily_rate': '2'}
Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'products_database'), 'customers')
{'user_id': 'AB001', 'name': 'Anderson, Bob', 'address': '123 A St NW, Somewhere, HH 12345', 'phone_number': '5554443333', 'email': 'b_ando@bla.xx'}
{'user_id': 'DE003', 'name': 'Dork, Either', 'address': '334 H Dr SE, There, HH 12378', 'phone_number': '5553331122', 'email': 'darkeither@blabla.xx'}
{'user_id': 'FB901', 'name': 'Farstriker, Gopollo', 'address': '889 Hat Ave NE, Somewhere, HH 12345', 'phone_number': '5554446666', 'email': 'gof@blablabla.xx'}
{'user_id': 'GH040', 'name': 'Greenwich, Heather', 'address': '927 Watch Ave W, Nowhere, HH 12367', 'phone_number': '5557778888', 'email': 'thetime@bla.xx'}
{'user_id': 'HI006', 'name': 'Hollow, India', 'address': '700 Giraffe Dr N, Somehwere, HH 12345', 'phone_number': '5557651234', 'email': 'noeye@blabla.xx'}
Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'products_database'), 'rentals')
{'rental_id': '1', 'user_id': 'HI006', 'product_id': 'BD001', 'quantity_rented': '4', 'start_date': '2018-01-02', 'end_date': '2022-01-02'}
{'rental_id': '2', 'user_id': 'HI006', 'product_id': 'OF001', 'quantity_rented': '4', 'start_date': '2018-01-02', 'end_date': '2022-01-02'}
{'rental_id': '3', 'user_id': 'DE003', 'product_id': 'BD001', 'quantity_rented': '1', 'start_date': '2017-08-01', 'end_date': ''}
{'rental_id': '4', 'user_id': 'AB001', 'product_id': 'BD002', 'quantity_rented': '3', 'start_date': '2019-07-15', 'end_date': '2020-07-15'}
{'rental_id': '5', 'user_id': 'AB001', 'product_id': 'OF001', 'quantity_rented': '1', 'start_date': '2019-07-15', 'end_date': '2020-07-15'}
{'rental_id': '6', 'user_id': 'AB001', 'product_id': 'DN001', 'quantity_rented': '1', 'start_date': '2019-07-15', 'end_date': '2020-07-15'}
{'rental_id': '7', 'user_id': 'FB901', 'product_id': 'BD001', 'quantity_rented': '2', 'start_date': '2020-01-05', 'end_date': '2021-08-01'}
{'rental_id': '8', 'user_id': 'FB901', 'product_id': 'OF001', 'quantity_rented': '2', 'start_date': '2020-01-05', 'end_date': '2021-08-01'}
{'rental_id': '9', 'user_id': 'FB901', 'product_id': 'DN001', 'quantity_rented': '1', 'start_date': '2020-01-05', 'end_date': '2021-08-01'}
{'rental_id': '10', 'user_id': 'GH040', 'product_id': 'BD001', 'quantity_rented': '1', 'start_date': '2020-02-01', 'end_date': '2022-02-01'}
{'rental_id': '11', 'user_id': 'GH040', 'product_id': 'OF001', 'quantity_rented': '1', 'start_date': '2020-02-01', 'end_date': '2022-02-01'}
{'rental_id': '12', 'user_id': 'GH040', 'product_id': 'LR001', 'quantity_rented': '1', 'start_date': '2020-02-01', 'end_date': '2022-02-01'}
{'rental_id': '13', 'user_id': 'GH040', 'product_id': 'DN002', 'quantity_rented': '1', 'start_date': '2020-02-01', 'end_date': '2022-02-01'}
{'rental_id': '14', 'user_id': 'AB001', 'product_id': 'LR002', 'quantity_rented': '1', 'start_date': '2019-07-30', 'end_date': '2020-07-15'}
{'rental_id': '15', 'user_id': 'AB001', 'product_id': 'LR003', 'quantity_rented': '1', 'start_date': '2019-07-30', 'end_date': '2020-07-15'}
""")

    def test_import_data(self):
        """
        Confirm correct tuple output of import_data.
        """
        self.assertEqual(import_data(src_dir, 'product_file.csv', 'customer_file.csv', 'rental_file.csv'), ((9999, 9999, 9999), (1, 0, 1)))

    def test_clear_data(self):
        """
        Confirm the products database clears.
        """
        import_data(src_dir, 'product_file.csv', 'customer_file.csv', 'rental_file.csv')
        self.assertNotIn('products_database', clear_data())

    def test_show_available_products(self):
        """
        Confirm correct screening for available products only (nonzero quantity available).
        """
        import_data(src_dir, 'product_file_old.csv', 'customer_file_old.csv', 'rental_file_old.csv')
        self.assertEqual(show_available_products(), {'LR001': {'description': '55in TV', 'product_type': 'Living Room', 'quantity_available': '15', 'daily_rate': '3'},
'BD002': {'description': 'Queen Bed', 'product_type': 'Bedroom', 'quantity_available': '12', 'daily_rate': '2'},
'BD001': {'description': 'Full Bed', 'product_type': 'Bedroom', 'quantity_available': '40', 'daily_rate': '1'},
'OF001': {'description': 'Desk + Chair', 'product_type': 'Office', 'quantity_available': '26', 'daily_rate': '1'},
'DN002': {'description': 'Dining Table + 6 Chair', 'product_type': 'Dining Room', 'quantity_available': '8', 'daily_rate': '3'},
'LR003': {'description': 'Sofa', 'product_type': 'Living Room', 'quantity_available': '17', 'daily_rate': '2'}})

    def test_show_rentals(self):
        """
        Confirm correct screening for customers by product ID..
        """
        import_data(src_dir, 'product_file.csv', 'customer_file.csv', 'rental_file.csv')
        self.assertEqual(show_rentals('PID9997'), {'CID0907': {'name': 'last907, first907',
                         'address': 'address0907', 'phone_number': '5553332018',
                         'email': 'email0907@xx.xx'}, 'CID0646': {'name': 'last646, first646',
                         'address': 'address0646', 'phone_number': '5553331757',
                         'email': 'email0646@xx.xx'}, 'CID1530': {'name': 'last1530, first1530',
                         'address': 'address1530', 'phone_number': '5553332641',
                         'email': 'email1530@xx.xx'}})

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_1(self, mock_stdout):
        """
        Confirm behavior for main menu handling of option 1.
        """
        with patch('builtins.input', side_effect=key_seq[0:1]):
            main_menu()
            self.assertEqual(mock_stdout.getvalue(), """Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
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
            main_menu()
            self.assertEqual(mock_stdout.getvalue(), """Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
              'q' - Quit
total rows/documents = (9999, 9999, 9999)   invalid rows/documents(blank entries aside from end_date) = (1, 0, 1)
""")

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_3(self, mock_stdout):
        """
        Confirm behavior for main menu handling of option 1.
        """
        with patch('builtins.input', side_effect=key_seq[6:7]):
            main_menu()
            self.assertEqual(mock_stdout.getvalue(), """Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
              'q' - Quit
products_database dropped
""")

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_4(self, mock_stdout):
        """
        Confirm behavior for main menu handling of option 1.
        """
        import_data(src_dir, 'product_file_old.csv', 'customer_file_old.csv', 'rental_file_old.csv')
        with patch('builtins.input', side_effect=key_seq[7:8]):
            main_menu()
            self.assertEqual(mock_stdout.getvalue(), """total rows/documents = (8, 5, 15)   invalid rows/documents(blank entries aside from end_date) = (1, 0, 1)
Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
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
        import_data(src_dir, 'product_file.csv', 'customer_file.csv', 'rental_file.csv')
        with patch('builtins.input', side_effect=key_seq[8:10]):
            main_menu()
            self.assertEqual(mock_stdout.getvalue(), """total rows/documents = (9999, 9999, 9999)   invalid rows/documents(blank entries aside from end_date) = (1, 0, 1)
Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
              'q' - Quit
  usrID |             NAME             |                     ADDRESS                      |   PHONE    |          EMAIL          
---------------------------------------------------------------------------------------------------------------------------------
 CID0907|      last907, first907       |                   address0907                    | 5553332018 |     email0907@xx.xx     
 CID0646|      last646, first646       |                   address0646                    | 5553331757 |     email0646@xx.xx     
 CID1530|     last1530, first1530      |                   address1530                    | 5553332641 |     email1530@xx.xx     
""")
