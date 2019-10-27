"""
    Defines all the unit tests for the customer model, and basic operations code.
"""


import sys
sys.path.append('../src')

import unittest
import warnings

from basic_operations import *
from customer_model import Customer

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
        """Test the search customer function. Assumes inputs are in correct format."""
        customer1 = search_customer(100)

        # check that we are returning a dict
        self.assertIsInstance(customer1, dict)

        # check that the dictionary is empty
        if customer1:
            print(f'Dict {customer1}: should be empty but is not')
            assert False

        add_customer(100, 'Fran', 'K', '100 New York Ave, NYC, 98109', '248-331-6243',
                     'my_email@gmail.com', 'Active', 5000)
        customer2 = search_customer(100)

        # check that all the correct fields are in the dictionary
        self.assertIn('customer_id', customer2.keys())
        self.assertIn('name', customer2.keys())
        self.assertIn('last_name', customer2.keys())
        self.assertIn('home_address', customer2.keys())
        self.assertIn('phone_number', customer2.keys())
        self.assertIn('email_address', customer2.keys())
        self.assertIn('status', customer2.keys())
        self.assertIn('credit_limit', customer2.keys())

        # check that we get a dict with the correct customer
        self.assertEqual(customer2['customer_id'], 100)
        self.assertEqual(customer2['name'], 'Fran')
        self.assertEqual(customer2['last_name'], 'K')
        self.assertEqual(customer2['home_address'], '100 New York Ave, NYC, 98109')
        self.assertEqual(customer2['phone_number'], '248-331-6243')
        self.assertEqual(customer2['email_address'], 'my_email@gmail.com')
        self.assertEqual(customer2['status'], 'Active')
        self.assertEqual(customer2['credit_limit'], 5000)

    def test_delete_customer(self):
        """Deletes a customer properly if input is given in the correct format"""

        # deleting a non existing customer should only cause a print statement and no run errors
        with warnings.catch_warnings(record=True) as w:
            delete_customer(100)
            self.assertNotEqual(w, [])
            self.assertIs(w[0].category, UserWarning)
            self.assertEqual(str(w[0].message), 'User with customer_id=100 does not exist in the '
                                                'database.')

        add_customer(100, 'Fran', 'K', '100 New York Ave, NYC, 98109', '248-331-6243',
                     'my_email@gmail.com', 'Active', 5000)

        delete_customer(100)
        customer = Customer.get_or_none(Customer.customer_id == 100)

        self.assertIsNone(customer, 'Should evaluate to none.')

    def test_update_customer_credit(self):
        """
            Ensure that customer credit gets updates if inputs are in the correct format.
            Ensure that a ValueError exception is thrown if the customer does not exist in the
            database.
        """
        add_customer(100, 'Fran', 'K', '100 New York Ave, NYC, 98109', '248-331-6243',
                     'my_email@gmail.com', 'Active', 5000)

        customer = Customer.get(Customer.customer_id == 100)
        self.assertEqual(customer.credit_limit, 5000)

        update_customer_credit(100, 10000)

        customer_updated = Customer.get(Customer.customer_id == 100)

        self.assertEqual(customer_updated.credit_limit, 10000)
        self.assertEqual(customer.credit_limit, 5000)

        # ensure a value error is raised if the customer does not exist
        with self.assertRaises(ValueError):
            update_customer_credit(250, 5000)

    def test_list_active_customer(self):
        """Test that the correct number of active customers are counted in database."""

        # ensure no current customers
        active_customers = list_active_customers()
        self.assertEqual(active_customers, 0)

        # add a couple of customer whose status is all active
        add_customer(100, 'Fran', 'K', '100 New York Ave, NYC, 98109', '248-331-6243',
                     'my_email@gmail.com', 'Active', 5000)

        add_customer(200, 'Fran', 'K', '100 New York Ave, NYC, 98109', '248-331-6243',
                     'my_email@gmail.com', 'Active', 5000)

        add_customer(300, 'Fran', 'K', '100 New York Ave, NYC, 98109', '248-331-6243',
                     'my_email@gmail.com', 'Active', 5000)
        active_customers = list_active_customers()
        self.assertEqual(active_customers, 3)

        # add customers with inactive status
        add_customer(400, 'Fran', 'K', '100 New York Ave, NYC, 98109', '248-331-6243',
                     'my_email@gmail.com', 'Inactive', 5000)

        add_customer(500, 'Fran', 'K', '100 New York Ave, NYC, 98109', '248-331-6243',
                     'my_email@gmail.com', 'Inactive', 5000)

        active_customers = list_active_customers()
        self.assertEqual(active_customers, 3)
