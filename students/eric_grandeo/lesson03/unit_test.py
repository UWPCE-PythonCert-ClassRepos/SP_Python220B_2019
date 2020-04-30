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
        
    def setUp(self):
        database.create_tables([Customers])
        logger.info('Create table successful')
        
    def tearDown(self):
        database.drop_tables([Customers])
        logger.info('Database tables dropped')
    
    def test_add_customer(self):
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
        test_customer = {'name':'Eric Grandeo', 'lastname':'Grandeo',
            'email_address':'email@email.com', 'phone_number':'1-212-555-1234'}
        result = search_customer('12345')
        self.assertEqual(result, test_customer)
        
        
    #should i create a static method for test customer that other tests call? should
    #i add it as a variable at the top?
    
    
   
       
        
        
        