"""
Test the functionality of the basic_operation.py
"""

#pylint: disable = C0413,E0401,E0602,W0401

import unittest
import sys
import decimal
sys.path.append(r"../src")
from basic_operations import *
from customer_model import DATABASE, Customer

LOGGER.setLevel(logging.CRITICAL)

class TestBasicOperations(unittest.TestCase):
    """
    This class tests all the methods in the basic operations
    """
    @classmethod
    def setUpClass(cls):
        """
        Setup the test case
        """
        # print('setup method is called')
        DATABASE.drop_tables([Customer])
        DATABASE.create_tables([Customer])


    @classmethod
    def tearDownClass(cls):
        """
        close the database connection at the end of each test.
        """
        # print('teardown method is called')
        DATABASE.close()


    def test_add_customer(self):
        """Test the add customer method"""
        new_customer = (1, 'Benjamin', 'Thomson',
                        '9x9 xyzxy Dr. Apt # 529D xxxxxx SC. 29403',
                        '202-755-3xx1', 'mxmxmx@gmail.com', True, 244.20)
        add_customer(*new_customer)
        new_customer = (2, 'Lindsay', 'Huggy',
                        '898 Bolian Dr. Myrtle Beach SC. 20909',
                        '717-934-2243', 'atomic@gmail.com', '', 244.20)
        add_customer(*new_customer)
        new_customer = (3, 'Ashley', 'Wiggins',
                        '999 Virginia Dr. Richmond VA. 20000',
                        '717-934-2243', 'ashleywiggins@gmail.com', False, 725.00)
        add_customer(*new_customer)
        new_row = Customer.get(Customer.customer_id == 1)

        self.assertEqual(new_row.name, 'Benjamin')
        self.assertEqual(new_row.last_name, 'Thomson')
        self.assertEqual(new_row.home_address[-5:], '29403')
        self.assertEqual(new_row.phone_number, '202-755-3xx1')
        self.assertEqual(new_row.email_address, 'mxmxmx@gmail.com')
        self.assertEqual(new_row.status, True)
        self.assertEqual(new_row.credit_limit, decimal.Decimal('244.2'))

        new_row = Customer.get(Customer.customer_id == 2)
        self.assertFalse(new_row.status)

        with self.assertRaises(peewee.IntegrityError):
            add_customer(*new_customer)


    def test_search_customer(self):
        """Test the search customer method """
        test_value = {'Name':'Lindsay', 'Last Name':'Huggy',
                      'Email': 'atomic@gmail.com', 'Phone':'717-934-2243'}
        self.assertEqual(search_customer(2), test_value)

        # Test when customer id is not in the table.
        self.assertEqual(search_customer(4), dict())


    def test_update_customer(self):
        """Test the update customer method."""
        update_customer(2, 1000.99)
        self.assertEqual(Customer.credit_limit, decimal.Decimal(1000.99))
        with self.assertRaises(ValueError):
            update_customer(4, 200)


    def test_delete_customer(self):
        """Delete the customer"""
        delete_customer(3)
        self.assertEqual(search_customer(3), dict())
        with self.assertRaises(peewee.DoesNotExist):
            delete_customer(3)


    def test_list_active_customer(self):
        """Test the list of active customers."""
        self.assertEqual(list_active_customer(), 1)


if __name__ == "__main__":

    unittest.main()
