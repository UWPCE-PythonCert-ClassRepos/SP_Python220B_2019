"""Module for testing integration of basic operations"""

import unittest
from unittest import TestCase

import customer_model as cm
import basic_operations as bo


class BasicOperationsTest(TestCase):
    """Testing integration"""
    @classmethod
    def setUp(cls):
        """Setup database"""
        cm.DATABASE.drop_tables([cm.Customer])
        cm.DATABASE.create_tables([cm.Customer])

    @classmethod
    def tearDown(cls):
        """Close database"""
        cm.DATABASE.close()

    def test_integration(self):
        """Testing integration of the modules"""
        bo.add_customer(100, 'Peter', 'Parker',
                        '135 W. 50th Street, New York City, NY 10011',
                        '212-576-4000', 'peter.parker@marvel.com',
                        True, 1000)
        bo.add_customer(200, 'Iron', 'Man',
                        '17801 International Blvd, Seattle, WA 98101',
                        '206-787-5388', 'iron.man@gmail.com',
                        True, 5000)

        bo.update_customer_credit(200, 9000)
        a_customer = cm.Customer.get(cm.Customer.customer_id == 200)
        self.assertEqual(a_customer.credit_limit, 9000)

        bo.add_customer(300, 'Ramkumar', 'Rajanbabu',
                        '7525 166th Ave NE, Redmond, WA 98052',
                        '425-556-2900', 'ram.kumar@gmail.com',
                        False, 7078)

        self.assertEqual(bo.list_active_customers(), 2)

        a_customer_2 = bo.search_customer(100)
        a_customer_2_dict = {'first_name': 'Peter',
                             'last_name': 'Parker',
                             'email_address': 'peter.parker@marvel.com',
                             'phone_number': '212-576-4000'}
        self.assertEqual(a_customer_2, a_customer_2_dict)

        bo.delete_customer(100)
        self.assertEqual(bo.search_customer(100), {})


if __name__ == "__main__":
    unittest.main()
