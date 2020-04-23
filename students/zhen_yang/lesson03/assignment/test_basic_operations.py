""" This module test the functions written in basic_operations.py """
from unittest import TestCase
from unittest.mock import MagicMock, call, patch
import logging
from customer_model import *
from basic_operations import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class basic_operationsTests(TestCase):

    def test_add_customer(self):
        """ create an empty database for testing """
        database.drop_tables([Customer])
        database.create_tables([Customer])

        logger.info('-- Testing adding new customer --')
        add_customer(1, 'Emily', 'Yang',
                     '121 Main street NewYork', '2062847320',
                     'yange@hotmail.com', True, 10000)

        customer = Customer.get(Customer.customer_id == 1)
        self.assertEqual(customer.name, 'Emily')
        self.assertEqual(customer.lastname, 'Yang')
        self.assertEqual(customer.home_address, '121 Main street NewYork')
        self.assertEqual(customer.phone_number, '2062847320')
        self.assertEqual(customer.email_address, 'yange@hotmail.com')
        self.assertEqual(customer.status, True)
        self.assertEqual(customer.credit_limit, 10000)
        add_customer(2, 'Adam', 'Chilly',
                     '233 Jone street LA', '4342941868',
                     'chillya@hotmail.com', True, 5000)
        add_customer(3, 'Steve', 'Wagon',
                     '4508 Lord Ave Seattle', '6879337640', 'wagons@gmail.com',
                     False, 0)
        add_customer(4, 'Jone', 'Comba',
                     '1129 Brand street Boise', '3745689770',
                     'combaj@gmail.com', False, 100)
        add_customer(5, 'Zaler', 'Danny',
                     '29 Colb street Portland', '2323456787',
                     'dannyz@yahoo.com', True, 1000)
        self.assertEqual(len(Customer), 5)

        for customer in Customer:
            logger.info(f'{customer.name} {customer.home_address} '
                        f'{customer.phone_number} {customer.email_address} '
                        f'{customer.status} {customer.credit_limit}')
        logger.info('-- End of Testing adding new customer --\n')

    def test_search_customer(self):
        logger.info('-- Testing search an existing customer.--')
        # test seraching the exitsting customer
        the_customer = search_customer(2)
        expect_res = {'name': 'Adam',
                      'lastname': 'Chilly',
                      'phone_number': '4342941868',
                      'email_address': 'chillya@hotmail.com'}
        self.assertEqual(the_customer, expect_res)

        # test seraching the non-exitsting customer
        logger.info('-- Testing search a non-existing customer.--')
        the_customer = search_customer(12)
        expect_res = {}
        self.assertEqual(the_customer, expect_res)

    def test_delete_customer(self):
        logger.info('-- Testing delete an existing customer. --')
        delete_customer(5)
        the_customer = search_customer(5)
        expect_res = {}
        self.assertEqual(the_customer, expect_res)

    def test_update_customer_credit(self):
        logger.info('-- Testing update existing customer credit limit.--')

        # test existing customer
        update_customer_credit(3, 300)
        self.assertEqual(Customer.get(Customer.customer_id == 3).credit_limit,
                         300)
        # test non existing customer
        logger.info('-- Testing update non-existing customer credit limit.--')
        update_customer_credit(800, 300)

    def test_active_customers(self):
        logger.info('-- Testing the number of active customers.--')
        num = list_active_customers()
        logger.info(f'-- The number of active customers: {num} --\n')
        self.assertEqual(num, 2)
