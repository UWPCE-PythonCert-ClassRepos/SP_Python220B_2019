'''
Unit testing module
'''
import sys
sys.path.append("../customer_db")
import peewee
import os
from unittest import TestCase
from unittest.mock import patch
from basic_operations import *
from create_customer import *
from customer_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CUST_ID = 0
NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
EMAIL_ADDRESS = 4
PHONE = 5
STATUS = 6
CREDIT_LIMIT = 7

class DatabaseTests(TestCase):
    ''' Database test class '''
    def setUp(self):
        ''' 
        setup database and handle connections and closure 
        '''
        logger.info(f'setting up test cases')
        logger.info(f'creating database customers.db')
        database.create_tables([Customer])


        self.customers = [
            ('A500', 'Andrew', 'Smith',
            '23 Railroad Street Matthews, NC 28104', 'andrew@hpnorton.com',
            '202-555-0134', True, 1000),
            ('B200', 'Kate', 'Harris',
            '638 Cactus St. Wilmington, MA 01887', 'kate@hpnorton.com',
            '202-555-0169', False, 1000)
        ]

        self.new_customer = ['A501', 'David', 'Nelson',
                             '7 Blackburn Drive Tualatin, OR 97062',
                             'david@hpnorton.com','202-555-0169', True, 0]

        try:
            os.path.exists('customers.db')
        except Exception as e:
            logger.info(f'{e}') 

        try:
            for customer in self.customers:
                with database.transaction():
                    add_customer(customer[CUST_ID], customer[NAME],
                                 customer[LAST_NAME], customer[HOME_ADDRESS],
                                 customer[EMAIL_ADDRESS], customer[PHONE],
                                 customer[STATUS], customer[CREDIT_LIMIT])
        except Exception as e:
            logger.info(f'Exception: {e}')


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
        self.assertEqual(self.customers[0][CUST_ID], 'A500')
        self.assertEqual(self.customers[0][NAME], 'Andrew')
        self.assertEqual(self.customers[0][LAST_NAME], 'Smith')
        self.assertEqual(self.customers[0][HOME_ADDRESS], '23 Railroad Street Matthews, NC 28104')
        self.assertEqual(self.customers[0][EMAIL_ADDRESS], 'andrew@hpnorton.com')
        self.assertEqual(self.customers[0][PHONE], '202-555-0134')
        self.assertEqual(self.customers[0][STATUS], True)
        self.assertEqual(self.customers[0][CREDIT_LIMIT], 1000)

        with database.transaction():
            self.new_customer[0][CUST_ID] = 'AAAAA'
            add_customer(self.new_customer[0][CUST_ID], self.new_customer[0][NAME],
                         self.new_customer[0][LAST_NAME], self.new_customer[0][HOME_ADDRESS],
                         self.new_customer[0][EMAIL_ADDRESS], self.new_customer[0][PHONE],
                         self.new_customer[0][STATUS], self.new_customer[0][CREDIT_LIMIT])

        database.drop_tables([Customer])

    def test_search_customer(self):
        customer_id = 'B200'
        search_results = search_customer(customer_id)
        self.assertEqual(search_results['name'], 'Kate')

        with self.assertRaises(ValueError):
            customer_id = 'C200'
            search_results = search_customer(customer_id)
        logger.info(f'ValueError raised and customer id was not found')
        database.drop_tables([Customer])

#     def test_basic_operations(self):
#         ''' 
#         Tests that basic operations are functioning
#         basic operations:
#             add_customer
#             search_customer
#             delete_customer
#             update_customer
#             list_active_customer
#         '''
#         database.drop_tables([Customer])

# logger.info(f'clearing out existing database if it exists.')


# add_customer(customers[1][CUST_ID], customers[1][NAME], customers[1][LAST_NAME],
#              customers[1][HOME_ADDRESS], customers[1][EMAIL_ADDRESS],
#              customers[1][PHONE], customers[1][STATUS], customers[1][CREDIT_LIMIT])

# add_customer(customers[2][CUST_ID], customers[2][NAME], customers[2][LAST_NAME],
#              customers[2][HOME_ADDRESS], customers[2][EMAIL_ADDRESS],
#              customers[2][PHONE], customers[2][STATUS], customers[2][CREDIT_LIMIT])

