'''
tests for the basic operations/customer database
'''

from unittest import TestCase
from peewee import *
from customer_db_model import Customer
from basic_operations import *

test_db = SqliteDatabase('test.db')

def db_setup():
    test_db.drop_tables([Customer])
    test_db.create_tables([Customer])


class BasicOperationsTest(TestCase):
    '''tests for basic operations'''

    def test_add_customer(self):
        '''test add customer function/'''
        db_setup()

        add_customer(1234, 'Zach', 'Thomson', '1000 John St', '2068675309',
                     'ScubaSteve@gmail.com', True, 1000.00)
        generic = Customer.get(Customer.customer_id == 1234)
        self.assertEqual(generic.customer_id, 1234)
        self.assertEqual(generic.name, 'Zach')
        self.assertEqual(generic.last_name, 'Thomson')
        self.assertEqual(generic.home_address, '1000 John St')
        self.assertEqual(generic.phone_number, '2068675309')
        self.assertEqual(generic.email_address, 'ScubaSteve@gmail.com')
        self.assertEqual(generic.status, True)
        self.assertEqual(generic.credit_limit, 1000.00)

    def test_search_customer(self):
        db_setup()

        add_customer(1234, 'Zach', 'Thomson', '1000 John St', '2068675309',
                     'ScubaSteve@gmail.com', True, 1000.00)
        search = search_customer(1234)
        expected_dict = {'name': 'Zach', 'last_name': 'Thomson',
                         'email_address': 'ScubaSteve@gmail.com', 'phone_number': '2068675309'}
        self.assertEqual(search, expected_dict)
        #search_2 = search_customer(900)
        #new_exp_dict = {}
        #self.assertEqual(search_2, new_exp_dict)
        #need to work on when a customer doesn't exist, empty dict returns

    def test_delete_customer(self):
        db_setup()

        add_customer(1234, 'Zach', 'Thomson', '1000 John St', '2068675309',
                     'ScubaSteve@gmail.com', True, 1000.00)
        delete_customer(1234)
        #work in progress

    def test_update_customer_credit(self):
        db_setup()

        add_customer(1234, 'Zach', 'Thomson', '1000 John St', '2068675309',
                     'ScubaSteve@gmail.com', True, 1000.00)
        update_customer_credit(1234, 2000.00)
        new_credit = Customer.get(Customer.customer_id == 1234)
        self.assertEqual(new_credit.credit_limit, 2000.00)
        #need to work on ValueError exception


    def test_list_active_customers(self):
        pass
