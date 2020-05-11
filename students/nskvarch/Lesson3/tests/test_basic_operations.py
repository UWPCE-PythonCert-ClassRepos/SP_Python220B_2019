#!/usr/bin/env python3
"""Unit tests for the HP Norton Furniture Customer database Lesson 3 Assignment"""
# created by Niels Skvarch

import unittest
from src.basic_operations import *
from src.customer_model import *


def database_setup():
    """Creates or resets a database in the test folder using the customer model
    schema file that the rest of the tests will utilize."""
    database.drop_tables([Customer])
    database.create_tables([Customer])
    database.close()


class TestCaseOne(unittest.TestCase):
    """Test the Add Customer Function of the basic_operations file."""
    def test_add_customer(self):
        """Test the addition of customers to the database."""
        database_setup()
        add_customer("123", "Markus", "Garvey", "35 Spring Weather drive",
                     "123456789", "m.garvey@my_email_server.com", True, 2000.00)
        customer_one = Customer.get(Customer.customer_id == "123")
        self.assertEqual(customer_one.first_name, "Markus")
        self.assertEqual(customer_one.active_status, True)

    def test_add_customer_not_enough_input(self):
        """Test a failure to provide correct input."""
        database_setup()
        with self.assertRaises(TypeError):
            add_customer("lalaloopsy")


class TestCaseTwo(unittest.TestCase):
    """Test the Search Customer Function of the basic_operations file."""
    def test_search_customer(self):
        """Test a customer look-up."""
        database_setup()
        add_customer("123", "Markus", "Garvey", "35 Spring Weather drive",
                     "123456789", "m.garvey@my_email_server.com", True, 2000.00)
        customer_two = search_customer("123")
        self.assertEqual(customer_two["phone_number"], "123456789")
        self.assertEqual(customer_two["last_name"], "Garvey")
        self.assertEqual(customer_two["email_address"], "m.garvey@my_email_server.com")
        self.assertEqual(customer_two["first_name"], "Markus")

    def test_search_customer_not_found(self):
        """Test a customer look up when a bad customer id is given."""
        customer_three = search_customer("5678")
        self.assertEqual(customer_three, {})


class TestCaseThree(unittest.TestCase):
    """Test the Delete Customer Function from the basic_operations file"""
    def test_delete_customer(self):
        """Test the deletion of a customer"""
        database_setup()
        add_customer("123", "Markus", "Garvey", "35 Spring Weather drive",
                     "123456789", "m.garvey@my_email_server.com", True, 2000.00)
        delete_customer("123")
        customer_three = search_customer("123")
        self.assertEqual(customer_three, {})

    def test_del_customer_not_found(self):
        """Test the deletion of a customer that does not exist"""
        database_setup()
        with self.assertRaises(DoesNotExist):
            delete_customer("123")


class TestCaseFour(unittest.TestCase):
    """Test the Update Customer Credit Function from the basic_operations file"""
    def test_update_customer_credit(self):
        """Test the update of  the credit limit filed of a record"""
        database_setup()
        add_customer("123", "Markus", "Garvey", "35 Spring Weather drive",
                     "123456789", "m.garvey@my_email_server.com", True, 2000.00)
        update_customer_credit("123", 4500.00)
        customer_four = Customer.get(Customer.customer_id == "123")
        self.assertEqual(customer_four.credit_limit, 4500.00)

    def test_Update_customer_credit_not_found(self):
        """Test the update of a record that does not exist"""
        database_setup()
        with self.assertRaises(DoesNotExist):
            update_customer_credit("123", 4500.00)


class TestCaseFive(unittest.TestCase):
    """Tests the List Active Customers Function from the basic_operations file."""
    def test_list_active_customers(self):
        """Tests a count of active customers"""
        database_setup()
        add_customer("123", "Markus", "Garvey", "35 Spring Weather drive",
                     "123456789", "m.garvey@my_email_server.com", True, 2000.00)
        add_customer("456789", "Jeff", "Ingram", "201 Private road",
                     "937564323", "jeffiscool@server.com", False, 3500.00)
        add_customer("78910", "Roy", "Batty", "Shoulder of Orion",
                     "756453867", "notareplicant@email_server.com", True, 500.00)
        self.assertEqual(list_active_customers(), 2)


# main program name-space
if __name__ == "__main__":
    unittest.main()
