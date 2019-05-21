"""Test case class for basic operations"""
import sys
import unittest
import sqlite3
sys.path.append('/Users/guntur/PycharmProjects/uw/p220/SP_Python220B_2019/students/g_rama'
                '/lesson03/src')
import basic_operations as bo
import customer_model

testdb = sqlite3.connect("test.db")
bo.DB = testdb


class TestBasicOperations(unittest.TestCase):
    """Base class tests"""
    def test_add_customer(self):
        """Function to test the add customers"""
        bo.add_customer("100", "First", "Last", "Address", "Phone", "test@test.com", "1", "1000")

    def test_search_customer(self):
        bo.add_customer("200", "First", "Last", "Address", "Phone", "test@test.com", "1", "1000")
        print("added")
        actual_data = bo.search_customer(200)
        expected_data = "200"
        print(actual_data)
        self.assertEqual(expected_data, actual_data)

    def test_delete_customer(self):
        pass

    def test_update_customer_credit(self):
        pass

    def test_list_active_customers(self):
        pass




