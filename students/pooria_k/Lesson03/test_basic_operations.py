from basic_operations import *
from unittest import TestCase
from unittest.mock import Mock, patch
import peewee


def db_init():
    """
    Function to initialize DB, create
    and add tables
    """
    db.init('customer.db')
    db.drop_tables([Customer])
    db.create_tables([Customer])
    add_customer(CUSTOMER_LIST)


class test_basic_operations(TestCase):
    """
    This class includes all the test function
    for testing functions inside basic_operation.py
    """

    def test_add_customer(self):
        """Test adding new customer"""
        db_init()
        input_customer_data = [('Andrew', 'peterson', '344 james ave' \
                              , 6308153728, 'a_peteerson@mail.com', True, 4500), \
                         ('Wang', 'Wou', '103 spring ave', \
                          2223334456, 'wang_wou@gmail.com', False, 22000)]

        add_customer(input_customer_data)
        customer_1_expected_output = input_customer_data[0]

        NAME = 0
        LASTNAME = 1
        ADDRESS = 2
        PHONE = 3
        EMAIL = 4
        STATUS = 5
        LIMIT = 6

        customer_1 = Customer.get(Customer.id == 1)

        self.assertEqual(customer_1.name, customer_1_expected_output[NAME])
        self.assertEqual(customer_1.lastname, customer_1_expected_output[LASTNAME])
        self.assertEqual(customer_1.home_address, customer_1_expected_output[ADDRESS])
        self.assertEqual(customer_1.phone_number, customer_1_expected_output[PHONE])
        self.assertEqual(customer_1.email_address, customer_1_expected_output[EMAIL])
        self.assertEqual(customer_1.status, customer_1_expected_output[STATUS])
        self.assertEqual(customer_1.credit_limit, customer_1_expected_output[LIMIT])

        expected_output = {'id': 1,
                           'name': 'Andrew',
                           'last_name': 'peterson',
                           'phone_number': 6308153728,
                           'email_address': 'a_peteerson@mail.com'}
        self.assertDictEqual(search_customer(1), expected_output)



    def test_search_cutomer(self):
        """Test searching a customer"""
        db_init()
        input_customer_data = [('Andrew', 'peterson', '344 james ave' \
                              , 6308153728, 'a_peteerson@mail.com', True, 4500), \
                         ('Wang', 'Wou', '103 spring ave', \
                          2223334456, 'wang_wou@gmail.com', False, 22000)]

        add_customer(input_customer_data)

        expected_output_1 = {'id': 1,
                           'name': 'Andrew',
                           'last_name': 'peterson',
                           'phone_number': 6308153728,
                           'email_address': 'a_peteerson@mail.com'}

        expected_output_2 = {'id': 2,
                           'name': 'Wang',
                           'last_name': 'Wou',
                           'phone_number': 2223334456,
                           'email_address': 'wang_wou@gmail.com'}

        self.assertDictEqual(search_customer(1),expected_output_1)
        self.assertDictEqual(search_customer(2), expected_output_2)


    def test_search_for_cutomer_that_dose_not_exists(self):
        """testing search_customer for customert ID
        That dosenot exists """
        search_customer(4)
        self.assertRaises(Customer.DoesNotExist)


    def test_del_customer(self):
        """Test deleting a customer"""
        db_init()
        input_customer_data = [('Andrew', 'peterson', '344 james ave' \
                              , 6308153728, 'a_peteerson@mail.com', True, 4500), \
                         ('Wang', 'Wou', '103 spring ave', \
                          2223334456, 'wang_wou@gmail.com', False, 22000)]

        add_customer(input_customer_data)
        del_customer(1)
        self.assertDictEqual(search_customer(1),{})

    def test_delete_customer_that_dose_not_exists(self):
        """Test deleting customer that
        dosenot exists"""
        del_customer(4)
        self.assertRaises(Customer.DoesNotExist)

    def test_update_customer_credit(self):
        """Test updating customer credit limit """
        db_init()
        input_customer_data = [('Andrew', 'peterson', '344 james ave' \
                              , 6308153728, 'a_peteerson@mail.com', True, 4500), \
                         ('Wang', 'Wou', '103 spring ave', \
                          2223334456, 'wang_wou@gmail.com', False, 22000)]

        add_customer(input_customer_data)
        update_customer_credit(1, 6500)
        update_customer_credit(2, 30000)
        customer_1 = Customer.get(Customer.id ==1)
        customer_2 = Customer.get(Customer.id ==2)
        self.assertEqual(customer_1.credit_limit, 6500)
        self.assertEqual(customer_2.credit_limit, 30000)

    def test_list_active_customer(self):
        """testing list_active_customer()"""
        db_init()
        input_customer_data = [('Andrew', 'peterson', '344 james ave' \
                              , 6308153728, 'a_peteerson@mail.com', True, 4500), \
                         ('Wang', 'Wou', '103 spring ave', \
                          2223334456, 'wang_wou@gmail.com', False, 22000)]

        add_customer(input_customer_data)
        self.assertEqual(list_active_customers(), 1)

