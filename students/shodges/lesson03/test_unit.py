from unittest import TestCase

import peewee, os

import basic_operations

class BaseDbTest(TestCase):
    """Test basic creation of, and connection to, the database."""
    def test_create_db(self):
        """Test that the database is successfully created."""

        self.assertIsInstance(basic_operations.CUSTOMER_DB, peewee.SqliteDatabase)

    def test_1_add_record(self):
        """Test that a record is successfully added when fields are correctly specified."""
        cust_1 = {'customer_id': 1, 'first_name':'John', 'last_name':'Doe',
                  'home_address': '123 Fake St', 'phone_number':5550111212,
                  'email_address':'john@johndoe.com', 'is_active':True,
                  'credit_limit':10000.00}

        cust_2 = {'customer_id': 2, 'first_name':'Bruce', 'last_name':'Wayne',
                  'home_address': '1 Wayne Manor', 'phone_number':9125553131,
                  'email_address':'bruce@notbatman.com', 'is_active':True,
                  'credit_limit':9999999.00}

        cust_3 = {'customer_id': 3}

        cust_4 = {'customer_id': 4, 'first_name':'Jane', 'last_name':'Doe',
                  'home_address': '0 Infinite Loop', 'phone_number':1112223333,
                  'email_address':'jane@janedoe.com', 'is_active':False,
                  'credit_limit':150000.00}

        # Duplicate customer_id with a field that doesn't equal what we later test for
        cust_4_b = {'customer_id': 4, 'first_name':'Jane', 'last_name':'Doe',
                    'home_address': '0 Infinite Loop', 'phone_number':1112223333,
                    'email_address':'jane@janedoe.com', 'is_active':True,
                    'credit_limit':150000.00}

        begin_record_count = basic_operations.list_active_customers()

        self.assertEqual(basic_operations.add_customer(**cust_1), True)

        self.assertEqual(basic_operations.add_customer(**cust_2), True)

        self.assertEqual(basic_operations.add_customer(**cust_3), False)

        self.assertEqual(basic_operations.add_customer(**cust_4), True)

        # The PK exists, so this should fail
        self.assertEqual(basic_operations.add_customer(**cust_4_b), False)

        self.assertEqual(basic_operations.list_active_customers(), (begin_record_count + 2))

        self.assertEqual(basic_operations.search_customer(2).home_address, cust_2['home_address'])

        # The duplicate is True -- so if there was no overwrite, this will pass
        self.assertEqual(basic_operations.search_customer(4).is_active, False)

    def test_2_update_record(self):
        """Test that a record is updated when the credit_limit is <=7 digits."""

        # This will fail
        self.assertEqual(basic_operations.update_customer_credit(3, 1000.00), False)

        self.assertEqual(basic_operations.search_customer(2).credit_limit, 9999999.00)
        self.assertEqual(basic_operations.update_customer_credit(2, 1000.00), True)
        self.assertEqual(basic_operations.search_customer(2).credit_limit, 1000.00)

    def test_3_delete_records(self):
        """Test that a record is deleted if it exists."""

        self.assertEqual(basic_operations.list_active_customers(), 2)

        self.assertEqual(basic_operations.delete_customer(1), True)
        self.assertEqual(basic_operations.delete_customer(2), True)

        self.assertEqual(basic_operations.delete_customer(3), False)
        self.assertEqual(basic_operations.delete_customer(4), True)

        self.assertEqual(basic_operations.list_active_customers(), 0)
