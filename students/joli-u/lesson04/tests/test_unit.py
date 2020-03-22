"""
test_unit.py
Assignment 4
Joli Umetsu
PY220
"""
from unittest import TestCase
import sys
sys.path.append('..')
from customer_model import DB, Customer
from basic_operations import add_customer, add_customers, search_customer, \
                             search_customers, delete_customer, delete_customers, \
                             update_customer_credit, list_active_customers

def setup_db():
    """ Sets up database for test cases """
    DB.drop_tables([Customer])
#    DB.close()
    DB.create_tables([Customer])
    add_customer(1, "Leo", "Messi", "100 Las Ramblas", 1234567890,
                 "lionelmessi@barcelona.com", True, 5000000.00)
    add_customer(2, "Ivan", "Rakitic", "111 Las Ramblas", 2345678901,
                 "ivanrakitic@barcelona.com", True, 2000000.00)
    add_customer(3, "Gerard", "Pique", "123 Las Ramblas", 3333333333,
                 "gerardpique@barcelona.com", True, 300000.00)
#    DB.close()

class TestBasicOperations(TestCase):
    """ Unit tests for basic_operations functions """

    def test_add_customer(self):
        """ Tests function to add customer """
        setup_db()
        add_customer(4, "Marc", "ter Stegen", "400 Las Ramblas", 0000000000,
                     "marcterstegen@barcelona.com", True, 1000000.00)
        test_customer = Customer.get(Customer.customer_id == 4)

        self.assertEqual("Marc", test_customer.name)
        self.assertEqual("ter Stegen", test_customer.lastname)
        self.assertEqual("400 Las Ramblas", test_customer.home_address)
        self.assertEqual(0000000000, test_customer.phone_number)
        self.assertEqual("marcterstegen@barcelona.com", test_customer.email_address)
        self.assertEqual(True, test_customer.status)
        self.assertEqual(1000000.00, test_customer.credit_limit)

    def test_add_customers(self):
        """ Tests function to add multiple customers """
        setup_db()
        info1 = [4, "Marc", "ter Stegen", "400 Las Ramblas", 0000000000,
                 "marcterstegen@barcelona.com", True, 1000000.00]
        info2 = [5, "Sergi", "Roberto", "567 Las Ramblas", 5678901234,
                 "sergiroberto@barcelona.com", True, 90000.00]

        add_customers([info1, info2])
        customer1 = Customer.get(Customer.customer_id == 4)
        self.assertEqual("Marc", customer1.name)
        customer2 = Customer.get(Customer.customer_id == 5)
        self.assertEqual("Sergi", customer2.name)

    def test_search_customer(self):
        """ Tests function to search customer """
        setup_db()
        expected0 = {}
        expected1 = {"name": "Leo", "lastname": "Messi",
                     "email_address": "lionelmessi@barcelona.com",
                     "phone_number": 1234567890}

        self.assertEqual(search_customer(0), expected0)
        self.assertEqual(search_customer(1), expected1)

    def test_search_customers(self):
        """ Tests function to search multiple customers """
        setup_db()
        expected1 = {"name": "Leo", "lastname": "Messi",
                     "email_address": "lionelmessi@barcelona.com",
                     "phone_number": 1234567890}
        to_search_list = [1, 2, 3]
        search_results = search_customers(to_search_list)
        self.assertEqual(search_results[0], expected1)
        self.assertEqual(search_results[1]['name'], "Ivan")
        self.assertEqual(search_results[2]['name'], "Gerard")

    def test_delete_customer(self):
        """ Tests function to delete customer """
        setup_db()
        delete_customer(1)
        self.assertEqual(search_customer(1), {})

    def test_delete_customers(self):
        """ Tests function to delete multiple customers """
        setup_db()
        to_delete_list = [2, 3]
        delete_customers(to_delete_list)
        self.assertEqual(search_customer(2), {})
        self.assertEqual(search_customer(3), {})

    def test_update_customer_credit(self):
        """ Tests function to update customer's credit """
        setup_db()
        update_customer_credit(3, 300.00)
        test_customer = Customer.get(Customer.customer_id == 3)
        self.assertEqual(300.00, test_customer.credit_limit)

        with self.assertRaises(ValueError):
            update_customer_credit(10, 300.00)

    def test_list_active_customers(self):
        """ Tests function to list active customers """
        setup_db()
        result = list_active_customers()
        self.assertEqual(3, result)
