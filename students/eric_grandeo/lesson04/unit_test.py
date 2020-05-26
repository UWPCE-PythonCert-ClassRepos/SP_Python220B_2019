'''
Unit tests
'''

# pylint: disable=W

import logging
from unittest import TestCase
import peewee
from customers_model import *
from basic_operations import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class TestBasicOperations(TestCase):
    '''Test all Database functions'''
    def setUp(self):
        '''Create the tables'''
        database.create_tables([Customers])
        LOGGER.info('Create table successful')

    def tearDown(self):
        '''Delete the tables'''
        database.drop_tables([Customers])
        LOGGER.info('Database tables dropped')

    def test_add_customer(self):
        '''test add a customer to the database'''
        test_customer = {
            'customer_id': '12345',
            'name': 'Eric Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        }
        add_customer(**test_customer)
        record = Customers.get(Customers.customer_id == test_customer['customer_id'])
        LOGGER.info("New customer: {}".format(record.name))
        self.assertEqual(record.customer_id, test_customer['customer_id'])

    def test_search_customer(self):
        '''test searching for a customer by ID'''
        test_customer = {
            'customer_id': '12345',
            'name': 'Eric Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        }

        add_customer(**test_customer)
        customer_record = {'name':'Eric Grandeo', 'lastname':'Grandeo',
                           'email_address':'email@email.com',
                           'phone_number':'1-212-555-1234'}
        result = search_customer('12345')
        self.assertEqual(result, customer_record)


    def test_search_customer_fail(self):
        '''test a failed search, user does not exist'''
        test_customer = {
            'customer_id': '12345',
            'name': 'Eric Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        }

        add_customer(**test_customer)
        fail_customer = {}
        result = search_customer('12346')
        self.assertEqual(result, fail_customer)

    def test_delete_customer(self):
        '''test deleting a customer'''
        test_customer = {
            'customer_id': '12345',
            'name': 'Eric Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        }
        add_customer(**test_customer)
        self.assertEqual(delete_customer(test_customer['customer_id']), None)

    def test_delete_customer_fail(self):
        '''test deleting a customer that does not exist'''
        with self.assertRaises(ValueError):
            delete_customer('2468')

    def test_update_customer_credit(self):
        '''test updating a users credit limit by id'''
        test_customer = {
            'customer_id': '12345',
            'name': 'Eric Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        }
        add_customer(**test_customer)
        update_customer_credit(test_customer['customer_id'], 100000)
        get_customer = Customers.get(Customers.customer_id == test_customer['customer_id'])
        LOGGER.info("New credit limit: {}".format(get_customer.credit_limit))
        self.assertEqual(get_customer.credit_limit, 100000)


    def test_update_customer_credit_fail(self):
        '''test updating the credit limit of a user that does not exist'''
        test_customer = {
            'customer_id': '12345',
            'name': 'Eric Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        }
        add_customer(**test_customer)
        with self.assertRaises(ValueError):
            update_customer_credit('2468', 100000)

    def test_list_active_customers(self):
        '''test getting the number of active customers where active == True'''
        test_customer_1 = {
            'customer_id': '12345',
            'name': 'Eric Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        }
        test_customer_2 = {
            'customer_id': '45678',
            'name': 'Jack Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': False,
            'credit_limit': 25000
        }
        test_customer_3 = {
            'customer_id': '54321',
            'name': 'Vivie Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        }
        add_customer(**test_customer_1)
        add_customer(**test_customer_2)
        add_customer(**test_customer_3)
        return_active_customers()
        self.assertEqual(list_active_customers(), 2)

    def test_add_multiple_customers(self):
        'test adding multiple customers'
        test_customers = [{
            'customer_id': '54321',
            'name': 'Eric Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        },
        {
            'customer_id': '98765',
            'name': 'Jack Charles',
            'lastname': 'Charles',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': False,
            'credit_limit': 25000
        }
        ,{
            'customer_id': '10846',
            'name': 'Vivie Harper',
            'lastname': 'Harper',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        }]
        add_multiple_customers(test_customers)
        #customer_list = return_all_customers()
        #for customer in customer_list:
        #    print(customer)
        print_all_customers()

    