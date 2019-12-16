"""tests for basic operations """

# pylint: disable=wrong-import-position
import sys

sys.path.append("..\\src")

# pylint: enable=wrong-import-position

# pylint: disable=import-error
from unittest import TestCase
from basic_operations import add_customer, search_customer, \
    delete_customer, update_customer, list_active_customers
from cust_schema import Customer, database


def database_setup():
    """function for setting up clean table each time"""
    database.drop_tables([Customer])
    database.create_tables([Customer])
    database.close()


class TestBasicOps(TestCase):
    """Class for housing the tests"""

    def test_add_customer(self):
        """Test the ability to add a customer"""
        database_setup()

        add_customer(1, 'Guy', 'Dudeman', '1139 Bro Street', '800-123-4567',
                     'Guy_Dudeman01@gmail.com.com', True, 1000000)

        test = Customer.get(Customer.customer_id == 1)
        self.assertEqual(test.customer_first_name, 'Guy')
        self.assertEqual(test.customer_last_name, 'Dudeman')
        self.assertEqual(test.customer_home_address, '1139 Bro Street')
        self.assertEqual(test.customer_phone_number, '800-123-4567')
        self.assertEqual(test.customer_email, 'Guy_Dudeman01@gmail.com.com')
        self.assertEqual(test.customer_status, True)
        self.assertEqual(test.customer_credit_limit, 1000000)

    def test_search_customer(self):
        """Test the ability to search for a customer"""
        database_setup()

        add_customer(1, 'Guy', 'Dudeman', '1139 Bro Street', '800-123-4567',
                     'Guy_Dudeman01@gmail.com.com', True, 1000000)

        test_dict = {'Name': 'Guy', 'Last Name': 'Dudeman',
                     'Email': 'Guy_Dudeman01@gmail.com.com', 'Phone Number': '800-123-4567'}

        # Test that we can find Guy Dudeman in the database after entering it
        self.assertEqual(search_customer(1), test_dict)

        # Test that a search for none exist entry returns nothing
        self.assertEqual(search_customer(2), dict())

    def test_update_customer(self):
        """Test the ability to ability to update a customer"""
        database_setup()

        add_customer(1, 'Guy', 'Dudeman', '1139 Bro Street', '800-123-4567',
                     'Guy_Dudeman01@gmail.com.com', True, 1000000)

        update_customer(1, 1000)
        self.assertAlmostEqual(Customer.get(Customer.customer_id == 1).customer_credit_limit, 1000)

    def test_list_active_customers(self):
        """Test the ability to test active customer"""
        database_setup()

        add_customer(1, 'Guy', 'Dudeman', '1139 Bro Street', '800-123-4567',
                     'Guy_Dudeman01@gmail.com.com', True, 1000000)

        self.assertEqual(list_active_customers(), 1)

    def test_delete_customer(self):
        """Test the ability to delete a customer"""
        database_setup()

        add_customer(1, 'Guy', 'Dudeman', '1139 Bro Street', '800-123-4567',
                     'Guy_Dudeman01@gmail.com.com', True, 1000000)

        delete_customer(1)
        self.assertEqual(search_customer(1), dict())
