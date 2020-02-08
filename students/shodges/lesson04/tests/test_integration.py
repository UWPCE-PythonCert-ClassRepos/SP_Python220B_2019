from unittest import TestCase

import peewee, os
import sys

sys.path.append('..')

import basic_operations

class IntegrationTest(TestCase):
    """Test the integrated application."""
    def test_integration(self):
        """Test the entire application functionality."""
        self.assertIsInstance(basic_operations.CUSTOMER_DB, peewee.SqliteDatabase)
        cust_1 = {'customer_id': 1, 'first_name':'George', 'last_name':'Washington',
                  'home_address': '4 Bowling Green', 'phone_number':2125555555,
                  'email_address':'george@governmenthouse.com', 'is_active':False,
                  'credit_limit':5.00}

        cust_2 = {'customer_id': 2, 'first_name':'John', 'last_name':'Adams',
                  'home_address': '524-30 Market St', 'phone_number':2675551212,
                  'email_address':'john@presidentshouse.com', 'is_active':False,
                  'credit_limit':100.00}

        cust_3 = {'customer_id': 3, 'first_name':'Thoams', 'last_name':'Jefferson',
                  'home_address': '1600 Pennsylvania Ave', 'phone_number':2029999999,
                  'email_address':'thomas@whitehouse.gov', 'is_active':True,
                  'credit_limit':10000.00}

        self.assertEqual(basic_operations.list_active_customers(), 0)

        self.assertEqual(basic_operations.add_customer(**cust_1), True)
        self.assertEqual(basic_operations.add_customer(**cust_2), True)
        self.assertEqual(basic_operations.add_customer(**cust_3), True)

        self.assertEqual(basic_operations.list_active_customers(), 1)

        self.assertEqual(basic_operations.update_customer_credit(1, 10000), True)
        self.assertEqual(basic_operations.update_customer_credit(3, 15000), True)

        self.assertEqual(basic_operations.search_customer(1)['credit_limit'], 10000)
        self.assertEqual(basic_operations.search_customer(3)['credit_limit'], 15000)

        self.assertEqual(basic_operations.delete_customer(1), True)
        self.assertEqual(basic_operations.delete_customer(2), True)
        self.assertEqual(basic_operations.delete_customer(3), True)

        self.assertEqual(basic_operations.list_active_customers(), 0)
