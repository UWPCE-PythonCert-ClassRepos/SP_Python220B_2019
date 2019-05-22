"""Test case class for basic operations"""
import sys
import unittest
from peewee import *  # pylint: disable=unused-wildcard-import,wildcard-import
import basic_operations as bo
import customer_model as cm
sys.path.append('/Users/guntur/PycharmProjects/uw/p220/SP_Python220B_2019/students/g_rama'
                '/lesson03/src')


# testdb = SqliteDatabase('test.db')
# testdb.connect()
# testdb.execute_sql('PRAGMA foreign_keys = ON;')
# bo.DB = testdb


class TestBasicOperations(unittest.TestCase):
    """Base class tests"""

    def setUp(self):
        """Set up database"""
        testdb = SqliteDatabase('test.db')
        testdb.connect()
        testdb.execute_sql('PRAGMA foreign_keys = ON;')
        cm.DB = testdb

    def test_add_customer(self):
        """Function to test the add customers"""
        bo.add_customer("100", "TestFirst1", "TestLast1", "TestAddress1",
                        "TestPhone1", "test1@test.com", "1", "1000")
        expected_data = ("100", "TestFirst1", "TestLast1", "TestAddress1",
                         "TestPhone1", "test1@test.com", "1", "1000")
        added_customer = bo.Customer.get(bo.Customer.customer_id == "100")
        actual_data = (added_customer.customer_id, added_customer.name, added_customer.last_name,
                       added_customer.home_address, added_customer.phone_number,
                       added_customer.email_address, added_customer.status,
                       added_customer.credit_limit)
        self.assertEqual(expected_data, actual_data)
        added_customer.delete_instance()

    def test_search_customer(self):
        """Test function for search """
        bo.add_customer("200", "TestFirst2", "TestLast2", "TestAddress2",
                        "TestPhone2", "test2@test.com", "1", "1000")
        print("added")
        actual_data = bo.search_customer("200")
        expected_data = "TestFirst2"
        print(actual_data)
        self.assertEqual(expected_data, actual_data)

    def test_delete_customer(self):
        """test function for delete operation uses """
        bo.delete_customer("200")
        expected_data = None
        actual_data = bo.search_customer("200")
        self.assertEqual(expected_data, actual_data)

    def test_update_customer_credit(self):
        """Test function for update operation"""
        pass

    def test_list_active_customers(self):
        """Test function to list the active customers"""
        pass
