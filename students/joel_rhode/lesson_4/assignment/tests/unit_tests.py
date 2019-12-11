"""
Contains unit tests for the basic_operations file for interacting with the customer database.
"""
# pylint: disable=unused-argument, no-value-for-parameter

from unittest import TestCase
from unittest.mock import patch
from io import StringIO
import peewee

import basic_operations
from basic_operations import (add_customer, search_customer, delete_customer,
                              update_customer_credit, list_active_customers,
                              report_single_customer, report_all_customers,
                              report_customers_by_status)
from customer_model import Customer, DATABASE as database

TEST_DATABASE = 'test.db'


class BasicOperationsUnitTests(TestCase):
    """Tests for each function in basic_operations.py."""
    def setUp(self):
        """Defines starting test database used for function testing."""
        self.starting_db = [(1, 'Bob', 'Bobbo', '12 Green St', '1112223344',
                        'bobbo@python.org', False, 85000),
                       (2, 'Jane', 'Janeo', '1550 Red Rd', '1118675309',
                        'jane@therealjane.com', True, 150000),
                       (5, 'Wilson', 'Volleyball', '1 Castaway Island', '0000000000',
                        'wilson@ImLost.com', True, 0)
                       ]
        database.init(TEST_DATABASE)
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON')
        database.create_tables([Customer])
        with database.transaction():
            Customer.delete().execute()
            Customer.insert_many(self.starting_db, fields=[Customer.customer_id, Customer.name,
                                                           Customer.lastname, Customer.home_address,
                                                           Customer.phone_number,
                                                           Customer.email_address,
                                                           Customer.active_status,
                                                           Customer.credit_limit
                                                           ]).execute()
        database.close()


    @patch('basic_operations.DATABASE_NAME')
    def test_add_customer(self, mock_database):
        """Testing adding a customer to the database via add_customer function."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        add_customer(17, 'Bob', 'Testy', '111 Test St', 1234567890, 'bob@thetest.net', True, 70000)
        test_customer = Customer.get_by_id(17)
        self.assertEqual(test_customer.name, 'Bob')
        self.assertEqual(test_customer.lastname, 'Testy')
        self.assertEqual(test_customer.home_address, '111 Test St')
        self.assertEqual(test_customer.phone_number, '1234567890')
        self.assertEqual(test_customer.email_address, 'bob@thetest.net')
        self.assertEqual(test_customer.active_status, True)
        self.assertEqual(test_customer.credit_limit, 70000)

        self.assertFalse(add_customer(17, 'Bob', 'Testy', '111 Test St', 1234567890,
                                      'bob@thetest.net', True, 70000))


    @patch('basic_operations.DATABASE_NAME')
    def test_search_customer(self, mock_database):
        """Testing searching a customer to the database via search_customer function."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        exp_dict = {
            'name': 'Wilson',
            'lastname': 'Volleyball',
            'email_address': 'wilson@ImLost.com',
            'phone_number': '0000000000'
            }
        self.assertDictEqual(search_customer(5), exp_dict)
        self.assertDictEqual(search_customer(3), {})


    @patch('basic_operations.DATABASE_NAME')
    def test_delete_customer(self, mock_database):
        """Testing deleting a customer to the database via delete_customer function."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        self.assertTrue(delete_customer(1))
        with self.assertRaises(peewee.DoesNotExist):
            Customer.get_by_id(1)
        self.assertFalse(delete_customer(3))


    @patch('basic_operations.DATABASE_NAME')
    def test_update_customer_credit(self, mock_database):
        """Testing updating customer credit via update_customer_credit function."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        self.assertTrue(update_customer_credit(5, 5000))
        self.assertEqual(Customer.get_by_id(5).credit_limit, 5000)
        with self.assertRaises(ValueError):
            update_customer_credit(4, 80000)


    @patch('basic_operations.DATABASE_NAME')
    def test_list_active_customers(self, mock_database):
        """Testing updating customer credit via update_customer_credit function."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        self.assertEqual(list_active_customers(), 2)


    @patch('basic_operations.DATABASE_NAME')
    def test_report_single_customer(self, mock_database):
        """Testing report_single_customer reporting function."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        table_columns = ('customer_id', 'name', 'lastname', 'home_address', 'phone_number',
                         'email_address', 'active_status', 'credit_limit')
        expected_print = ((' | '.join(('{:^20}'.format(column) for column in table_columns))) + '\n'
                         + ' | '.join(('{:^20}'.format(str(x)) for x in self.starting_db[1])))
        with patch('sys.stdout', new=StringIO()) as captured_output:
            report_single_customer(2)
            self.assertEqual(captured_output.getvalue().rstrip('\n'), expected_print)
        with patch('sys.stdout', new=StringIO()) as captured_output:
            report_single_customer(4)
            self.assertEqual(captured_output.getvalue().rstrip('\n'),
                             'No records matching criteria found.')


    @patch('basic_operations.DATABASE_NAME')
    def test_report_all_customers(self, mock_database):
        """Testing report_all_customers function output."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        table_columns = ('customer_id', 'name', 'lastname', 'home_address', 'phone_number',
                         'email_address', 'active_status', 'credit_limit')
        expected_print = ' | '.join(('{:^20}'.format(column) for column in table_columns))
        for row in self.starting_db:
            expected_print += '\n' + ' | '.join(('{:^20}'.format(str(x)) for x in row))
        with patch('sys.stdout', new=StringIO()) as captured_output:
            report_all_customers()
            self.assertEqual(captured_output.getvalue().rstrip('\n'), expected_print)


    @patch('basic_operations.DATABASE_NAME')
    def test_report_customers_by_status(self, mock_database):
        """Testing report_customers_by_status function output."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        table_columns = ('customer_id', 'name', 'lastname', 'home_address', 'phone_number',
                         'email_address', 'active_status', 'credit_limit')
        expected_print = ((' | '.join(('{:^20}'.format(column) for column in table_columns))) + '\n'
                         + ' | '.join(('{:^20}'.format(str(x)) for x in self.starting_db[0])))
        with patch('sys.stdout', new=StringIO()) as captured_output:
            report_customers_by_status(False)
            self.assertEqual(captured_output.getvalue().rstrip('\n'), expected_print)