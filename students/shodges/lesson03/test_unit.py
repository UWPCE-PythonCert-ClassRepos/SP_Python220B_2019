from unittest import TestCase

import basic_operations, peewee

class BaseDbTest(TestCase):
    """Test basic creation of, and connection to, the database."""
    def test_create_db(self):
        """Test that the database is successfully created."""

        self.assertIsInstance(basic_operations.customer_db, peewee.SqliteDatabase)

        # Set a var to track the beginning record count so we can test this later
        global begin_record_count
        bagin_record_count = basic_operations.list_active_customers()

    def test_add_record(self):
        """Test that a record is successfully added."""
        cust_1 = {'customer_id': 1, 'first_name':'John', 'last_name':'Doe',
                  'home_address': '123 Fake St', 'phone_number':5550111212,
                  'email_address':'john@johndoe.com', 'is_active':True,
                  'credit_limit':10000.00}

        cust_2 = {'customer_id': 2, 'first_name':'Bruce', 'last_name':'Wayne',
                  'home_address': '1 Wayne Manor', 'phone_number':9125553131,
                  'email_address':'bruce@notbatman.com', 'is_active':True,
                  'credit_limit':9999999.00}

        cust_3 = {'customer_id': 3, 'first_name':'Failure2', 'last_name':'Add',
                  'home_address': '2 Fail St', 'phone_number':9999999999,
                  'email_address':'fail@testcases.com', 'is_active':True,
                  'credit_limit':99999999.00}

        cust_4 = {'customer_id': 4}

        self.assertEqual(basic_operations.add_customer(**cust_1), True)

        self.assertEqual(basic_operations.add_customer(**cust_2), True)

        with self.assertRaises(ValueError):
            basic_operations.add_customer(**cust_3)

        with self.assertRaises(ValueError):
            basic_operations.add_customer(**cust_4)
