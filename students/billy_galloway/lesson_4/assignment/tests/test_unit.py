'''
Unit testing module
'''
import sys
sys.path.append("../customer_db")
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
                             'david@hpnorton.com', '202-555-0169', True, 10]

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

            #self.new_customer[CUST_ID] = ['A6000', 'AAAAA']

            add_customer(self.new_customer[CUST_ID], self.new_customer[NAME],
                         self.new_customer[LAST_NAME], self.new_customer[HOME_ADDRESS],
                         self.new_customer[EMAIL_ADDRESS], self.new_customer[PHONE],
                         self.new_customer[STATUS], self.new_customer[CREDIT_LIMIT])

        database.drop_tables([Customer])

    def test_add_customer(self):
        ''' test that customers can be added to the existing database '''
        logger.info(f'add customer test')
        with patch('builtins.input', side_effect=[self.new_customer]):
            add_customer(self.new_customer[CUST_ID], self.new_customer[NAME],
                         self.new_customer[LAST_NAME], self.new_customer[HOME_ADDRESS],
                         self.new_customer[EMAIL_ADDRESS], self.new_customer[PHONE],
                         self.new_customer[STATUS], self.new_customer[CREDIT_LIMIT])

        added_customer = Customer.get(Customer.name == self.new_customer[NAME])
        self.assertEqual(added_customer.name, 'David')
        logger.info(f'Found customer name in database')

        try:
            add_customer(self.new_customer[CUST_ID], 'Davidddddd',
                         self.new_customer[LAST_NAME], self.new_customer[HOME_ADDRESS],
                         self.new_customer[EMAIL_ADDRESS], self.new_customer[PHONE],
                         self.new_customer[STATUS], self.new_customer[CREDIT_LIMIT])
        except Exception:
            self.assertRaises(IntegrityError)
        database.drop_tables([Customer])

    def test_search_customer(self):
        ''' customer search test '''
        logger.info(f'search customer test')
        customer_id = 'B200'
        search_results = search_customer(customer_id)
        self.assertEqual(search_results['name'], 'Kate')

        with self.assertRaises(ValueError):
            customer_id = 'C200'
            search_results = search_customer(customer_id)
        logger.info(f'ValueError raised and customer id was not found')

        database.drop_tables([Customer])

    def test_delete_customer(self):
        ''' ensure deletions are working '''
        logger.info(f'delete customer test')

        customer_id = 'A500'
        delete_customer(customer_id)

        try:
            deleted_customer = Customer.get(Customer.customer_id == self.customers[0][CUST_ID])
            self.assertEqual(deleted_customer.customer_id, 'A500')
        except DoesNotExist:
            logger.info(f'Customer not found in database: {customer_id}')

        database.drop_tables([Customer])

    def test_delete_customer_exception(self):
        ''' ensure error is thrown for customer '''
        try:
            customer_id = 'A5000'
            delete_customer(customer_id)
        except ValueError:
            logger.info(f'Customer not found in database: {customer_id}')
            self.assertRaises(ValueError)

        database.drop_tables([Customer])

    def test_update_customer_credit(self):
        ''' test updating customers credit limit '''
        logger.info(f'update customer credit limit test')
        new_limit = 888

        add_customer(self.new_customer[CUST_ID], self.new_customer[NAME],
                     self.new_customer[LAST_NAME], self.new_customer[HOME_ADDRESS],
                     self.new_customer[EMAIL_ADDRESS], self.new_customer[PHONE],
                     self.new_customer[STATUS], self.new_customer[CREDIT_LIMIT])

        updated_customer = Customer.get(customer_id=self.new_customer[CUST_ID])
        logger.info(f'Customers current limit: {updated_customer.credit_limit}')

        self.assertEqual(update_customer_credit('A501', 888), new_limit)
        logger.info(f'Customers limit after update: {Customer.get(Customer.customer_id == self.new_customer[CUST_ID]).credit_limit}')

        try:
            update_customer_credit('A5011', 888)
        except ValueError:
            logger.info(f'Customer not found')

        database.drop_tables([Customer])


    def test_list_active_customers(self):
        ''' test listing active customers '''
        logger.info(f'list active customers test')
        with patch('builtins.input', return_value=1):
            list_active_customers()

        self.assertEqual(list_active_customers(), 1)

        database.drop_tables([Customer])

    def test_list_active_customers_name(self):
        ''' test listing active customers by name '''
        logger.info(f'list active customers test')
        list_active_customers_name()

        self.assertEqual(list_active_customers_name(), ['Andrew'])

        database.drop_tables([Customer])

    def test_update_customer_status(self):
        ''' test udpate customer status '''
        logger.info(f'testing customer status')

        self.assertEqual(list_active_customers_name(), ['Andrew'])


        self.assertEqual(update_customer_status('A500', False), False)

        database.drop_tables([Customer])
