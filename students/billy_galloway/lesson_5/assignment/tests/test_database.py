'''
Unit testing module
'''
import sys
sys.path.append("../hp_norton_inventory")
import os
import logging
from unittest import TestCase
from unittest.mock import patch
from pymongo import MongoClient
from database import *
from mongo_connect import *
from csv_handler import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseTests(TestCase):
    ''' Database test class '''
    def setUp(self):
        '''
        setup database and handle connections and closure
        '''
        logger.info(f'setting up test cases')
        try:
            os.path.exists('customer.csv')
            os.path.exists('product.csv')
            os.path.exists('rentals.csv')

            output = import_data('old_database', 'customer.csv', 'product.csv', 'rentals.csv')
            logger.info(f'{output}')
        except Exception as e:
            logger.info(f'{e}')

        self.customer = {
            'customer_id': 'A501',
            'name': 'David',
            'last_name': 'Nelson',
            'home_address': '7 Blackburn Drive Tualatin, OR 97062',
            'email_address': 'david@hpnorton.com',
            'phone_number': '202-555-0169',
            'status': True,
            'credit_limit': 0
        }

        self.product = {
            'customer_id': 'A501',
            'name': 'David',
            'last_name': 'Nelson',
            'home_address': '7 Blackburn Drive Tualatin, OR 97062',
            'email_address': 'david@hpnorton.com',
            'phone_number': '202-555-0169',
            'status': True,
            'credit_limit': 0
        }

        self.rentalS = {
            'product_id': 'prd006',
            'customer_id': 'user002',
            'name': 'Maya Data',
            'home_address': '4936 Elliot Avenue',
            'email_address': 'mdata@uw.edu',
            'phone_number': '206-777-1927',
        }

    def tearDown(self):
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.hpnorton_db
            db['customers'].drop()
            db['rentals'].drop()
            db['products'].drop()

    def test_database_created(self):
        '''
        Tests to ensure all the elements of the
        customer model are present

        Customer model elemenets:
            customer id
            name
            lastname
            home address
            email address
            status
            credit limit
        '''
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.hpnorton_db

            self.assertEqual(self.customer['customer_id'], 'A500')
            self.assertEqual(self.customer['name'], 'Andrew Smith')
            self.assertEqual(self.customer['home_address'], '23 Railroad Street')
            self.assertEqual(self.customer['email_address'], 'andrew@hpnorton.com')
            self.assertEqual(self.customer['phone_number'], '202-555-0134')
            self.assertEqual(self.customer['status'], True)
            self.assertEqual(self.customer['credit_limit'], 1000)

            self.assertEqual(self.product['product_id'], 'A500')
            self.assertEqual(self.product['description'], 'Andrew')
            self.assertEqual(self.product['product_type'], 'Smith')
            self.assertEqual(self.product['quantity_available'], '')
 
            self.assertEqual(self.rentals['product_id'], 'A500')
            self.assertEqual(self.rentals['customer_id'], 'Andrew')
            self.assertEqual(self.rentals['name'], 'Smith')
            self.assertEqual(self.rentals['home_address'], '23 Railroad Street Matthews, NC 28104')
            self.assertEqual(self.rentals['email_address'], 'andrew@hpnorton.com')
            self.assertEqual(self.rentals['phone_number'], '202-555-0134')

    def test_database_return_value(self):
        pass

    def test_available_products(self):
        pass
    def test_show_rentals(self):
        pass
    #     with database.transaction():

    #         #self.new_customer[CUST_ID] = ['A6000', 'AAAAA']

    #         add_customer(self.new_customer[CUST_ID], self.new_customer[NAME],
    #                      self.new_customer[LAST_NAME], self.new_customer[HOME_ADDRESS],
    #                      self.new_customer[EMAIL_ADDRESS], self.new_customer[PHONE],
    #                      self.new_customer[STATUS], self.new_customer[CREDIT_LIMIT])

    #     database.drop_tables([Customer])

    # def test_add_customer(self):
    #     ''' test that customers can be added to the existing database '''
    #     logger.info(f'add customer test')
    #     with patch('builtins.input', side_effect=[self.new_customer]):
    #         add_customer(self.new_customer[CUST_ID], self.new_customer[NAME],
    #                      self.new_customer[LAST_NAME], self.new_customer[HOME_ADDRESS],
    #                      self.new_customer[EMAIL_ADDRESS], self.new_customer[PHONE],
    #                      self.new_customer[STATUS], self.new_customer[CREDIT_LIMIT])

    #     added_customer = Customer.get(Customer.name == self.new_customer[NAME])
    #     self.assertEqual(added_customer.name, 'David')
    #     logger.info(f'Found customer name in database')

    #     try:
    #         add_customer(self.new_customer[CUST_ID], 'Davidddddd',
    #                      self.new_customer[LAST_NAME], self.new_customer[HOME_ADDRESS],
    #                      self.new_customer[EMAIL_ADDRESS], self.new_customer[PHONE],
    #                      self.new_customer[STATUS], self.new_customer[CREDIT_LIMIT])
    #     except Exception:
    #         self.assertRaises(IntegrityError)
    #     database.drop_tables([Customer])

    # def test_search_customer(self):
    #     ''' customer search test '''
    #     logger.info(f'search customer test')
    #     customer_id = 'B200'
    #     search_results = search_customer(customer_id)
    #     self.assertEqual(search_results['name'], 'Kate')

    #     with self.assertRaises(ValueError):
    #         customer_id = 'C200'
    #         search_results = search_customer(customer_id)
    #     logger.info(f'ValueError raised and customer id was not found')

    #     database.drop_tables([Customer])