#!/usr/bin/env python
"""
Integration test.
"""

from unittest import TestCase
from unittest.mock import patch
from io import StringIO
import os
import sys

os.chdir('..')
sys.path.append(os.getcwd())

from basic_operations import *
from customer_model import *
import sqlite3

key_seq = ['1', 'JF0001', 'Jarron', 'Fondue', '1234 A St NW, Nowhere, HH 12345', '1234567890',
           'jafo@who.xx', 'active', '20000', '1', 'SC0198', 'Stormy', 'Calmy',
           '1234 Z St SE, Somewhere, HH 23456', '1112223333', 'acts@what.xx', 'active', '15000',
           '2', 'JF0001', '3', 'JF0001', '4', 'SC0198', '5555', '5']

main_passes = key_seq.count('1') + key_seq.count('2') + key_seq.count('3') + key_seq.count('4')\
    + key_seq.count('5')


class IntegrationTest(TestCase):

    def setUp(self):
        database = SqliteDatabase('customers.db')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        database.drop_tables([Customer])
        database.create_tables([Customer])
        self.conn = sqlite3.connect('customers.db')
        self.conn.execute('PRAGMA foreign_keys = ON;')
        self.maxDiff = None

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_(self, mock_stdout):
        with patch('builtins.input', side_effect=key_seq):
            for i in range(main_passes):
                main_menu()
            cursor = self.conn.execute('SELECT * FROM Customer;')
            results = cursor.fetchall()
            self.assertEqual('|'.join(results[0]), 'SC0198|Stormy|Calmy|1234 Z St SE, Somewhere, '
                             'HH 23456|1112223333|acts@what.xx|active|5555')
            self.assertEqual(mock_stdout.getvalue(), """Please choose from the following:
              '1' - Add a new customer
              '2' - Search a customer
              '3' - Delete a customer
              '4' - Update customer credit
              '5' - List active customers
              'q' - Quit
Please provide the following customer information:
Please choose from the following:
              '1' - Add a new customer
              '2' - Search a customer
              '3' - Delete a customer
              '4' - Update customer credit
              '5' - List active customers
              'q' - Quit
Please provide the following customer information:
Please choose from the following:
              '1' - Add a new customer
              '2' - Search a customer
              '3' - Delete a customer
              '4' - Update customer credit
              '5' - List active customers
              'q' - Quit
{'name': 'Jarron', 'last_name': 'Fondue', 'email_address': 'jafo@who.xx', 'phone_number': '1234567890', 'credit_limit': '20000'}
Please choose from the following:
              '1' - Add a new customer
              '2' - Search a customer
              '3' - Delete a customer
              '4' - Update customer credit
              '5' - List active customers
              'q' - Quit
Please choose from the following:
              '1' - Add a new customer
              '2' - Search a customer
              '3' - Delete a customer
              '4' - Update customer credit
              '5' - List active customers
              'q' - Quit
Please choose from the following:
              '1' - Add a new customer
              '2' - Search a customer
              '3' - Delete a customer
              '4' - Update customer credit
              '5' - List active customers
              'q' - Quit
(active_customers, inactive_customers) = (1, 0)
""")
