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
            'customer_id': 'user001',
            'name': 'Andrew Smith',
            'home_address': '23 Railroad Street',
            'email_address': 'andrew@hpnorton.com',
            'phone_number': '202-555-0134',
            'status': True,
            'credit_limit': 1000
        }

        self.product = {
            'product_id': 'prd006',
            'description': 'computer',
            'product_type': 'office',
            'quantity_available': 0
        }

        self.rentals = {
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
        database are present
        '''
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.hpnorton_db

            customer_db = [x for x in db.customers.find()]
            self.assertEqual(self.customer['customer_id'], customer_db['customer_id'])
            self.assertEqual(self.customer['name'], customer_db['name'])
            self.assertEqual(self.customer['home_address'], customer_db['home_address'])
            self.assertEqual(self.customer['email_address'], customer_db['email_address'])
            self.assertEqual(self.customer['phone_number'], customer_db['phone_number'])
            self.assertEqual(self.customer['status'], customer_db['status'])
            self.assertEqual(self.customer['credit_limit'], customer_db['credit_limit'])

            producst_db = [x for x in db.product.find()]
            self.assertEqual(self.product['product_id'], product_db['product_id'])
            self.assertEqual(self.product['description'], product_db['name'])
            self.assertEqual(self.product['product_type'], product_db['product_type'])
            self.assertEqual(self.product['quantity_available'], product_db['quantity_available'])

            rentals_db = [x for x in db.rentals.find()]
            self.assertEqual(self.rentals['product_id'], rentals_db['product_id'])
            self.assertEqual(self.rentals['customer_id'], nrentalsdb['customer_id'])
            self.assertEqual(self.rentals['name'], rentals_db['name'])
            self.assertEqual(self.rentals['home_address'], rentals_db['home_address'])
            self.assertEqual(self.rentals['email_address'], rentals_db['email_address'])
            self.assertEqual(self.rentals['phone_number'], rentals_db['phone_number'])

    def test_database_return_value(self):
        self.assertEqual(added_customer.name, 'David')
    #     logger.info(f'Found customer name in database')

    def test_available_products(self):
        pass
    def test_show_rentals(self):
        pass
