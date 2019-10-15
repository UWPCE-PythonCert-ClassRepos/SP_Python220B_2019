from basic_operations import *
from unittest import TestCase
from unittest.mock import Mock, patch
import peewee


def db_init():
    """
    Function to initialize DB, create
    and add tables
    """
    DB.init('customer.db')
    DB.drop_tables([Customer])
    DB.create_tables([Customer])


class Integration_testing(TestCase):
    """Integration testing for basic_operations.py"""
    def test_integration(self):
        db_init()
        input_customer_data = [('Andrew', 'peterson', '344 james ave' \
                                    , 6308153728, 'a_peteerson@mail.com', True, 4500), \
                               ('Wang', 'Wou', '103 spring ave', \
                                2223334456, 'wang_wou@gmail.com', True, 22000)]

        add_customer(input_customer_data)
        expected_output_1 = {'id': 1,
                             'name': 'Andrew',
                             'last_name': 'peterson',
                             'phone_number': 6308153728,
                             'email_address': 'a_peteerson@mail.com'}
        self.assertDictEqual(search_customer(1), expected_output_1)
        self.assertEqual(list_active_customers(), 2)
        update_customer_credit(1, 6500)
        update_customer_credit(2, 30000)
        customer_1 = Customer.get(Customer.id ==1)
        customer_2 = Customer.get(Customer.id ==2)
        self.assertEqual(customer_1.credit_limit, 6500)
        self.assertEqual(customer_2.credit_limit, 30000)
        self.assertEqual(list_active_customers(), 2)
        del_customer(2)
        self.assertEqual(list_active_customers(), 1)