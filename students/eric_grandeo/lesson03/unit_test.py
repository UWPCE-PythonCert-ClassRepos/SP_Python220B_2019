'''
Unit tests
'''

'''
import sys
# Add path to files
sys.path.append('/home/ejgrandeo/uwpython/SP_Python220B_2019/students/eric_grandeo/lesson03')
'''


from unittest import TestCase
#from customers_model import database, Customers
#from basic_operations import add_customer
from customers_model import *
from basic_operations import *
import peewee
import logging

#database = SqliteDatabase('customer.db')
#database.connect()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestBasicOperations(TestCase):
    '''insert docstring'''    
    
    def setUp(self):
        '''insert docstring''' 
        database.create_tables([Customers])
        logger.info('Create table successful')
        
    def tearDown(self):
        '''insert docstring''' 
        database.drop_tables([Customers])
        logger.info('Database tables dropped')
    
    def test_add_customer(self):
        '''insert docstring''' 
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
        self.assertEqual(record.customer_id, test_customer['customer_id'])
        
    def test_search_customer(self):
        '''insert docstring''' 
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
            'email_address':'email@email.com', 'phone_number':'1-212-555-1234'}
        result = search_customer('12345')
        self.assertEqual(result, customer_record)
        
    def test_search_customer_fail(self):
        '''insert docstring''' 
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
        '''insert docstring''' 
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
        '''insert docstring''' 
        with self.assertRaises(ValueError):
            delete_customer('2468')
            
    
       
    
    
   
       
        
        
        