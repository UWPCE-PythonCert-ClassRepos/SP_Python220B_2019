'''Unit tests for basic_operations.py'''

# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name
# pylint: disable=wrong-import-position

import sys
#sys.path.append(r'C:\Users\chels\SP_Python220B_2019\students\chelsea_nayan\lesson03\src')
sys.path.insert(1, r'C:\Users\chels\SP_Python220B_2019\students\chelsea_nayan\lesson03\src')
sys.path.insert(1, '..')
from unittest import TestCase
import logging
from peewee import *

import create_db
from basic_operations import *
from customer_model import Customer

logging.basicConfig(level=logging.INFO)

def setup():
    '''Setting up the database'''
    LOGGER.info("Initializing the database!")
    database = create_db.database
    database.drop_tables([Customer])
    database.create_tables([Customer])
    database.close()

    LOGGER.info("Finished setting up the database!")

class TestingBasicOperations(TestCase):
    '''Testing py'''
    LOGGER.info('Start testing basic_operations.py!')

    CUSTOMER_LIST = [('01', 'Anakin', 'Skywalker', '100 1st Ave N', # Customer [0]
                      '(206)111-1111', 'aanacortes@email.com', 'Inactive', 10.00),
                     ('02', 'Bilbo', 'Baggins', '200 2nd Ave E', '(206)222-222', # Customer [1]
                      'bbaggins@email.com', 'Active', 20500.00),
                     ('03', 'Charlie', 'Chadmeister', '300 3rd Ave S', # Customer [2]
                      '(206)333-3333', 'cchadmesiter@gmail.com', 'Active', 4000),
                     ('04', 'Danny', 'Devito', '400 4th Ave W', '(206)444-444', # Customer [3]
                      'ddevito@email.com', 'Inactive', 500000)]
    LOGGER.info('Intialized ')

    def test_add_customer(self):
        '''Testing add_customer function'''
        LOGGER.info('Testing add_customer function!')
        setup()

        add_customer(*self.CUSTOMER_LIST[0])
        add_customer(*self.CUSTOMER_LIST[1])
        add_customer(*self.CUSTOMER_LIST[2])
        add_customer(*self.CUSTOMER_LIST[3])

        test_customer_01 = Customer.get(Customer.c_id == '01')
        test_customer_02 = Customer.get(Customer.c_id == '02')
        test_customer_03 = Customer.get(Customer.c_id == '03')
        test_customer_04 = Customer.get(Customer.c_id == '04')

        # Testing customer 01
        self.assertEqual(test_customer_01.c_firstname, self.CUSTOMER_LIST[0][1])
        self.assertEqual(test_customer_01.c_lastname, self.CUSTOMER_LIST[0][2])

        # Testing customer 02
        self.assertEqual(test_customer_02.c_home_address, self.CUSTOMER_LIST[1][3])
        self.assertEqual(test_customer_02.c_phone_number, self.CUSTOMER_LIST[1][4])

        # Testing customer 03
        self.assertEqual(test_customer_03.c_email_address, self.CUSTOMER_LIST[2][5])
        self.assertEqual(test_customer_03.c_status, self.CUSTOMER_LIST[2][6])

        # Testing customer 04
        self.assertEqual(test_customer_04.c_id, self.CUSTOMER_LIST[3][0])
        self.assertEqual(test_customer_04.c_firstname, self.CUSTOMER_LIST[3][1])
        self.assertEqual(test_customer_04.c_lastname, self.CUSTOMER_LIST[3][2])
        self.assertEqual(test_customer_04.c_home_address, self.CUSTOMER_LIST[3][3])
        self.assertEqual(test_customer_04.c_phone_number, self.CUSTOMER_LIST[3][4])
        self.assertEqual(test_customer_04.c_email_address, self.CUSTOMER_LIST[3][5])
        self.assertEqual(test_customer_04.c_status, self.CUSTOMER_LIST[3][6])
        self.assertEqual(test_customer_04.c_credit_limit, self.CUSTOMER_LIST[3][7])

        with self.assertRaises(IndexError):
            add_customer(*self.CUSTOMER_LIST[6])

        LOGGER.info('Finished testing add_customer function!')

    def test_search_customer(self):
        '''Testing search_customer function'''

        LOGGER.info('Testing search_customer function!')
        setup()

        add_customer(*self.CUSTOMER_LIST[3]) # Danny Devito
        expected = {'firstname': 'Danny',
                    'lastname': 'Devito',
                    'email_address': 'ddevito@email.com',
                    'phone_number': '(206)444-444'}

        empty_dict = {}

        try:
            test_dict = search_customer('04')
            test_none = search_customer('05')

            self.assertEqual(test_dict, expected)
            self.assertEqual(test_none, empty_dict)

        except DoesNotExist:
            assert False

        with self.assertRaises(IndexError):
            search_customer(self.CUSTOMER_LIST[5])

        LOGGER.info('Finished testing search_customer function!')

    def test_delete_customer(self):
        '''Testing delete_customer function'''

        LOGGER.info('Testing delete_customer function!')
        setup()

        add_customer(*self.CUSTOMER_LIST[0]) # Anakin Skywalker
        add_customer(*self.CUSTOMER_LIST[1]) # Bilbo Baggins
        add_customer(*self.CUSTOMER_LIST[2]) # Charlie Chadmeister
        add_customer(*self.CUSTOMER_LIST[3]) # Danny Devito

        test_customer_02 = Customer.get(Customer.c_id == '02')
        self.assertEqual(test_customer_02.c_firstname, 'Bilbo')
        delete_customer('02')

        with self.assertRaises(DoesNotExist):
            delete_customer('07')

        LOGGER.info('Finished testing delete_customer function!')

    def test_update_customer_credit(self):
        '''Testing update_customer_credit function'''

        LOGGER.info('Testing update_customer_credit function!')
        setup()

        add_customer(*self.CUSTOMER_LIST[2]) # Charlie Chadmeister
        add_customer(*self.CUSTOMER_LIST[3]) # Danny Devito

        test_customer_03 = Customer.get(Customer.c_id == '03')

        LOGGER.info('Customer id 03 credit limit is %i: ', self.CUSTOMER_LIST[2][7])
        LOGGER.info('Customer id 04 credit limit is %i: ', self.CUSTOMER_LIST[3][7])

        update_customer_credit('03', 3000.0)
        update_customer_credit('04', 2.0)

        self.assertEqual(test_customer_03.c_credit_limit, 4000.0)

        LOGGER.info('Finished testing update_customer_credit function!')

    def test_list_active_customers(self):
        '''Testing list_active_customers function'''
        LOGGER.info('Testing list_active_customers function!')
        setup()

        add_customer(*self.CUSTOMER_LIST[0]) # Anakin Skywalker
        add_customer(*self.CUSTOMER_LIST[1]) # Bilbo Baggins
        add_customer(*self.CUSTOMER_LIST[2]) # Charlie Chadmeister
        add_customer(*self.CUSTOMER_LIST[3]) # Danny Devito

        self.assertEqual(list_active_customers(), 2)

        active_status_count_1 = list_active_customers()
        self.assertEqual(2, active_status_count_1)

        test_customer_02 = Customer.get(Customer.c_id == '02')
        test_customer_02.delete_instance()
        active_status_count_2 = list_active_customers()
        self.assertEqual(1, active_status_count_2)

        LOGGER.info('Finished testing list_active_customers function!')

    def clear_database(self):
        '''Testing clear_database function'''

        LOGGER.info('Testing clear_database function!')

        for each in self.CUSTOMER_LIST:
            try:
                customer_exit = Customer.get(Customer.c_id == each[0])
                customer_exit.delete_instance()
            except DoesNotExist:
                LOGGER.info('Database does not exist!')

        LOGGER.info('Finished testing clear_database function!')
