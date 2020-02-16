"""
Unit test for assignment 3
test_unit.py
Joli Umetsu
PY220
"""
from unittest import TestCase
from customer_model import DB, Customer
from basic_operations import add_customer, search_customer, delete_customer, \
                             update_customer_credit, list_active_customers


def setup_db():
    """ Sets up database for test cases """
    DB.drop_tables([Customer])
    DB.close()
    DB.create_tables([Customer])
    DB.close()

class TestBasicOperations(TestCase):
    """ Unit tests for basic_operations functions """

    def test_add_customer(self):
        """ Tests function to add customer """
        setup_db()
        add_customer(1, "Gerard", "Pique", "123 Las Ramblas", 333333333,
                     "gerardpique@barcelona.com", True, 1000000.00)
        test_customer = Customer.get(Customer.customer_id == 1)

        self.assertEqual("Gerard", test_customer.name)
        self.assertEqual("Pique", test_customer.lastname)
        self.assertEqual("123 Las Ramblas", test_customer.home_address)
        self.assertEqual(333333333, test_customer.phone_number)
        self.assertEqual("gerardpique@barcelona.com", test_customer.email_address)
        self.assertEqual(True, test_customer.status)
        self.assertEqual(1000000.00, test_customer.credit_limit)

    def test_search_customer(self):
        """ Tests function to serach customer """
        setup_db()
        add_customer(1, "Gerard", "Pique", "123 Las Ramblas", 333333333,
                     "gerardpique@barcelona.com", True, 1000000.00)

        expected1 = {"name": "Gerard", "lastname": "Pique",
                     "email_address": "gerardpique@barcelona.com",
                     "phone_number": 333333333}
        expected2 = {}

        self.assertEqual(search_customer(1), expected1)
        self.assertEqual(search_customer(2), expected2)

    def test_delete_customer(self):
        """ Tests function to delete customer """
        setup_db()
        add_customer(1, "Gerard", "Pique", "123 Las Ramblas", 333333333,
                     "gerardpique@barcelona.com", True, 1000000.00)
        add_customer(2, "Leo", "Messi", "111 Las Ramblas", 1111111111,
                     "lionelmessi@barcelona.com", True, 5000000.00)
        delete_customer(1)

        self.assertEqual(search_customer(1), {})

    def test_update_customer_credit(self):
        """ Tests function to update customer's credit """
        setup_db()
        add_customer(1, "Gerard", "Pique", "123 Las Ramblas", 333333333,
                     "gerardpique@barcelona.com", True, 1000000.00)
        update_customer_credit(1, 300.00)

        test_customer = Customer.get(Customer.customer_id == 1)
        self.assertEqual(300.00, test_customer.credit_limit)

        with self.assertRaises(ValueError):
            update_customer_credit(2, 300.00)

    def test_list_active_customers(self):
        """ Tests function to list active customers """
        setup_db()
        add_customer(1, "Gerard", "Pique", "123 Las Ramblas", 333333333,
                     "gerardpique@barcelona.com", True, 1000000.00)
        add_customer(2, "Leo", "Messi", "111 Las Ramblas", 1111111111,
                     "lionelmessi@barcelona.com", False, 5000000.00)

        result = list_active_customers()
        self.assertEqual(1, result)
