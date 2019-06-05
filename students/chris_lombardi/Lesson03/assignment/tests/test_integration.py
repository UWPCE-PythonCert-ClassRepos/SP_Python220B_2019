import sys
sys.path.append('C:\\Users\\chris\\documents\\PY220_Git\\SP_Python220B_2019\\'
                '\\students\\chris_lombardi\\Lesson03\\assignment')

import logging
import unittest
import basic_operations
from customer_model import *
import create_customers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Test_Basic_Operations(unittest.TestCase):
    """
    Test that the basic operations methods interact and function as a whole
    propoerly to add, delete, and search the database.
    """
    DATABASE = SqliteDatabase('customers.db')
    DATABASE.connect()
    DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

    CUST_LIST = [('001', 'Abe', 'Lincoln', '1600 Pennsylvania Ave NW',
              '9999990000', 'abe@whitehouse.com', 'Active', 10000.0),
              ('002', 'George', 'Washington', '1600 State St',
               '5601321111', 'george@whitehouse.com', 'Active', 5000.0),
              ('003', 'Ben', 'Franklin', '20401 Electric Ave',
               '1234567890', 'ben@elecave.com', 'Inactive', 23400.00)]

    logger.info('Clearing database...')
    for cust in CUST_LIST:
        try:
            cust_exit = Customer.get(Customer.cust_id == cust[0])
            cust_exit.delete_instance()
        except Exception as e:
            logger.info('DNE')
    logger.info('Database Clear!')

    def test_operations(self):

        logger.info(f'Adding customer {self.CUST_LIST[0][0]} to database.')
        basic_operations.add_customer(*self.CUST_LIST[0])
        logger.info(f'Adding customer {self.CUST_LIST[1][0]} to database.')
        basic_operations.add_customer(*self.CUST_LIST[1])

        try:
            logger.info('Checking that customer id 001 is in the database...')
            test_dict = basic_operations.search_customer('001')
            expected_dict = {'name': self.CUST_LIST[0][1], 'lastname': self.CUST_LIST[0][2],
                             'email address': self.CUST_LIST[0][5], 'phone number': self.CUST_LIST[0][4]}
            self.assertEqual(test_dict, expected_dict)
            logger.info('Found Customer 001!')
        except Exception as e:
            logger.info('Customer id 001 not found in database.')
            assert False

        try:
            logger.info('Looking for customer id 003 in the database...')
            #for cust in Customer:

            test_empty = basic_operations.search_customer('003')
            self.assertEqual({}, test_empty)
            logger.info('Confirmed no customer id 003 in the database...')
        except Exception as e:
            logger.info('Incorrectly found customer id 003 in the database...')
            assert False

        try:
            logger.info('Attempting to delete customer 002 from database...')
            acust = basic_operations.delete_customer('002')
            logger.info('Customer 002 succesfully deleted!')
        except Exception as e:
            logger.info('Customer 002 was not deleted from the database as requested...')
            assert False

        logger.info('Searching for customer 002 to confirm deletion.')
        test_deleted = basic_operations.search_customer('002')
        self.assertEqual({}, test_deleted)

        logger.info('Checking that there is only one active customer in the database...')
        num_active = basic_operations.list_active_customers()
        self.assertEqual(1, num_active)
        logger.info('Confirmed only one active customer.')

        logger.info('Adding customer 003 to the database.')
        basic_operations.add_customer(*self.CUST_LIST[2])
        logger.info('Checking that there is still only one active customer in the database...')
        num_active_again = basic_operations.list_active_customers()
        self.assertEqual(1, num_active_again)
        logger.info('Confirmed only one active customer')