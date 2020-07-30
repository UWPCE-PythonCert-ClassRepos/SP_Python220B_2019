"""Tests basic operations for customer model"""

import logging
from unittest import TestCase
from customer_model import Customer
from basic_operations import *

# set up logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("LOGGER initialized")

def clear_db():
    """ clears and creates database """
    DB.drop_tables([Customer])
    DB.create_tables([Customer])
    DB.close()

class BasicOperationsTests(TestCase):
    """ This class defines unit test fuctions for basic_operations.py """
    def test_add_customer(self):
        """ Tests that customers get added to the DB correctly """
        LOGGER.info('clearing and creating new db table')
        clear_db()
        LOGGER.info('-- Testing adding new customer --')
        customer_list = [('1', 'Susan', 'Anderson', '1 A Ave Davis CA 95630',
                          '9161234567', 'emaila@gmail.com', True, 1000),
                         ('2', 'Karen', 'Smith', '2 B St Dana Point CA 92673',
                          '9491234567', 'emailb@hotmail.com', False, 10000),
                         ('3', 'Mo', 'Walters', '3 C Rd Houston, TX 77057',
                          '7131234567', 'emailc@mail.com', False, 15000)]
        add_customer(*customer_list[0])
        customer = Customer.get(Customer.customer_id == 1)
        self.assertEqual(customer.firstname, 'Susan')
        self.assertEqual(customer.lastname, 'Anderson')
        self.assertEqual(customer.home_address, '1 A Ave Davis CA 95630')
        self.assertEqual(customer.phone_number, 9161234567)
        self.assertEqual(customer.email_address, 'emaila@gmail.com')
        self.assertEqual(customer.status, True)
        self.assertEqual(customer.credit_limit, 1000)

        add_customer(*customer_list[1])
        add_customer(*customer_list[2])
        self.assertEqual(len(Customer), 3)

    def test_search_customer(self):
        """ Tests that searching for customers works correctly """
        LOGGER.info('Testing search on an existing customer')
        the_customer = search_customer(2)
        expect_res = {'firstname': 'Karen',
                      'lastname': 'Smith',
                      'phone_number': 9491234567,
                      'email_address': 'emailb@hotmail.com'}
        self.assertEqual(the_customer, expect_res)

        LOGGER.info('Testing search on an non-existing customer')
        the_customer = search_customer(123)
        expect_res = {}
        self.assertEqual(the_customer, expect_res)

    def test_delete_customer(self):
        """ Tests that deleting customers works correctly """
        LOGGER.info('Testing deletion of an existing customer')
        delete_customer(1)
        the_customer = search_customer(1)
        expect_res = {}
        self.assertEqual(the_customer, expect_res)

    def test_update_customer_credit(self):
        """This function tests that updating the credit works correctly"""
        LOGGER.info('Updating existing customer credit limit')
        update_customer_credit(2, 15000)
        self.assertEqual(Customer.get(Customer.customer_id == 2).credit_limit,
                         15000)

    def test_list_active_customers(self):
        """ This function tests that active customers are listed correctly """
        LOGGER.info('Testing the number of active customers.')
        num = list_active_customers()
        LOGGER.info('The number of active customers: %s', num)
        self.assertEqual(num, 0)
