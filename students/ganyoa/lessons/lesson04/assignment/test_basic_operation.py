from basic_operation import *
from customer_model import *
import sqlite3
import unittest
'''
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
'''

#logging.basicConfig(level=logging.INFO, format="%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s")
#LOGGER.info('testing, one two')

def customer_setup():
    add_customer('009', 'Joe', 'Moe', '773 Apple St Strangefield, CT 03821', \
         '333-555-1234', 'jm@email.com', True, 150)
    add_customer('008', 'Terry', 'Scary', '999 Smeln St Freefield, ND 53821', \
             '222-555-1234', 'ts@email.com', True, 925)
    add_customer('007', 'Pam', 'Glam', '374 Brooke St Nofield, OR 97382', \
         '683-555-1234', 'pg@email.com', True, 375)

class TestBasicOps(unittest.TestCase):

    def test_db_creation(self):
        db.drop_tables([Customer])
        db.create_tables([Customer])



class TestCustomerModel(unittest.TestCase):
    def test_add_customer(self):
        '''add two customers to the database'''
        LOGGER.info('test_add_customer')
        customer_setup()

        add_cust01 = Customer.get(Customer.customer_id == '009') # Model.get() method
        self.assertEqual(add_cust01.last_name, 'Moe')
        self.assertEqual(add_cust01.email_address, 'jm@email.com')

        add_cust02 = Customer.select().where(Customer.customer_id == '008').get() # Select.get() method
        self.assertEqual(add_cust02.first_name, 'Terry')
        self.assertEqual(add_cust02.credit_limit, 925)


    def test_search_match(self):
        '''dictionary output matches expectation'''
        LOGGER.info('test_search_match')
        customer_setup()
        search_test01 = search_customer('009')
        self.assertDictEqual(search_test01, {'009': ['Joe', 'Moe', 'jm@email.com', '333-555-1234']})


    def test_search_no_match(self):
        '''empty dictionary is returned is customer_id is not found'''
        LOGGER.info('test_search_no_match')
        search_test02 = search_customer('765')
        self.assertDictEqual(search_test02, {})


    def test_delete_customer_match(self):
        """remove customer data from database for known customer_id"""
        LOGGER.info('test_delete_customer_match')
        customer_setup()
        delete_customer('009')
        self.assertDictEqual(search_customer('009'), {})


    def test_delete_customer_no_match(self):
        """attempt to remove customer data for non-existing customer_id"""
        LOGGER.info('test_delete_customer_no_match')
        with self.assertRaises(ValueError):
            delete_customer('055')

    def test_update_credit_match(self):
        '''update a customer credit amount for known customer_id'''
        LOGGER.info('test_update_credit_match')
        update_customer_credit('007', 575)
        cust_cred = Customer.select().where(Customer.customer_id == '007').get()
        self.assertEqual(cust_cred.credit_limit, 575)


    def test_update_credit_no_match(self):
        '''attempt to update credit for non-existing customer_id'''
        LOGGER.info('test_update_credit_no_match')
        with self.assertRaises(ValueError):
            update_customer_credit('005', 450)


    def test_list_active_customers(self):
        '''confirm active customer quantity is correct'''
        LOGGER.info("test_list_active_customers")
        customer_setup()
        self.assertEqual(list_active_customers(), 3)



