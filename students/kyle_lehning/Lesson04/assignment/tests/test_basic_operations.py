#!/usr/bin/env python3
"""
Tests for basic_operations
"""
from unittest import TestCase
from functools import wraps
import peewee
from customer_schema import Customer  # pylint: disable=E0401
import basic_operations as b_o  # pylint: disable=E0401


TEST_DB = peewee.SqliteDatabase(':memory:')


def use_test_database(fn):  # pylint: disable=C0103
    """
    Used to create decorator that binds the given models to the db for the duration of wrapped block
    """
    @wraps(fn)
    def inner(self):
        with TEST_DB.bind_ctx([Customer]):
            TEST_DB.create_tables([Customer])
            try:
                fn(self)
            finally:
                TEST_DB.drop_tables([Customer])
    return inner


class BasicOperationsUnitTest(TestCase):
    """
    Class for unit tests for basic_operations.py
    """
    @use_test_database
    def test_add_customer(self):
        """
        Test that add_customer function works and returns correct errors
        """
        test_user = {'customer_id': '1255', 'name': 'Tim', 'lastname': 'Allen',
                     'home_address': "15402 W 8 Mile Rd, Detroit, MI 48219",
                     'phone_number': '5558468665', 'email_address': 'TimToolManTaylor@ToolTime.com',
                     'status': True, 'credit_limit': 10000.00}
        b_o.add_customer(**test_user)

        db_query = Customer.get_by_id('1255')
        self.assertEqual(db_query.customer_id, test_user['customer_id'])
        self.assertEqual(db_query.name, test_user['name'])
        self.assertEqual(db_query.lastname, test_user['lastname'])
        self.assertEqual(db_query.home_address, test_user['home_address'])
        self.assertEqual(db_query.phone_number, test_user['phone_number'])
        self.assertEqual(db_query.email_address, test_user['email_address'])
        self.assertEqual(db_query.status, test_user['status'])
        self.assertEqual(db_query.credit_limit, test_user['credit_limit'])

        with self.assertRaises(peewee.IntegrityError) as context:
            b_o.add_customer(**test_user)
        self.assertTrue('Tried to add a customer_id that already exists:'
                        in str(context.exception))

        second_user = {'customer_id': '1245', 'name': 'Tim', 'lastname': 'Allen',
                       'home_address': "15402 W 8 Mile Rd, Detroit, MI 48219",
                       'phone_number': '55584686654433443434344343434334343',
                       'email_address': 'TimToolManTaylor@ToolTime.com',
                       'status': True, 'credit_limit': '100'}
        b_o.add_customer(**second_user)
        self.assertEqual(Customer.select().count(), 2)

    @use_test_database
    def test_search_customer(self):
        """
        Test that add_customer function works and returns empty dictionary if doesn't exist
        """
        Customer.create(
            customer_id='1564', name='First', lastname='Last',
            home_address='12 1st st, Seattle, WA 98101',
            phone_number='5551251255', email_address='test_email@tests.com',
            status=True, credit_limit=150.00
        )
        self.assertEqual(len(b_o.search_customer("doesn't exist")), 0)
        db_query = b_o.search_customer('1564')
        self.assertEqual(db_query['name'], 'First')
        self.assertEqual(db_query['lastname'], 'Last')
        self.assertEqual(db_query['phone_number'], '5551251255')
        self.assertEqual(db_query['email_address'], 'test_email@tests.com')

    @use_test_database
    def test_delete_customer(self):
        """
        Test that delete_customer function works
        """
        Customer.create(
            customer_id='1564', name='First', lastname='Last',
            home_address='12 1st st, Seattle, WA 98101',
            phone_number='5551251255', email_address='test_email@tests.com',
            status=True, credit_limit=150.00
        )
        Customer.create(
            customer_id='2', name='First2', lastname='Last2',
            home_address='12 2nd st, Seattle, WA 98101',
            phone_number='5551251252', email_address='test_email2@tests.com',
            status=True, credit_limit=152.00
        )
        db_query = Customer.get_by_id('1564')
        self.assertEqual(db_query.customer_id, '1564')
        self.assertEqual(Customer.select().count(), 2)
        try:
            b_o.delete_customer('doesnt exist')
        except Exception as exception: # pylint: disable=W0703
            self.fail("delete_customer() raised {} unexpectedly".format(exception))
        b_o.delete_customer('1564')
        self.assertEqual(Customer.select().count(), 1)
        with self.assertRaises(peewee.DoesNotExist):
            Customer.get_by_id('1564')

    @use_test_database
    def test_update_credit_limit(self):
        """
        Test that update_credit_limit() function works
        """
        Customer.create(
            customer_id='1564', name='First', lastname='Last',
            home_address='12 1st st, Seattle, WA 98101',
            phone_number='5551251255', email_address='test_email@tests.com',
            status=True, credit_limit=150.00
        )
        db_query = Customer.get_by_id('1564')
        self.assertEqual(db_query.credit_limit, 150.00)
        b_o.update_customer_credit('1564', 200.20)
        db_query = Customer.get_by_id('1564')
        self.assertEqual(float(db_query.credit_limit), 200.20)
        with self.assertRaises(ValueError):
            b_o.update_customer_credit("Value Fail", 500)

    @use_test_database
    def test_list_active_customers(self):
        """
        Test that list_active_customers() returns correct amount of active customers
        """
        active_count = b_o.list_active_customers()
        self.assertEqual(active_count, 0)
        Customer.create(
            customer_id='1564', name='First', lastname='Last',
            home_address='12 1st st, Seattle, WA 98101',
            phone_number='5551251255', email_address='test_email@tests.com',
            status=True, credit_limit=150.00
        )
        active_count = b_o.list_active_customers()
        self.assertEqual(active_count, 1)
        Customer.create(
            customer_id='2', name='First2', lastname='Last2',
            home_address='12 2nd st, Seattle, WA 98101',
            phone_number='5551251252', email_address='test_email2@tests.com',
            status=False, credit_limit=152.00
        )
        active_count = b_o.list_active_customers()
        self.assertEqual(active_count, 1)


class BasicOperationsIntegrationTest(TestCase):
    """Class for integration tests of basic_operations.py"""
    @use_test_database
    def test_basic_operations_integration(self):
        """
        Test that list_active_customers() returns correct amount of active customers
        """
        test_user = {'customer_id': '1255', 'name': 'Tim', 'lastname': 'Allen',
                     'home_address': "15402 W 8 Mile Rd, Detroit, MI 48219",
                     'phone_number': '5558468665', 'email_address': 'TimToolManTaylor@ToolTime.com',
                     'status': True, 'credit_limit': 10000.00}
        b_o.add_customer(**test_user)
        test_search = b_o.search_customer('1255')
        self.assertEqual(test_search['name'], 'Tim')
        self.assertEqual(test_search['lastname'], 'Allen')
        self.assertEqual(test_search['phone_number'], '5558468665')
        self.assertEqual(test_search['email_address'], 'TimToolManTaylor@ToolTime.com')
        b_o.update_customer_credit('1255', 520)
        db_query = Customer.get_by_id('1255')
        self.assertEqual(db_query.credit_limit, 520)
        customer_count = b_o.list_active_customers()
        self.assertEqual(customer_count, 1)
        b_o.delete_customer('1255')
        customer_count = b_o.list_active_customers()
        self.assertEqual(customer_count, 0)
