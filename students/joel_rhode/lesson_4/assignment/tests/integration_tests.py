"""
Contains integration tests for the basic_operations file for interacting with customer database.
"""
# pylint: disable=unused-argument, no-value-for-parameter

from unittest import TestCase
from unittest.mock import patch
from io import StringIO

import basic_operations
from basic_operations import (add_customer, search_customer, delete_customer,
                              update_customer_credit, list_active_customers,
                              report_all_customers)
from customer_model import Customer, DATABASE as database

TEST_DATABASE = 'test.db'


class BasicOperationsIntegrationTests(TestCase):
    """Integrated tests for functions in basic_operations.py."""
    def setUp(self):
        """Defines starting test database used for function testing."""
        starting_db = [(1, 'Bob', 'Bobbo', '12 Green St', '1112223344',
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
            Customer.insert_many(starting_db, fields=[Customer.customer_id, Customer.name,
                                                      Customer.lastname, Customer.home_address,
                                                      Customer.phone_number, Customer.email_address,
                                                      Customer.active_status, Customer.credit_limit
                                                      ]).execute()
        database.close()

    @patch('basic_operations.DATABASE_NAME')
    def test_main_integration(self, mock_database):
        """Full integration testing of basic_operations.py functions."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        self.assertEqual(list_active_customers(), 2)
        add_customer(17, 'Bob1', 'Testy', '111 Test St', 1234567890, 'bob@thetest.net', True, 70000)
        add_customer(18, 'Bob2', 'Testo', '112 Test St', 2234567890, 'b2@thetest.net', True, 71000)
        add_customer(19, 'Bob3', 'Testi', '113 Test St', 3234567890, 'b3@thetest.net', False, 72000)

        exp_dict = {
            'name': 'Bob2',
            'lastname': 'Testo',
            'email_address': 'b2@thetest.net',
            'phone_number': '2234567890'
            }
        self.assertDictEqual(search_customer(18), exp_dict)

        update_customer_credit(19, 50000)
        self.assertEqual(Customer.get_by_id(19).credit_limit, 50000)
        delete_customer(18)
        self.assertEqual(list_active_customers(), 3)

        ending_db = [(1, 'Bob', 'Bobbo', '12 Green St', '1112223344',
                     'bobbo@python.org', False, 85000),
                     (2, 'Jane', 'Janeo', '1550 Red Rd', '1118675309',
                     'jane@therealjane.com', True, 150000),
                     (5, 'Wilson', 'Volleyball', '1 Castaway Island', '0000000000',
                     'wilson@ImLost.com', True, 0),
                     (17, 'Bob1', 'Testy', '111 Test St', 1234567890,
                     'bob@thetest.net', True, 70000),
                     (19, 'Bob3', 'Testi', '113 Test St', 3234567890,
                      'b3@thetest.net', False, 50000)
                     ]
        table_columns = ('customer_id', 'name', 'lastname', 'home_address', 'phone_number',
                         'email_address', 'active_status', 'credit_limit')
        expected_print = ' | '.join(('{:^20}'.format(column) for column in table_columns))
        for row in ending_db:
            expected_print += '\n' + ' | '.join(('{:^20}'.format(str(x)) for x in row))
        with patch('sys.stdout', new=StringIO()) as captured_output:
            report_all_customers()
            self.assertEqual(captured_output.getvalue().rstrip('\n'), expected_print)
