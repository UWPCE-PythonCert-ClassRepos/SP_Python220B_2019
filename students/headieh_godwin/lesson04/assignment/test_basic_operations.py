"""Tests basic operations for customer model"""

import logging
from unittest import TestCase
from peewee import IntegrityError
from customer_model import Customer
from basic_operations import *

# set up logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("LOGGER initialized")

def test_logger():
    """ checks that log file was made """
    file = os.path.join(PARENT, TIMESTR + "/db.log")
    assert os.path.exists(file) == 1

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
        LOGGER.info('Testing addition of new customer')
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
        with self.assertRaises(IntegrityError):
            add_customer(*customer_list[0])


    def test_add_customers(self):
        """Tests that adding multiple customers to database works"""
        new1 = (4, 'AJ', 'Kemp',
                '4 D Dr Houston, TX 77057',
                '7131234567', 'emaild@gmail.com',
                True, 5000.00)
        new2 = (5, 'Kyle', 'Sheridan',
                '5 E Way Houston, TX 77057',
                '7137654321', 'emaile@gmail.com',
                False, 1500.00)
        new3 = (6, 'Travis', 'Harrington',
                '6 F Blvd Houston, TX 77057',
                '7135671234', 'emailf@gmail.com',
                True, 5500.00)
        add_customers([new1, new2, new3])
        n_1 = Customer.get(Customer.customer_id == 4)
        n_2 = Customer.get(Customer.customer_id == 5)
        n_3 = Customer.get(Customer.customer_id == 6)
        self.assertEqual(n_1.firstname, 'AJ')
        self.assertEqual(n_1.credit_limit, 5000.00)
        self.assertEqual(n_2.firstname, 'Kyle')
        self.assertEqual(n_2.email_address, 'emaile@gmail.com')
        self.assertEqual(n_3.firstname, 'Travis')
        self.assertEqual(n_3.phone_number, 7135671234)



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

    def test_delete_customers(self):
        """Tests that deleting multiple customers to database works"""
        delete_customers([4, 5, 6])
        n_1 = search_customer(4)
        n_2 = search_customer(5)
        n_3 = search_customer(6)
        n_group = search_customers([4, 5, 6])
        expect_res = {}
        self.assertEqual(n_1, expect_res)
        self.assertEqual(n_2, expect_res)
        self.assertEqual(n_3, expect_res)
        self.assertEqual(n_group, [{}, {}, {}])

    def test_update_customer_credit(self):
        """This function tests that updating the credit works correctly"""
        LOGGER.info('Updating existing customer credit limit')
        update_customer_credit(2, 15000)
        self.assertEqual(Customer.get(Customer.customer_id == 2).credit_limit, 15000)
        LOGGER.info('Updating existing non-customer credit limit')
        #with self.assertRaises(IndexError):
            #update_customer_credit(123, 15000)

    def test_list_active_customers(self):
        """ This function tests that active customers are listed correctly """
        LOGGER.info('Testing the number of active customers.')
        num = list_active_customers()
        LOGGER.info('The number of active customers: %s', num)
        self.assertEqual(num, 0)
