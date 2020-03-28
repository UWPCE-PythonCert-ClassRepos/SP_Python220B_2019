#!/usr/bin/env python
"""
Unit tests.
"""

from unittest import TestCase
import os
import sys

os.chdir('..')
sys.path.append(os.getcwd())

from basic_operations import *
from customer_model import *
import sqlite3
import load_database

customers = [
        ('JF0001', 'Jarron', 'Fondue', '1234 A St NW, Nowhere, HH 12345', '1234567890',
         'jafo@who.xx', 'active', '20000'),
        ('SC0198', 'Stormy', 'Calmy', '1234 Z St SE, Somewhere, HH 23456', '1112223333',
         'acts@what.xx', 'active', '15000'),
        ('DK7621', 'Dana', 'Kabar', '1234 BB Dr SE, Here, HH 23456', '1112225555',
         'AK_AD@where.xx', 'inactive', '12000'),
        ('JT0198', 'John', 'Tigger', '1234 K St SW, Somewhere, HH 23456', '1112224444',
         'actsup@what.xx', 'active', '7000')
        ]


class FunctionTests(TestCase):

    def setUp(self):
        database = SqliteDatabase('customers.db')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        database.drop_tables([Customer])
        database.create_tables([Customer])
        self.conn = sqlite3.connect('customers.db')
        self.conn.execute('PRAGMA foreign_keys = ON;')

    def tearDown(self):
        database.close()

    def test_add_customer_pass(self):
        """
        Confirm that a customer can be added.
        """
        add_customer(customers[0][0], customers[0][1], customers[0][2], customers[0][3],
                     customers[0][4], customers[0][5], customers[0][6], customers[0][7])
        cursor = self.conn.execute('SELECT * FROM Customer;')
        results = cursor.fetchall()
        self.assertEqual('|'.join(results[0]), 'JF0001|Jarron|Fondue|1234 A St NW, Nowhere, HH '
                         '12345|1234567890|jafo@who.xx|active|20000')

    def test_add_customer_fail_id(self):
        """
        Confirm that adding a customer with an improperly formatted ID will result in no addition.
        """
        add_customer('225555', customers[0][1], customers[0][2], customers[0][3],
                     customers[0][4], customers[0][5], customers[0][6], customers[0][7])
        cursor = self.conn.execute('SELECT * FROM Customer;')
        results = cursor.fetchall()
        self.assertEqual(results, [])

    def test_add_customer_fail_phone(self):
        """
        Confirm that adding a customer with an improperly formatted phone# will result in no addition.
        """
        add_customer(customers[0][0], customers[0][1], customers[0][2], customers[0][3],
                     '8675309', customers[0][5], customers[0][6], customers[0][7])
        cursor = self.conn.execute('SELECT * FROM Customer;')
        results = cursor.fetchall()
        self.assertEqual(results, [])

    def test_add_customer_fail_status(self):
        """
        Confirm that adding a customer with a status besides 'active' or 'inactive' results in no addition.
        """
        add_customer(customers[0][0], customers[0][1], customers[0][2], customers[0][3],
                     customers[0][4], customers[0][5], 'passive', customers[0][7])
        cursor = self.conn.execute('SELECT * FROM Customer;')
        results = cursor.fetchall()
        self.assertEqual(results, [])

    def test_search_customer_pass(self):
        """
        Confirm that a customer can be searched.
        """
        add_customer(customers[1][0], customers[1][1], customers[1][2], customers[1][3],
                     customers[1][4], customers[1][5], customers[1][6], customers[1][7])
        self.assertEqual(search_customer('SC0198'), {'name': 'Stormy', 'last_name': 'Calmy',
                         'email_address': 'acts@what.xx', 'phone_number': '1112223333', 
                         'credit_limit': '15000'})

    def test_search_customer_fail(self):
        """
        Confirm that searching a customer with an incorrect id will result in an empty dict.
        """
        add_customer(customers[2][0], customers[2][1], customers[2][2], customers[2][3],
                     customers[2][4], customers[2][5], customers[2][6], customers[2][7])
        self.assertEqual(search_customer('SC0198'), {})

    def test_delete_customer_pass(self):
        """
        Confirm a customer can be deleted.
        """
        add_customer(customers[2][0], customers[2][1], customers[2][2], customers[2][3],
                     customers[2][4], customers[2][5], customers[2][6], customers[2][7])
        delete_customer('DK7621')
        cursor = self.conn.execute('SELECT * FROM Customer;')
        results = cursor.fetchall()
        self.assertEqual(results, [])

    def test_delete_customer_fail(self):
        """
        Confirm that deleting a customer with an incorrect id will result in the database unchanged.
        """
        add_customer(customers[2][0], customers[2][1], customers[2][2], customers[2][3],
                     customers[2][4], customers[2][5], customers[2][6], customers[2][7])
        delete_customer('JT0198')
        cursor = self.conn.execute('SELECT * FROM Customer;')
        results = cursor.fetchall()
        self.assertEqual(results, [('DK7621', 'Dana', 'Kabar', '1234 BB Dr SE, Here, HH 23456',
                                    '1112225555', 'AK_AD@where.xx', 'inactive', '12000')])

    def test_update_customer_credit_limit_pass(self):
        """
        Confirm that an existing customer credit limit can be changed.
        """
        add_customer(customers[3][0], customers[3][1], customers[3][2], customers[3][3],
                     customers[3][4], customers[3][5], customers[3][6], customers[3][7])
        update_customer_credit('JT0198', '9999')
        cursor = self.conn.execute('SELECT * FROM Customer;')
        results = cursor.fetchall()
        self.assertEqual(results, [('JT0198', 'John', 'Tigger', 
                                    '1234 K St SW, Somewhere, HH 23456', '1112224444', 
                                    'actsup@what.xx', 'active', '9999')])

    def test_update_customer_credit_limit_fail(self):
        """
        Confirm that changing a customer's credit limit to a mixed character value will result in no change.
        """
        add_customer(customers[3][0], customers[3][1], customers[3][2], customers[3][3],
                     customers[3][4], customers[3][5], customers[3][6], customers[3][7])
        update_customer_credit('JT0198', '999p')
        cursor = self.conn.execute('SELECT * FROM Customer;')
        results = cursor.fetchall()
        self.assertEqual(results, [('JT0198', 'John', 'Tigger', 
                                    '1234 K St SW, Somewhere, HH 23456', '1112224444', 
                                    'actsup@what.xx', 'active', '7000')])

    def test_list_active_customers_pass(self):
        """
        Confirm that the number of active an inactive customers will be properly returned.
        """
        load_database.add_customers()
        self.assertEqual(list_active_customers(), (3, 1))