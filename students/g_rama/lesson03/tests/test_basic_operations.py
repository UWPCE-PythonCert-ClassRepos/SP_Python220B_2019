"""Test case class for basic operations"""
# pylint: disable=unused-wildcard-import,wildcard-import,too-many-arguments,wrong-import-position
import unittest
import sys
sys.path.append('/Users/guntur/PycharmProjects/uw/p220/SP_Python220B_2019/'
                'students/g_rama/lesson03/src/')
from peewee import *
import basic_operations as bo
import customer_model as cm


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
        bo.add_customer("300", "TestFirst3", "TestLast3", "TestAddress3",
                        "TestPhone3", "test3@test.com", "1", "1000")
        bo.update_customer_credit("300", "3000")
        updated_customer = bo.Customer.get(bo.Customer.customer_id == "300")
        expected_credit = "3000"
        actual_credit = updated_customer.credit_limit
        self.assertEqual(expected_credit, actual_credit)
        updated_customer.delete_instance()

    def test_list_active_customers(self):
        """Test function to list the active customers"""
        bo.add_customer("400", "TestFirst4", "TestLast4", "TestAddress4",
                        "TestPhone4", "test4@test.com", "1", "1000")
        bo.add_customer("500", "TestFirst5", "TestLast5", "TestAddress5",
                        "TestPhone5", "test5@test.com", "1", "5000")
        bo.add_customer("600", "TestFirst6", "TestLast6", "TestAddress6",
                        "TestPhone6", "test6@test.com", "0", "5000")
        actual_count = bo.list_active_customers()
        expected_count = 2
        self.assertEqual(actual_count, expected_count)
        added_customer1 = bo.Customer.get(bo.Customer.customer_id == "400")
        added_customer2 = bo.Customer.get(bo.Customer.customer_id == "500")
        added_customer3 = bo.Customer.get(bo.Customer.customer_id == "600")
        added_customer1.delete_instance()
        added_customer2.delete_instance()
        added_customer3.delete_instance()
