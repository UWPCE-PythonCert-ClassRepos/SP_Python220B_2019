'''
Unit testing module
'''
import sys
sys.path.append("../hp_norton_inventory")
import os
import logging
import threading
from queue import Queue
from unittest import TestCase
from unittest.mock import patch
from pymongo import MongoClient
from parallel import *
from mongo_connect import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseTests(TestCase):
    ''' Database test class '''
    def setUp(self):
        '''
        setup database and handle connections and closure
        '''
        self.test_queue = Queue()
        logger.info(f'setting up test cases')
        try:
            os.path.exists('customer.csv')
            os.path.exists('product.csv')
            os.path.exists('rental.csv')

            output = import_data('data', 'customer.csv', 'product.csv', 'rental.csv', self.test_queue)
            logger.info(f'{output}')
        except FileNotFoundError as e:
            logger.info(f'{e}')

    def tearDown(self):
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.hpnorton_db
            db['customer'].drop()
            db['rental'].drop()
            db['product'].drop()

    def test_database_created(self):
        '''
        Tests to ensure all the elements of the
        database are present
        '''
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.hpnorton_db

            ''' confirm customer document is correct '''
            customer_db = [x for x in db.customer.find()]
            self.assertEqual(customer_db[0]['customer_id'], 'user001')
            

            ''' confirm product document is correct '''
            product_db = [x for x in db.product.find()]
            self.assertEqual(product_db[0]['product_id'], 'prd001')


            ''' confirm rentals document is corrrect '''
            rentals_db = [x for x in db.rental.find()]
            self.assertEqual(rentals_db[0]['product_id'], 'prd001')

    def test_database_return_value(self):
        ''' ensures that a list of 2 tuples is returned '''
        output = import_data('data', 'customer.csv', 'product.csv', 'rental.csv', self.test_queue)
        logger.info(f'{output}')
        self.assertTupleEqual(output[0], (2002, 2002, 1000))
        self.assertTupleEqual(output[1], (0, 0, 0))

    def test_database_error_return(self):
        ''' ensure error count matches '''
        output = import_data('data', 'customer', 'product', 'rental', self.test_queue)
        logger.info(f'{output}')
        self.assertTupleEqual(output[0], (0, 0, 0))
        self.assertTupleEqual(output[1], (1, 1, 1))

    def test_available_products(self):
        ''' ensure only available products are returned '''
        output = show_available_products()
        logger.info(f'Products available for rent')
        self.assertEqual(output[0]['product_id'], 'prd001')
        self.assertEqual(output[0]['description'], '60-inch TV stand')
        self.assertEqual(output[0]['product_type'], 'livingroom')
        self.assertEqual(output[0]['quantity_available'], '3')

    def test_show_rentals(self):
        ''' ensure rentals are displaybed '''
        output = show_rentals('prd006')
        print(output)
        self.assertEqual(output[0]['product_id'], 'prd006')

    def test_main(self):
        ''' just for coverage '''
        main()