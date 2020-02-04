from unittest import TestCase

import peewee, os

# Remove customers.db if it exists so we can start fresh
try:
    os.remove("customers.db")
except:
    pass

import basic_operations

class BaseDbTest(TestCase):
    """Test basic creation of, and connection to, the database."""
    def test_create_db(self):
        """Test that the database is successfully created."""

        self.assertIsInstance(basic_operations.customer_db, peewee.SqliteDatabase)

        # Set a var to track the beginning record count so we can test this later
        global begin_record_count
        begin_record_count = basic_operations.list_active_customers()

    def test_add_record(self):
        """Test that a record is successfully added when fields are correctly specified."""
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

        with self.assertRaises(ValueError): # cust_3 has too many digits in the credit_limit
            basic_operations.add_customer(**cust_3)

        with self.assertRaises(ValueError): # cust_4 is missing required fields
            basic_operations.add_customer(**cust_4)

        global begin_record_count
        self.assertEqual(basic_operations.list_active_customers(), (begin_record_count + 2))

        self.assertEqual(basic_operations.search_customer(2), cust_2)

    def test_update_record(self):
        """Test that a record is updated when the credit_limit is <=7 digits."""

        expected = {'customer_id': 2, 'first_name':'Bruce', 'last_name':'Wayne',
                    'home_address': '1 Wayne Manor', 'phone_number':9125553131,
                    'email_address':'bruce@notbatman.com', 'is_active':True,
                    'credit_limit':1000.00}

        with self.assertRaises(ValueError): # customer_id 3 doesn't exist
            basic_operations.update_customer_credit(3, 1000.00)

        self.assertEqual(basic_operations.update_customer_credit(2, 1000.00), True)

        self.assertEqual(basic_operations.search_customer(2), expected)

    def test_delete_records(self):
        """Test that a record is deleted if it exists."""

        with self.assertRaises(IndexError): # customer_id 3 wasn't added successfully
            basic_operations.delete_customer(3)

        self.assertEqual(basic_operations.delete_customer(1), True)
        self.assertEqual(basic_operations.delete_customer(2), True)

        self.assertEqual(basic_operations.list_active_customers(), 0)
