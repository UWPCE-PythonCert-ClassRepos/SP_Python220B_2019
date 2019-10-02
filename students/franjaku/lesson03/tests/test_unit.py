"""
    Defines all the unit tests for the customer model, and basic operations code.
"""


import sys
sys.path.append('../')

import unittest
from unittest import mock
from basic_operations import *
from customer_model import *

class CustomerModelTests(unittest.TestCase):
    """Customer model tests."""
    pass


class BasicOpertationsTests(unittest.TestCase):
    """Test all the basic operations written."""

    def setUp(self):
        database.create_tables([Customer])

    def tearDown(self):
        Customer.delete().execute()
        database.close()

    def test_add_customer(self):
        """Ensure that a customer is inserted if all the inputs have the correct format."""
        add_customer(100, 'Fran', 'K', '100 New York Ave, NYC, 98109', '248-331-6243',
                     'my_email@gmail.com', 'Active', 5000)

        query = Customer.get_or_none()
        print(f'Query object: {query}')
        print(type(query))
        # checks that something got added
        self.assertIsNotNone(query)

        # check that the right unique person got added
        self.assertEqual(Customer[100].customer_id, 100)
        self.assertEqual(Customer[100].name, 'Fran')
        self.assertEqual(Customer[100].last_name, 'K')
        self.assertEqual(Customer[100].home_address, '100 New York Ave, NYC, 98109')
        self.assertEqual(Customer[100].phone_number, '248-331-6243')
        self.assertEqual(Customer[100].email_address, 'my_email@gmail.com')
        self.assertEqual(Customer[100].status, 'Active')
        self.assertEqual(Customer[100].credit_limit, 5000)

    def test_search_customer(self):
        pass

    def test_delete_customer(self):
        pass

    def test_update_customer_credit(self):
        pass

    def test_list_active_customer(self):
        pass
